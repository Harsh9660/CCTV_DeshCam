import cv2
import uvicorn
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time
import logging
import numpy as np
import config
from sqlalchemy.orm import Session
from database import SessionLocal, engine, init_db, Alert
import datetime
from fake_camera import FakeCameraFeed
from mock_alerts import MockAlertGenerator
from typing import List
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DB
init_db()

app = FastAPI(title="CCTV Safety Monitoring System", version="2.0")

# Initialize fake camera and alert generator
fake_camera = FakeCameraFeed(width=640, height=480, fps=30)
alert_generator = MockAlertGenerator()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            if conn in self.active_connections:
                self.active_connections.remove(conn)

manager = ConnectionManager()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Global variables for stats
stats = {
    "active_cameras": 4,
    "total_alerts": 0,
    "uptime": 0,
    "start_time": time.time()
}

# Store historical alerts in memory
historical_alerts = alert_generator.generate_historical_alerts(50)

def generate_frames():
    """
    Generator function to create fake video frames
    """
    global historical_alerts
    
    while True:
        try:
            # Generate frame from fake camera
            frame, detections, (alert_triggered, alert_message) = fake_camera.generate_frame()
            
            # If alert triggered, broadcast to WebSocket clients
            if alert_triggered:
                alert_data = alert_generator.generate_alert()
                historical_alerts.insert(0, alert_data)
                
                # Broadcast to WebSocket
                asyncio.create_task(manager.broadcast(alert_data))
                
                logger.info(f"Alert generated: {alert_message}")
            
            # Encode frame
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                logger.error("Failed to encode frame")
                continue
                
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Control frame rate
            time.sleep(1/30)  # 30 FPS
            
        except Exception as e:
            logger.error(f"Error generating frame: {e}")
            time.sleep(0.1)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CCTV Safety Monitoring System API",
        "version": "2.0",
        "status": "operational"
    }

@app.get("/video_feed")
async def video_feed():
    """Stream fake video feed"""
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    stats["uptime"] = int(time.time() - stats["start_time"])
    stats["total_alerts"] = len(historical_alerts)
    
    # Calculate severity breakdown
    severity_stats = alert_generator.get_stats(historical_alerts)
    
    return {
        **stats,
        "severity_breakdown": {
            "critical": severity_stats.get('critical', 0),
            "high": severity_stats.get('high', 0),
            "medium": severity_stats.get('medium', 0),
            "low": severity_stats.get('low', 0)
        },
        "status_breakdown": {
            "active": severity_stats.get('active', 0),
            "resolved": severity_stats.get('resolved', 0)
        }
    }

@app.get("/alerts")
async def get_alerts(limit: int = 50):
    """Get recent alerts"""
    return historical_alerts[:limit]

@app.get("/alerts/{alert_id}")
async def get_alert(alert_id: int):
    """Get specific alert by ID"""
    alert = next((a for a in historical_alerts if a['id'] == alert_id), None)
    if alert:
        return alert
    return {"error": "Alert not found"}, 404

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time alerts"""
    await manager.connect(websocket)
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to CCTV Monitoring System",
            "timestamp": datetime.datetime.now().isoformat()
        })
        
        # Keep connection alive and listen for messages
        while True:
            try:
                # Wait for messages from client (ping/pong)
                data = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                
                # Echo back or handle client messages
                if data == "ping":
                    await websocket.send_json({"type": "pong"})
                    
            except asyncio.TimeoutError:
                # Send keepalive
                await websocket.send_json({
                    "type": "keepalive",
                    "timestamp": datetime.datetime.now().isoformat()
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected normally")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat(),
        "active_connections": len(manager.active_connections)
    }

# Background task to periodically generate alerts
async def periodic_alert_generator():
    """Generate alerts periodically"""
    global historical_alerts
    
    while True:
        try:
            await asyncio.sleep(15)  # Every 15 seconds
            
            # 30% chance to generate an alert
            if np.random.random() < 0.3:
                alert_data = alert_generator.generate_alert()
                historical_alerts.insert(0, alert_data)
                
                # Broadcast to all connected clients
                await manager.broadcast(alert_data)
                
                logger.info(f"Periodic alert: {alert_data['event']}")
                
        except Exception as e:
            logger.error(f"Error in periodic alert generator: {e}")

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("Starting CCTV Monitoring System...")
    logger.info(f"Fake camera initialized: {fake_camera.width}x{fake_camera.height}")
    logger.info(f"Historical alerts loaded: {len(historical_alerts)}")
    
    # Start periodic alert generator
    asyncio.create_task(periodic_alert_generator())

@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down CCTV Monitoring System...")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        log_level="info"
    )

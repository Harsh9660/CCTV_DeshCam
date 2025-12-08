import cv2
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import time
import logging
import numpy as np
import config
from Models.AI_models import CCTVSystem
from sqlalchemy.orm import Session
from database import SessionLocal, engine, init_db, Alert
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize DB
init_db()

app = FastAPI()
system = CCTVSystem()
cap = None

@app.on_event("startup")
async def startup_event():
    global cap
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    if not cap.isOpened():
        logger.warning("Webcam not found. Will use dummy video generation.")
        cap = None

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

system = CCTVSystem(model_path='yolov8n.pt') 

# Global variables for stats
stats = {
    "active_cameras": 1,
    "total_alerts": 0,
    "uptime": 0,
    "start_time": time.time()
}

def generate_frames(db: Session):
    """
    Generator function to read frames, process them, and yield them as MJPEG stream.
    """
    global cap
    while True:
        if cap and cap.isOpened():
            success, frame = cap.read()
            if not success:
                logger.error("Failed to read from webcam.")
                time.sleep(1)
                continue
        else:
            # Dummy frame
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, f"No Camera - {time.ctime()}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            time.sleep(0.1)

        # Process frame
        detections, recognized_faces = system.process_frame(frame)
        
        # Save alerts to DB
        # We check system.alerts queue which is populated by process_frame -> trigger_alert
        # But system.alerts is in-memory deque. We should intercept or modify trigger_alert.
        # For now, let's just check the detections here and save to DB directly to avoid modifying AI_models too much
        # OR better, we iterate over the new alerts.
        # Actually, system.process_frame calls trigger_alert which appends to system.alerts.
        # We can pop from system.alerts and save to DB.
        
        while system.alerts:
            alert_data = system.alerts.pop() # Pop right (oldest) or popleft? appendleft used. so pop() is oldest.
            # Wait, appendleft means newest is at 0. pop() gets oldest.
            # Let's just save the newest ones.
            # Actually, let's just save what's in the queue and clear it?
            # system.alerts is a deque.
            
            # To be safe and simple:
            db_alert = Alert(
                timestamp=datetime.datetime.now(),
                camera=alert_data['camera'],
                event=alert_data['event'],
                details=alert_data['details'],
                status=alert_data['status']
            )
            db.add(db_alert)
            db.commit()
            stats["total_alerts"] += 1
            
        processed_frame = system.draw_on_frame(frame, detections, recognized_faces)
        
        # Encode
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    # We need a DB session for the generator. 
    # This is tricky with StreamingResponse. 
    # Instead of passing DB to generator, let's use a fresh session inside or just skip DB in generator for now?
    # No, we need to save alerts.
    # Let's create a session manually.
    db = SessionLocal()
    try:
        return StreamingResponse(generate_frames(db), media_type="multipart/x-mixed-replace; boundary=frame")
    except Exception as e:
        logger.error(f"Stream error: {e}")
        db.close()

@app.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    stats["uptime"] = int(time.time() - stats["start_time"])
    stats["total_alerts"] = db.query(Alert).count()
    return stats

@app.get("/alerts")
async def get_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(Alert.timestamp.desc()).limit(50).all()
    return alerts

if __name__ == "__main__":
    uvicorn.run(app, host=config.SERVER_HOST, port=config.SERVER_PORT)

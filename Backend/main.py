import cv2
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import time
import logging
import numpy as np
import config
from Models.AI_models import CCTVSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


system = CCTVSystem(model_path='yolov8n.pt') 

# Global variables for stats
stats = {
    "active_cameras": 1,
    "total_alerts": 0,
    "uptime": 0,
    "start_time": time.time()
}

def generate_frames():
    """
    Generator function to read frames, process them, and yield them as MJPEG stream.
    """
    # Try to open webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        logger.warning("Webcam not found. Using dummy video generation.")
        
        while True:
        
            import numpy as np
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, f"No Camera - {time.ctime()}", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            # Process frame (detection will be empty but pipeline runs)
            processed_frame = system.process_frame(frame)
            
            # Encode
            ret, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.1)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
            
        # Process frame
        processed_frame = system.process_frame(frame)
        
        # Encode
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
async def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/stats")
async def get_stats():
    stats["uptime"] = int(time.time() - stats["start_time"])
    # In a real app, we'd update alerts count from the system
    return stats

@app.get("/alerts")
async def get_alerts():
    # Placeholder for alerts
    return [
        {"time": "10:42 AM", "camera": "Cam 01", "event": "Person Detected", "status": "Review"},
        {"time": "10:38 AM", "camera": "Cam 02", "event": "Vehicle Entry", "status": "Logged"}
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

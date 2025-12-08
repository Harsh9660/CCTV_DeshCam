"""
Centralized configuration for the CCTV Dashcam project.
"""
import os
from typing import List

# --- General Settings ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- AI Model Settings ---

# Path to the YOLO model file.
YOLO_MODEL_PATH: str = "yolov8s.pt"

# Directory containing images of known faces for recognition.
# Set to None to disable face recognition.
KNOWN_FACES_DIR: str = os.path.join(BASE_DIR, "data", "known_faces")

# List of YOLO object classes to be considered 'critical' for triggering alerts.
CRITICAL_CLASSES: List[str] = ['person', 'knife', 'fire']

# Confidence threshold for a detection to be considered valid.
DETECTION_CONFIDENCE_THRESHOLD: float = 0.5

# --- Backend/Stream Settings ---

# Index of the camera to use (e.g., 0 for the default webcam).
CAMERA_INDEX: int = 0
# Host and port for the FastAPI server.
SERVER_HOST: str = "0.0.0.0"
SERVER_PORT: int = 8000
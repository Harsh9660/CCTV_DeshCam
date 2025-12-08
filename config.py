"""
Centralized configuration for the Childcare Safety Monitoring System.
"""
import os
from typing import List, Dict
from enum import Enum

# --- General Settings ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Zones ---
class Zone(str, Enum):
    OUTDOOR_PLAY = "outdoor_play"
    CLASSROOM = "classroom"
    STAFF_ROOM = "staff_room"
    HALLWAY = "hallway"
    ENTRANCE = "entrance"

# Zone to Camera Mapping (camera_id: zone)
CAMERA_ZONES = {
    0: Zone.OUTDOOR_PLAY,  # Default webcam for testing
    # Add more cameras as needed
}

# --- AI Model Settings ---

# YOLO Model for general object detection
YOLO_MODEL_PATH: str = "yolov8s.pt"

# Fence Defect Detection Model (from Roboflow)
FENCE_MODEL_PATH: str = os.path.join(BASE_DIR, "models", "fence_defect.pt")
FENCE_DEFECT_CLASSES: List[str] = ['HOLE', 'BENT', 'BROKEN', 'COLLAPSED']

# Person Classification
PERSON_HEIGHT_THRESHOLD: int = 120  # pixels - approximate child vs adult differentiation
CHILD_MAX_HEIGHT: int = 120  # Max height in pixels for child classification

# Face Recognition
KNOWN_FACES_DIR: str = os.path.join(BASE_DIR, "data", "known_faces")
STAFF_FACES_DIR: str = os.path.join(KNOWN_FACES_DIR, "staff")
CHILDREN_FACES_DIR: str = os.path.join(KNOWN_FACES_DIR, "children")

# Uniform Detection
UNIFORM_MODEL_PATH: str = os.path.join(BASE_DIR, "models", "uniform_detector.pt")

# --- Detection Thresholds ---
DETECTION_CONFIDENCE_THRESHOLD: float = 0.5
FENCE_DEFECT_THRESHOLD: float = 0.6
CLIMBING_HAZARD_DISTANCE: int = 50  # pixels from fence

# --- Alert Severity Levels ---
class AlertSeverity(str, Enum):
    CRITICAL = "critical"  # Immediate action required
    HIGH = "high"         # Urgent attention needed
    MEDIUM = "medium"     # Should be addressed soon
    LOW = "low"           # Informational

# Scenario to Severity Mapping
SCENARIO_SEVERITY: Dict[str, AlertSeverity] = {
    "fence_damage": AlertSeverity.CRITICAL,
    "unsupervised_child": AlertSeverity.CRITICAL,
    "unauthorized_adult": AlertSeverity.CRITICAL,
    "climbing_hazard": AlertSeverity.HIGH,
    "restricted_area_entry": AlertSeverity.HIGH,
    "emergency_route_blocked": AlertSeverity.CRITICAL,
    "uniform_violation": AlertSeverity.MEDIUM,
    "staff_location": AlertSeverity.LOW,
}

# --- Backend/Stream Settings ---
CAMERA_INDEX: int = 0
SERVER_HOST: str = "0.0.0.0"
SERVER_PORT: int = 8000

# --- Heatmap Settings ---
HEATMAP_DECAY_RATE: float = 0.95  # How quickly activity fades
HEATMAP_UPDATE_INTERVAL: int = 30  # seconds
"""
Fence Defect Detector - Detects critical fence defects (HOLE, BENT, BROKEN, COLLAPSED)
"""
import cv2
import logging
from typing import List, Dict, Any
import config

logger = logging.getLogger(__name__)

try:
    from ultralytics import YOLO
except ImportError:
    logger.error("ultralytics not found")
    YOLO = None

class FenceDefectDetector:
    def __init__(self):
        self.model = self._load_model()
        self.critical_classes = config.FENCE_DEFECT_CLASSES
    
    def _load_model(self):
        """Load fence defect detection model"""
        if YOLO:
            try:
                # Try to load custom fence model, fallback to general YOLO
                if config.FENCE_MODEL_PATH and os.path.exists(config.FENCE_MODEL_PATH):
                    logger.info(f"Loading fence defect model from {config.FENCE_MODEL_PATH}")
                    return YOLO(config.FENCE_MODEL_PATH)
                else:
                    logger.warning("Fence model not found, using general YOLO")
                    return YOLO(config.YOLO_MODEL_PATH)
            except Exception as e:
                logger.error(f"Failed to load fence model: {e}")
                return None
        return None
    
    def detect_defects(self, frame: Any) -> List[Dict[str, Any]]:
        """
        Detect fence defects in frame
        
        Returns:
            List of defect detections with class, confidence, and bbox
        """
        defects = []
        if not self.model:
            return defects
        
        try:
            results = self.model(frame, verbose=False)
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = self.model.names[cls_id]
                    
                    # Check if it's a critical defect
                    if label in self.critical_classes and conf >= config.FENCE_DEFECT_THRESHOLD:
                        defects.append({
                            'type': label,
                            'confidence': conf,
                            'bbox': box.xyxy[0].tolist(),
                            'severity': 'CRITICAL'
                        })
        except Exception as e:
            logger.error(f"Error detecting fence defects: {e}")
        
        return defects

# Import os at the top
import os

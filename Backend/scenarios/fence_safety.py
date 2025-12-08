"""
Fence Safety Scenario - Handles fence damage and climbing hazard detection
"""
import logging
from typing import List, Dict, Any
import config
from models.fence_detector import FenceDefectDetector

logger = logging.getLogger(__name__)

class FenceSafetyScenario:
    def __init__(self):
        self.fence_detector = FenceDefectDetector()
    
    def check_fence_damage(self, frame: Any) -> List[Dict[str, Any]]:
        """
        Check for fence defects (HOLE, BENT, BROKEN, COLLAPSED)
        
        Returns:
            List of alerts for fence damage
        """
        alerts = []
        defects = self.fence_detector.detect_defects(frame)
        
        for defect in defects:
            alerts.append({
                'scenario': 'fence_damage',
                'severity': 'CRITICAL',
                'event': f"Fence Defect: {defect['type']}",
                'details': f"Detected {defect['type']} with {defect['confidence']:.2f} confidence",
                'confidence': defect['confidence'],
                'bbox': defect['bbox']
            })
        
        return alerts
    
    def check_climbing_hazard(self, frame: Any, objects: List[Dict]) -> List[Dict[str, Any]]:
        """
        Check for objects near fence that could be climbing aids
        
        Args:
            frame: Image frame
            objects: List of detected objects with bboxes
        
        Returns:
            List of alerts for climbing hazards
        """
        alerts = []
        
        # Define climbing aid classes
        climbing_aids = ['chair', 'bench', 'table', 'box', 'crate']
        
        # TODO: Implement fence boundary detection
        # For now, assume fence is at edges of frame
        frame_height, frame_width = frame.shape[:2]
        fence_zones = [
            (0, 0, frame_width, 50),  # Top
            (0, frame_height-50, frame_width, frame_height),  # Bottom
            (0, 0, 50, frame_height),  # Left
            (frame_width-50, 0, frame_width, frame_height),  # Right
        ]
        
        for obj in objects:
            if obj.get('label') in climbing_aids:
                bbox = obj['bbox']
                x1, y1, x2, y2 = bbox
                obj_center = ((x1 + x2) / 2, (y1 + y2) / 2)
                
                # Check if object is near fence
                for fence_zone in fence_zones:
                    fx1, fy1, fx2, fy2 = fence_zone
                    if (fx1 <= obj_center[0] <= fx2 and fy1 <= obj_center[1] <= fy2):
                        alerts.append({
                            'scenario': 'climbing_hazard',
                            'severity': 'HIGH',
                            'event': f"Climbing Hazard: {obj['label']} near fence",
                            'details': f"Detected {obj['label']} positioned near boundary fence",
                            'confidence': obj['confidence'],
                            'bbox': bbox
                        })
                        break
        
        return alerts

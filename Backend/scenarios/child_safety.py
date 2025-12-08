"""
Child Safety Scenario - Handles unsupervised children and restricted area entry
"""
import logging
from typing import List, Dict, Any
from models.person_classifier import PersonClassifier

logger = logging.getLogger(__name__)

class ChildSafetyScenario:
    def __init__(self):
        self.person_classifier = PersonClassifier()
    
    def check_unsupervised_child(self, frame: Any, persons: List[Dict]) -> List[Dict[str, Any]]:
        """
        Check if children are present without staff supervision
        
        Args:
            frame: Image frame
            persons: List of detected persons with classifications
        
        Returns:
            List of alerts for unsupervised children
        """
        alerts = []
        
        children = [p for p in persons if p['person_type'] == 'child']
        staff = [p for p in persons if p['person_type'] == 'staff']
        
        if children and not staff:
            for child in children:
                alerts.append({
                    'scenario': 'unsupervised_child',
                    'severity': 'CRITICAL',
                    'event': 'Unsupervised Child Detected',
                    'details': f"Child detected without staff supervision",
                    'confidence': child['confidence'],
                    'bbox': child['bbox']
                })
        
        return alerts
    
    def check_restricted_area_entry(self, frame: Any, persons: List[Dict], zone: str) -> List[Dict[str, Any]]:
        """
        Check if children entered restricted areas
        
        Args:
            frame: Image frame
            persons: List of detected persons
            zone: Current zone (e.g., "hallway", "staff_room")
        
        Returns:
            List of alerts for restricted area entry
        """
        alerts = []
        
        # Define restricted zones for children
        restricted_zones = ['staff_room', 'hallway']
        
        if zone in restricted_zones:
            children = [p for p in persons if p['person_type'] == 'child']
            for child in children:
                alerts.append({
                    'scenario': 'restricted_area_entry',
                    'severity': 'HIGH',
                    'event': f'Child in Restricted Area: {zone}',
                    'details': f"Child detected in {zone} which is a restricted area",
                    'confidence': child['confidence'],
                    'bbox': child['bbox']
                })
        
        return alerts
    
    def check_emergency_route(self, frame: Any, objects: List[Dict]) -> List[Dict[str, Any]]:
        """
        Check if emergency routes are obstructed
        
        Args:
            frame: Image frame
            objects: List of detected objects
        
        Returns:
            List of alerts for blocked emergency routes
        """
        alerts = []
        
        # Define obstruction classes
        obstructions = ['box', 'crate', 'furniture', 'equipment', 'vehicle']
        
        # TODO: Define emergency route zones
        # For now, check for large objects that could block paths
        for obj in objects:
            if obj.get('label') in obstructions:
                bbox = obj['bbox']
                x1, y1, x2, y2 = bbox
                obj_area = (x2 - x1) * (y2 - y1)
                
                # If object is large enough to block a path
                if obj_area > 10000:  # Threshold in pixels
                    alerts.append({
                        'scenario': 'emergency_route_blocked',
                        'severity': 'CRITICAL',
                        'event': 'Emergency Route Potentially Blocked',
                        'details': f"Large {obj['label']} detected that may obstruct emergency exit",
                        'confidence': obj['confidence'],
                        'bbox': bbox
                    })
        
        return alerts

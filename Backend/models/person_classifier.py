"""
Person Classifier - Differentiates between staff, children, and unknown adults
"""
import os
import cv2
import logging
from typing import List, Dict, Any, Tuple
import config
import numpy as np

logger = logging.getLogger(__name__)

try:
    import face_recognition
except ImportError:
    logger.warning("face_recognition not found")
    face_recognition = None

class PersonClassifier:
    def __init__(self, staff_faces_dir=None, children_faces_dir=None):
        self.staff_encodings = []
        self.staff_names = []
        self.child_encodings = []
        self.child_names = []
        
        if staff_faces_dir:
            self._load_faces(staff_faces_dir, is_staff=True)
        if children_faces_dir:
            self._load_faces(children_faces_dir, is_staff=False)
    
    def _load_faces(self, directory: str, is_staff: bool):
        """Load face encodings from directory"""
        if not face_recognition or not os.path.exists(directory):
            return
        
        person_type = "staff" if is_staff else "children"
        logger.info(f"Loading {person_type} faces from {directory}")
        
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(directory, filename)
                try:
                    image = face_recognition.load_image_file(filepath)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        name = os.path.splitext(filename)[0]
                        if is_staff:
                            self.staff_encodings.append(encodings[0])
                            self.staff_names.append(name)
                        else:
                            self.child_encodings.append(encodings[0])
                            self.child_names.append(name)
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")
    
    def classify_person(self, frame: Any, bbox: List[int]) -> Dict[str, Any]:
        """
        Classify a detected person as staff, child, or unknown
        
        Args:
            frame: Image frame
            bbox: Bounding box [x1, y1, x2, y2]
        
        Returns:
            Dict with person_type, name, confidence
        """
        x1, y1, x2, y2 = map(int, bbox)
        height = y2 - y1
        
        # Simple heuristic: smaller bounding boxes are likely children
        if height < config.CHILD_MAX_HEIGHT:
            person_type = "child"
        else:
            person_type = "adult"
        
        # Try face recognition if available
        if face_recognition and (self.staff_encodings or self.child_encodings):
            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                
                # Filter face locations to those within bbox
                relevant_faces = [
                    loc for loc in face_locations
                    if self._is_face_in_bbox(loc, bbox)
                ]
                
                if relevant_faces:
                    face_encodings = face_recognition.face_encodings(rgb_frame, relevant_faces)
                    if face_encodings:
                        # Check staff first
                        if self.staff_encodings:
                            matches = face_recognition.compare_faces(self.staff_encodings, face_encodings[0])
                            if True in matches:
                                idx = matches.index(True)
                                return {
                                    'person_type': 'staff',
                                    'name': self.staff_names[idx],
                                    'confidence': 0.9,
                                    'bbox': bbox
                                }
                        
                        # Check children
                        if self.child_encodings:
                            matches = face_recognition.compare_faces(self.child_encodings, face_encodings[0])
                            if True in matches:
                                idx = matches.index(True)
                                return {
                                    'person_type': 'child',
                                    'name': self.child_names[idx],
                                    'confidence': 0.9,
                                    'bbox': bbox
                                }
            except Exception as e:
                logger.error(f"Face recognition error: {e}")
        
        # Default classification based on size
        return {
            'person_type': person_type,
            'name': 'Unknown',
            'confidence': 0.6,
            'bbox': bbox
        }
    
    def _is_face_in_bbox(self, face_loc: Tuple, bbox: List[int]) -> bool:
        """Check if face location is within person bbox"""
        top, right, bottom, left = face_loc
        x1, y1, x2, y2 = bbox
        return (left >= x1 and right <= x2 and top >= y1 and bottom <= y2)

import os

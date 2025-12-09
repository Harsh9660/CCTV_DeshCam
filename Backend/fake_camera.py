"""
Fake Camera Feed Generator - Creates realistic animated video frames for demo purposes
"""
import cv2
import numpy as np
import time
import random
from datetime import datetime
from typing import Tuple, List, Dict


class FakeCameraFeed:
    def __init__(self, width: int = 640, height: int = 480, fps: int = 30):
        self.width = width
        self.height = height
        self.fps = fps
        self.frame_count = 0
        
        # Simulated people (x, y, width, height, speed_x, speed_y, person_type)
        self.people = [
            {'x': 100, 'y': 200, 'w': 40, 'h': 80, 'vx': 1.5, 'vy': 0.5, 'type': 'child', 'color': (100, 200, 255)},
            {'x': 300, 'y': 250, 'w': 50, 'h': 100, 'vx': -1.0, 'vy': 0.3, 'type': 'staff', 'color': (100, 255, 100)},
            {'x': 450, 'y': 180, 'w': 35, 'h': 70, 'vx': 0.8, 'vy': -0.6, 'type': 'child', 'color': (100, 200, 255)},
        ]
        
        # Alert scenarios
        self.alert_probability = 0.02  # 2% chance per frame
        self.last_alert_time = time.time()
        
    def generate_background(self) -> np.ndarray:
        """Generate a playground-like background"""
        frame = np.ones((self.height, self.width, 3), dtype=np.uint8) * 40
        
        # Draw grass area (bottom half)
        cv2.rectangle(frame, (0, self.height//2), (self.width, self.height), (60, 120, 60), -1)
        
        # Draw sky area (top half)
        cv2.rectangle(frame, (0, 0), (self.width, self.height//2), (135, 180, 200), -1)
        
        # Draw playground equipment (simple rectangles)
        # Slide
        cv2.rectangle(frame, (50, 150), (120, 250), (180, 100, 100), -1)
        cv2.rectangle(frame, (50, 150), (120, 250), (150, 80, 80), 2)
        
        # Swing set
        cv2.line(frame, (200, 120), (200, 250), (100, 100, 100), 3)
        cv2.line(frame, (250, 120), (250, 250), (100, 100, 100), 3)
        cv2.line(frame, (200, 120), (250, 120), (100, 100, 100), 3)
        
        # Fence (background)
        for x in range(0, self.width, 30):
            cv2.line(frame, (x, self.height//2 - 50), (x, self.height//2 + 50), (139, 90, 60), 2)
        
        # Add some texture/noise for realism
        noise = np.random.randint(-10, 10, (self.height, self.width, 3), dtype=np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        return frame
    
    def update_people_positions(self):
        """Update positions of simulated people"""
        for person in self.people:
            # Update position
            person['x'] += person['vx']
            person['y'] += person['vy']
            
            # Bounce off walls
            if person['x'] <= 0 or person['x'] + person['w'] >= self.width:
                person['vx'] *= -1
            if person['y'] <= self.height//2 or person['y'] + person['h'] >= self.height:
                person['vy'] *= -1
            
            # Keep within bounds
            person['x'] = max(0, min(person['x'], self.width - person['w']))
            person['y'] = max(self.height//2, min(person['y'], self.height - person['h']))
    
    def draw_person(self, frame: np.ndarray, person: Dict) -> np.ndarray:
        """Draw a simulated person on the frame"""
        x, y, w, h = int(person['x']), int(person['y']), person['w'], person['h']
        color = person['color']
        
        # Draw body (rectangle)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
        
        # Draw head (circle)
        head_radius = w // 2
        head_center = (x + w//2, y - head_radius)
        cv2.circle(frame, head_center, head_radius, color, -1)
        
        # Draw outline
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
        cv2.circle(frame, head_center, head_radius, (255, 255, 255), 2)
        
        return frame
    
    def draw_detection_box(self, frame: np.ndarray, person: Dict, detected: bool = True) -> np.ndarray:
        """Draw detection bounding box around person"""
        if not detected:
            return frame
            
        x, y, w, h = int(person['x']), int(person['y']), person['w'], person['h']
        
        # Expand box to include head
        box_y = y - person['w']
        box_h = h + person['w']
        
        # Draw bounding box
        box_color = (0, 255, 0) if person['type'] == 'staff' else (255, 200, 0)
        cv2.rectangle(frame, (x - 5, box_y - 5), (x + w + 5, box_y + box_h + 5), box_color, 2)
        
        # Draw label
        label = f"{person['type'].upper()}"
        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
        cv2.rectangle(frame, (x - 5, box_y - 25), (x + label_size[0] + 5, box_y - 5), box_color, -1)
        cv2.putText(frame, label, (x, box_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        
        return frame
    
    def add_overlay_info(self, frame: np.ndarray) -> np.ndarray:
        """Add timestamp and zone information"""
        # Semi-transparent overlay at top
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (self.width, 40), (0, 0, 0), -1)
        frame = cv2.addWeighted(overlay, 0.6, frame, 0.4, 0)
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Zone label
        zone_text = "ZONE: Outdoor Play Area"
        cv2.putText(frame, zone_text, (self.width - 250, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Camera ID
        cam_text = "CAM-01"
        cv2.circle(frame, (self.width - 30, 20), 8, (255, 0, 0), -1)
        cv2.putText(frame, cam_text, (self.width - 80, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
        return frame
    
    def should_generate_alert(self) -> Tuple[bool, str]:
        """Determine if an alert should be generated"""
        # Don't generate alerts too frequently
        if time.time() - self.last_alert_time < 10:
            return False, ""
        
        if random.random() < self.alert_probability:
            self.last_alert_time = time.time()
            
            # Random alert type
            alert_types = [
                "Unsupervised Child Detected",
                "Restricted Area Entry",
                "Unusual Activity Detected",
                "Person Count Changed"
            ]
            return True, random.choice(alert_types)
        
        return False, ""
    
    def get_detections(self) -> List[Dict]:
        """Get current detection data"""
        detections = []
        for person in self.people:
            x, y, w, h = int(person['x']), int(person['y']), person['w'], person['h']
            box_y = y - person['w']
            box_h = h + person['w']
            
            detections.append({
                'type': person['type'],
                'bbox': [x - 5, box_y - 5, x + w + 5, box_y + box_h + 5],
                'confidence': random.uniform(0.85, 0.98)
            })
        
        return detections
    
    def generate_frame(self) -> Tuple[np.ndarray, List[Dict], Tuple[bool, str]]:
        """Generate a single frame with detections"""
        # Create background
        frame = self.generate_background()
        
        # Update and draw people
        self.update_people_positions()
        for person in self.people:
            frame = self.draw_person(frame, person)
            frame = self.draw_detection_box(frame, person, detected=True)
        
        # Add overlay information
        frame = self.add_overlay_info(frame)
        
        # Check for alerts
        alert_triggered, alert_message = self.should_generate_alert()
        
        # Get detection data
        detections = self.get_detections()
        
        self.frame_count += 1
        
        return frame, detections, (alert_triggered, alert_message)


if __name__ == "__main__":
    # Test the fake camera
    camera = FakeCameraFeed()
    
    print("Testing fake camera feed. Press 'q' to quit.")
    
    while True:
        frame, detections, (alert, msg) = camera.generate_frame()
        
        if alert:
            print(f"ALERT: {msg}")
        
        cv2.imshow("Fake Camera Feed", frame)
        
        if cv2.waitKey(33) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

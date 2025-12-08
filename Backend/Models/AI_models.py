import os
import cv2
import logging
from typing import List, Optional, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from ultralytics import YOLO
except ImportError:
    logger.error("ultralytics not found. Please install it using `pip install ultralytics`")
    YOLO = None

try:
    import face_recognition
except ImportError:
    logger.warning("face_recognition not found. Face recognition features will be disabled.")
    face_recognition = None

class CCTVSystem:
    def __init__(self, model_path: str = 'yolov8n.pt', known_faces_dir: Optional[str] = None):
        """
        Initialize the CCTV System with YOLO model and Face Recognition.
        
        Args:
            model_path (str): Path to the YOLO model file.
            known_faces_dir (str, optional): Directory containing images of known faces.
        """
        self.critical_classes = ['person', 'knife', 'gun', 'fire'] 
        self.model = self._load_yolo_model(model_path)
        self.known_face_encodings = []
        self.known_face_names = []
        
        if known_faces_dir and face_recognition:
            self._load_known_faces(known_faces_dir)

    def _load_yolo_model(self, model_path: str):
        if YOLO:
            try:
                logger.info(f"Loading YOLO model from {model_path}...")
                return YOLO(model_path)
            except Exception as e:
                logger.error(f"Failed to load YOLO model: {e}")
                return None
        return None

    def _load_known_faces(self, known_faces_dir: str):
        """Loads known face encodings from a directory."""
        if not os.path.exists(known_faces_dir):
            logger.warning(f"Known faces directory {known_faces_dir} does not exist.")
            return

        logger.info(f"Loading known faces from {known_faces_dir}...")
        for filename in os.listdir(known_faces_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                filepath = os.path.join(known_faces_dir, filename)
                try:
                    image = face_recognition.load_image_file(filepath)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        self.known_face_encodings.append(encodings[0])
                        self.known_face_names.append(os.path.splitext(filename)[0])
                except Exception as e:
                    logger.error(f"Error processing face image {filename}: {e}")

    def detect_objects(self, frame) -> List[Dict[str, Any]]:
        """
        Detects objects in a frame using YOLO.
        
        Returns:
            List of dictionaries containing detection details.
        """
        detections = []
        if self.model:
            results = self.model(frame, verbose=False)
            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = self.model.names[cls_id]
                    
                    if label in self.critical_classes:
                        detections.append({
                            'label': label,
                            'confidence': conf,
                            'bbox': box.xyxy[0].tolist()
                        })
        return detections

    def recognize_faces(self, frame) -> List[str]:
        """
        Recognizes faces in the frame.
        
        Returns:
            List of recognized names.
        """
        recognized_names = []
        if face_recognition and self.known_face_encodings:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                
                recognized_names.append(name)
        
        return recognized_names

    def trigger_alert(self, detection_type: str, details: str):
        """
        Triggers an alert (Email, SMS, Log).
        """
        logger.warning(f"ALERT TRIGGERED: {detection_type} - {details}")
        

    def process_frame(self, frame):
        """
        Process a single frame for object detection and face recognition.
        """
     
        detections = self.detect_objects(frame)
        for det in detections:
            self.trigger_alert("Critical Object Detected", f"{det['label']} ({det['confidence']:.2f})")
            
            x1, y1, x2, y2 = map(int, det['bbox'])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(frame, f"{det['label']} {det['confidence']:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        
        names = self.recognize_faces(frame)
        for name in names:
            if name == "Unknown":
                self.trigger_alert("Unknown Person", "Unrecognized face detected")
            else:
                logger.info(f"Recognized: {name}")

        return frame

if __name__ == "__main__":
    system = CCTVSystem()
    logger.info("CCTV System initialized. Run main.py to start processing.")
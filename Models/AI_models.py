import os
import cv2
import logging
from typing import List, Optional, Dict, Any, Tuple
from collections import deque
import config

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
    def __init__(
        self,
        model_path: str = config.YOLO_MODEL_PATH,
        known_faces_dir: Optional[str] = config.KNOWN_FACES_DIR,
        critical_classes: List[str] = config.CRITICAL_CLASSES,
        confidence_threshold: float = config.DETECTION_CONFIDENCE_THRESHOLD
    ):
        """
        Initialize the CCTV System with YOLO model and Face Recognition.
        
        Args:
            model_path (str): Path to the YOLO model file.
            known_faces_dir (str, optional): Directory containing images of known faces.
            critical_classes (List[str]): List of classes that trigger alerts.
            confidence_threshold (float): Minimum confidence for a valid detection.
        """
        self.critical_classes = critical_classes
        self.confidence_threshold = confidence_threshold
        self.model = self._load_yolo_model(model_path)
        self.known_face_encodings = []
        self.known_face_names = []
        self.alerts = deque(maxlen=100)  # Store last 100 alerts
        
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

    def detect_objects(self, frame: Any) -> List[Dict[str, Any]]:
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
                    
                    if conf >= self.confidence_threshold:
                        detections.append({
                            'label': label,
                            'confidence': conf,
                            'bbox': box.xyxy[0].tolist()
                        })
        return detections

    def recognize_faces(self, frame: Any, face_locations: List[Tuple[int, int, int, int]]) -> List[Dict[str, Any]]:
        """
        Recognizes faces within the given locations in the frame.
        
        Args:
            frame (Any): The image frame.
            face_locations (List): A list of bounding boxes (top, right, bottom, left) for faces.

        Returns:
            List of dictionaries with recognized name and location.
        """
        recognized_faces = []
        if face_recognition and self.known_face_encodings and face_locations:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                recognized_faces.append({'name': name, 'location': face_location})
        
        return recognized_faces

    def trigger_alert(self, event: str, details: str, camera: str = "Cam 01"):
        """
        Logs an alert and adds it to the alerts queue.
        """
        timestamp = logging.Formatter.converter.now().strftime('%Y-%m-%d %H:%M:%S')
        alert_message = f"ALERT: {event} - {details}"
        logger.warning(alert_message)
        self.alerts.appendleft({
            "time": timestamp,
            "camera": camera,
            "event": event,
            "details": details,
            "status": "Review"
        })

    def process_frame(self, frame: Any) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Process a single frame for object detection and face recognition.
        Returns structured data, does not draw on the frame.

        Returns:
            A tuple containing (object_detections, face_recognitions).
        """
        detections = self.detect_objects(frame)
        person_locations = []

        for det in detections:
            if det['label'] in self.critical_classes:
                self.trigger_alert("Critical Object", f"{det['label']} ({det['confidence']:.2f})")
            # Efficiently find persons to run face recognition on them
            if det['label'] == 'person':
                x1, y1, x2, y2 = map(int, det['bbox'])
                # face_recognition uses (top, right, bottom, left) format
                person_locations.append((y1, x2, y2, x1))

        recognized_faces = self.recognize_faces(frame, person_locations)
        for face in recognized_faces:
            if face['name'] == "Unknown":
                self.trigger_alert("Unknown Person", "Unrecognized face detected")
            else:
                logger.info(f"Recognized: {face['name']}")

        return detections, recognized_faces

    def draw_on_frame(self, frame: Any, detections: List[Dict], recognized_faces: List[Dict]) -> Any:
        """Draws detections and recognitions on a frame."""
        # Draw object detections
        for det in detections:
            x1, y1, x2, y2 = map(int, det['bbox'])
            color = (0, 0, 255) if det['label'] in self.critical_classes else (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{det['label']} {det['confidence']:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        # Draw face recognitions
        for face in recognized_faces:
            top, right, bottom, left = face['location']
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.putText(frame, face['name'], (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return frame

if __name__ == "__main__":
    system = CCTVSystem()
    logger.info("CCTV System initialized. Run batch_processor.py or Backend/main.py to start processing.")
import unittest
import numpy as np
import cv2
import os
from Models.AI_models import CCTVSystem
import config

class TestCCTVSystem(unittest.TestCase):
    
    def setUp(self):
        """Set up a test instance of the CCTVSystem."""
        self.system = CCTVSystem()
        
        self.dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    def test_initialization(self):
        """Test that the system initializes correctly."""
        self.assertIsNotNone(self.system)
        self.assertIsNotNone(self.system.model, "YOLO model should be loaded.")
        self.assertIsInstance(self.system.critical_classes, list)

    def test_detect_objects_dummy(self):
        """Test object detection on a dummy (black) frame."""
        detections = self.system.detect_objects(self.dummy_frame)
        self.assertIsInstance(detections, list)
        self.assertEqual(len(detections), 0)

    def test_process_frame_and_draw_no_crash(self):
        """Test that processing and drawing on a frame does not crash."""
        detections, faces = self.system.process_frame(self.dummy_frame)
        self.assertIsInstance(detections, list)
        self.assertIsInstance(faces, list)

        processed_frame = self.system.draw_on_frame(self.dummy_frame, detections, faces)
        self.assertIsNotNone(processed_frame)
        self.assertEqual(processed_frame.shape, self.dummy_frame.shape)

    def test_alerting_mechanism(self):
        """Test that alerts are triggered and stored correctly."""
        initial_alert_count = len(self.system.alerts)
       
        critical_detection = [{
            'label': 'person',
            'confidence': 0.9,
            'bbox': [10, 10, 50, 50]
        }]
        
        self.system.process_frame(self.dummy_frame) 
        self.system.alerts.clear()
        
        self.system.draw_on_frame(self.dummy_frame, critical_detection, [])
       
        original_detect = self.system.detect_objects
        self.system.detect_objects = lambda frame: critical_detection
        
        self.system.process_frame(self.dummy_frame)

        self.assertGreater(len(self.system.alerts), initial_alert_count)
        self.assertEqual(self.system.alerts[0]['event'], 'Critical Object')
        self.system.detect_objects = original_detect # restore original method

if __name__ == '__main__':
    unittest.main()

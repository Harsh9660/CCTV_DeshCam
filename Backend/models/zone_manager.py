"""
Zone Manager - Handles zone-based alert routing and scenario activation
"""
from typing import Dict, List
import config
from config import Zone, AlertSeverity
import logging

logger = logging.getLogger(__name__)

class ZoneManager:
    def __init__(self):
        self.active_scenarios = self._initialize_scenarios()
    
    def _initialize_scenarios(self) -> Dict[Zone, List[str]]:
        """Define which scenarios are active in each zone"""
        return {
            Zone.OUTDOOR_PLAY: [
                "fence_damage",
                "climbing_hazard",
                "unsupervised_child",
                "emergency_route_blocked",
                "unauthorized_adult",
            ],
            Zone.CLASSROOM: [
                "unsupervised_child",
                "restricted_area_entry",
                "unauthorized_adult",
                "uniform_violation",
            ],
            Zone.STAFF_ROOM: [
                "staff_location",
            ],
            Zone.HALLWAY: [
                "restricted_area_entry",
                "unauthorized_adult",
            ],
            Zone.ENTRANCE: [
                "unauthorized_adult",
            ],
        }
    
    def get_camera_zone(self, camera_id: int) -> Zone:
        """Get the zone for a given camera"""
        return config.CAMERA_ZONES.get(camera_id, Zone.OUTDOOR_PLAY)
    
    def is_scenario_active(self, zone: Zone, scenario: str) -> bool:
        """Check if a scenario is active in a given zone"""
        return scenario in self.active_scenarios.get(zone, [])
    
    def get_scenario_severity(self, scenario: str) -> AlertSeverity:
        """Get the severity level for a scenario"""
        return config.SCENARIO_SEVERITY.get(scenario, AlertSeverity.MEDIUM)
    
    def should_trigger_alert(self, zone: Zone, scenario: str, confidence: float) -> bool:
        """Determine if an alert should be triggered"""
        if not self.is_scenario_active(zone, scenario):
            return False
        
        # Critical scenarios have lower threshold
        severity = self.get_scenario_severity(scenario)
        if severity == AlertSeverity.CRITICAL:
            return confidence >= 0.5
        elif severity == AlertSeverity.HIGH:
            return confidence >= 0.6
        else:
            return confidence >= config.DETECTION_CONFIDENCE_THRESHOLD

zone_manager = ZoneManager()

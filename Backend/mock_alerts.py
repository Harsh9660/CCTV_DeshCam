"""
Mock Alert Generator - Creates realistic alert data for demo purposes
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict


class MockAlertGenerator:
    def __init__(self):
        self.scenarios = [
            {
                'scenario': 'unsupervised_child',
                'event': 'Unsupervised Child Detected',
                'severity': 'CRITICAL',
                'details': 'Child detected without staff supervision in play area',
                'zones': ['outdoor_play', 'classroom_a']
            },
            {
                'scenario': 'restricted_area_entry',
                'event': 'Restricted Area Entry',
                'severity': 'HIGH',
                'details': 'Unauthorized person entered staff-only area',
                'zones': ['staff_room', 'hallway']
            },
            {
                'scenario': 'fence_damage',
                'event': 'Fence Damage Detected',
                'severity': 'CRITICAL',
                'details': 'Potential breach in perimeter fence detected',
                'zones': ['outdoor_play', 'entrance']
            },
            {
                'scenario': 'climbing_hazard',
                'event': 'Climbing Hazard',
                'severity': 'HIGH',
                'details': 'Child detected near fence - potential climbing risk',
                'zones': ['outdoor_play']
            },
            {
                'scenario': 'emergency_route_blocked',
                'event': 'Emergency Route Blocked',
                'severity': 'CRITICAL',
                'details': 'Large object blocking emergency exit path',
                'zones': ['hallway', 'entrance']
            },
            {
                'scenario': 'uniform_violation',
                'event': 'Uniform Policy Violation',
                'severity': 'MEDIUM',
                'details': 'Staff member not wearing required uniform',
                'zones': ['classroom_a', 'outdoor_play']
            },
            {
                'scenario': 'unusual_activity',
                'event': 'Unusual Activity Detected',
                'severity': 'MEDIUM',
                'details': 'Unexpected movement pattern detected',
                'zones': ['outdoor_play', 'hallway']
            },
            {
                'scenario': 'person_count_change',
                'event': 'Person Count Changed',
                'severity': 'LOW',
                'details': 'Number of people in zone has changed',
                'zones': ['outdoor_play', 'classroom_a']
            }
        ]
        
        self.zone_names = {
            'outdoor_play': 'Outdoor Play Area',
            'classroom_a': 'Classroom A',
            'staff_room': 'Staff Room',
            'hallway': 'Main Hallway',
            'entrance': 'Main Entrance'
        }
    
    def generate_alert(self, scenario_type: str = None) -> Dict:
        """Generate a single mock alert"""
        if scenario_type:
            scenario = next((s for s in self.scenarios if s['scenario'] == scenario_type), None)
            if not scenario:
                scenario = random.choice(self.scenarios)
        else:
            scenario = random.choice(self.scenarios)
        
        zone_key = random.choice(scenario['zones'])
        
        alert = {
            'id': random.randint(1000, 9999),
            'timestamp': datetime.now().isoformat(),
            'camera': f'CAM-{random.randint(1, 4):02d}',
            'zone': self.zone_names[zone_key],
            'zone_key': zone_key,
            'scenario': scenario['scenario'],
            'event': scenario['event'],
            'severity': scenario['severity'].lower(),
            'details': scenario['details'],
            'status': random.choice(['active', 'acknowledged', 'resolved']),
            'confidence': round(random.uniform(0.75, 0.98), 2)
        }
        
        return alert
    
    def generate_historical_alerts(self, count: int = 50) -> List[Dict]:
        """Generate a list of historical alerts"""
        alerts = []
        base_time = datetime.now()
        
        for i in range(count):
            # Generate alerts going back in time
            time_offset = timedelta(minutes=random.randint(1, 1440))  # Up to 24 hours ago
            alert_time = base_time - time_offset
            
            scenario = random.choice(self.scenarios)
            zone_key = random.choice(scenario['zones'])
            
            alert = {
                'id': 1000 + i,
                'timestamp': alert_time.isoformat(),
                'camera': f'CAM-{random.randint(1, 4):02d}',
                'zone': self.zone_names[zone_key],
                'zone_key': zone_key,
                'scenario': scenario['scenario'],
                'event': scenario['event'],
                'severity': scenario['severity'].lower(),
                'details': scenario['details'],
                'status': random.choice(['active', 'acknowledged', 'resolved']),
                'confidence': round(random.uniform(0.75, 0.98), 2)
            }
            
            alerts.append(alert)
        
        # Sort by timestamp (newest first)
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return alerts
    
    def get_stats(self, alerts: List[Dict]) -> Dict:
        """Calculate statistics from alerts"""
        if not alerts:
            return {
                'total_alerts': 0,
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0,
                'active': 0,
                'resolved': 0
            }
        
        stats = {
            'total_alerts': len(alerts),
            'critical': sum(1 for a in alerts if a['severity'] == 'critical'),
            'high': sum(1 for a in alerts if a['severity'] == 'high'),
            'medium': sum(1 for a in alerts if a['severity'] == 'medium'),
            'low': sum(1 for a in alerts if a['severity'] == 'low'),
            'active': sum(1 for a in alerts if a['status'] == 'active'),
            'resolved': sum(1 for a in alerts if a['status'] == 'resolved')
        }
        
        return stats


if __name__ == "__main__":
    # Test the mock alert generator
    generator = MockAlertGenerator()
    
    print("Generating sample alerts...\n")
    
    # Generate a few random alerts
    for i in range(5):
        alert = generator.generate_alert()
        print(f"Alert {i+1}:")
        print(f"  Event: {alert['event']}")
        print(f"  Severity: {alert['severity'].upper()}")
        print(f"  Zone: {alert['zone']}")
        print(f"  Time: {alert['timestamp']}")
        print()
    
    # Generate historical alerts
    print("\nGenerating 20 historical alerts...")
    historical = generator.generate_historical_alerts(20)
    print(f"Generated {len(historical)} alerts")
    
    # Get stats
    stats = generator.get_stats(historical)
    print(f"\nStats: {stats}")

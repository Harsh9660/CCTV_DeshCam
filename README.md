# 🏫 Sparrow Childcare Safety Monitoring System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-FF0000?style=for-the-badge&logo=yolo&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **An AI-powered safety monitoring system specifically designed for childcare facilities**

Automatically detects and alerts on critical safety scenarios including fence damage, unsupervised children, unauthorized adults, staff compliance, and emergency route obstructions.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Safety Scenarios](#-safety-scenarios)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Privacy & Compliance](#-privacy--compliance)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The Sparrow Childcare Safety Monitoring System is a specialized AI surveillance platform designed to enhance safety and compliance in childcare facilities. Unlike generic CCTV systems, it focuses on childcare-specific scenarios and provides actionable alerts for staff and administrators.

### Key Capabilities

- **Zone-Based Monitoring**: Different safety checks for different areas (outdoor, classroom, staff room)
- **Multi-Model AI**: Specialized detectors for fences, people, uniforms, and hazards
- **Real-Time Alerts**: Instant notifications via WebSocket with severity levels
- **Persistent Storage**: All alerts and activity logs saved to database
- **Analytics Dashboard**: Heatmaps, activity tracking, and compliance reports

---

## 🚨 Safety Scenarios

### 🌳 Outdoor Play Area

#### 1. **Fence Damage Detection** (CRITICAL)
- **What**: Detects structural defects in boundary fencing
- **Classes**: HOLE, BENT, BROKEN, COLLAPSED
- **Model**: Custom YOLOv8 trained on [Roboflow fence dataset](https://universe.roboflow.com/iveia/broken-fence)
- **Alert Trigger**: Immediate alert when any critical defect is detected
- **Why**: Prevents children from escaping through damaged fencing

#### 2. **Climbing Hazard Alert** (HIGH)
- **What**: Identifies objects near fence that could be used as climbing aids
- **Detection**: Chairs, benches, tables, boxes near boundary
- **Model**: Standard YOLOv8 object detection
- **Alert Trigger**: Object detected within 50px of fence boundary
- **Why**: Prevents children from climbing over fences using equipment

#### 3. **Unsupervised Child** (CRITICAL)
- **What**: Detects children in outdoor area without staff supervision
- **Model**: YOLOv8 + FaceNet + Person Classification
- **Alert Trigger**: Child detected with no staff present in frame
- **Why**: Ensures children are always supervised outdoors

#### 4. **Emergency Route Obstruction** (CRITICAL)
- **What**: Monitors evacuation paths for blockages
- **Detection**: Large objects blocking gates or pathways
- **Model**: YOLOv8 with area-based filtering
- **Alert Trigger**: Object >10,000px² detected in emergency route
- **Why**: Ensures clear evacuation routes during emergencies

### 🏫 Classrooms

#### 5. **Unsupervised Child in Classroom** (CRITICAL)
- **What**: Child alone or sneaking back into unattended classroom
- **Model**: YOLOv8 + FaceNet + LSTM (temporal tracking)
- **Alert Trigger**: Child detected without educator for >30 seconds
- **Why**: Prevents accidents when children are alone

#### 6. **Restricted Area Entry** (HIGH)
- **What**: Children entering unauthorized areas (storerooms, hallways)
- **Model**: YOLOv8 + FaceNet + Zone awareness
- **Alert Trigger**: Child detected in restricted zone
- **Why**: Keeps children safe from hazardous areas

### 👥 All Areas

#### 7. **Unauthorized Adult** (CRITICAL)
- **What**: Unknown adult in facility without escort
- **Model**: YOLOv8 + FaceNet face recognition
- **Alert Trigger**: Adult face not in staff/visitor database
- **Why**: Prevents unauthorized access to children

#### 8. **Staff Location Tracking** (LOW)
- **What**: Logs educator presence in different zones
- **Model**: FaceNet + Time Logger
- **Purpose**: Audit staff ratios, attendance, incident investigation
- **Data**: Who was where and when, with duration tracking

#### 9. **Uniform Compliance** (MEDIUM)
- **What**: Verifies educators wearing Sparrow uniform
- **Model**: Custom YOLOv8 trained on uniform logo detection
- **Alert Trigger**: Educator detected without visible uniform logo
- **Why**: Professional appearance and easy identification

#### 10. **Activity Heatmaps** (ANALYTICS)
- **What**: Visualizes popular equipment and areas
- **Model**: YOLOv8 + OpenCV/NumPy heatmap generation
- **Purpose**: Facility improvement and space optimization
- **Output**: Visual heatmaps showing activity density over time

---

## ✨ Features

### Core Functionality
✅ **Zone-Based Monitoring**: Outdoor, Classroom, Staff Room, Hallway, Entrance  
✅ **Multi-Model AI Pipeline**: Specialized detectors for each scenario  
✅ **Real-Time WebSocket Alerts**: Instant notifications to connected clients  
✅ **Severity-Based Prioritization**: CRITICAL, HIGH, MEDIUM, LOW  
✅ **Persistent Database**: SQLite storage for all alerts and logs  
✅ **Face Recognition**: Staff and child identification (with consent)  

### Advanced Features
✅ **Activity Heatmaps**: Visualize facility usage patterns  
✅ **Staff Ratio Auditing**: Track educator-to-child ratios  
✅ **Temporal Analysis**: LSTM-based behavior tracking  
✅ **Export Reports**: CSV and PDF generation (planned)  
✅ **Dark Mode UI**: Modern, accessible interface  
✅ **Mobile Responsive**: Works on tablets and phones  

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core language |
| **FastAPI** | High-performance REST API |
| **Ultralytics YOLOv8** | Object detection |
| **FaceNet** | Face recognition |
| **OpenCV** | Image processing & heatmaps |
| **SQLAlchemy** | Database ORM |
| **WebSockets** | Real-time communication |
| **SQLite** | Data persistence |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React 18** | UI framework |
| **Vite** | Build tool |
| **Tailwind CSS** | Styling |
| **Recharts** | Data visualization |
| **React Hot Toast** | Notifications |
| **Lucide React** | Icons |
| **date-fns** | Date formatting |

### AI Models
| Model | Use Case |
|-------|----------|
| **YOLOv8 Small** | General object detection |
| **Custom Fence Model** | Fence defect classification |
| **FaceNet** | Staff/child identification |
| **Custom Uniform Model** | Sparrow uniform detection |

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Webcam or IP camera (for testing)

### Step 1: Clone Repository
```bash
git clone https://github.com/Harsh9660/CCTV_DeshCam.git
cd CCTV_DeshCam
```

### Step 2: Backend Setup
```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```bash
cd Frontend
npm install
cd ..
```

### Step 4: Database Initialization
```bash
cd Backend
python -c "from database import init_db; init_db()"
cd ..
```

---

## 🚀 Quick Start

### Option 1: One-Command Launch (Recommended)
```bash
./start.sh
```

### Option 2: Manual Launch

**Terminal 1 - Backend:**
```bash
source env/bin/activate
cd Backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Frontend:**
```bash
cd Frontend
npm run dev
```

### Access the Dashboard
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## ⚙️ Configuration

### Zone Setup

Edit `config.py` to map cameras to zones:

```python
CAMERA_ZONES = {
    0: Zone.OUTDOOR_PLAY,    # Camera 0 monitors outdoor area
    1: Zone.CLASSROOM,       # Camera 1 monitors classroom
    2: Zone.STAFF_ROOM,      # Camera 2 monitors staff room
    3: Zone.HALLWAY,         # Camera 3 monitors hallway
    4: Zone.ENTRANCE,        # Camera 4 monitors entrance
}
```

### Alert Severity Levels

```python
SCENARIO_SEVERITY = {
    "fence_damage": AlertSeverity.CRITICAL,
    "unsupervised_child": AlertSeverity.CRITICAL,
    "unauthorized_adult": AlertSeverity.CRITICAL,
    "emergency_route_blocked": AlertSeverity.CRITICAL,
    "climbing_hazard": AlertSeverity.HIGH,
    "restricted_area_entry": AlertSeverity.HIGH,
    "uniform_violation": AlertSeverity.MEDIUM,
    "staff_location": AlertSeverity.LOW,
}
```

### Face Recognition Setup

1. **Create directories:**
```bash
mkdir -p data/known_faces/staff
mkdir -p data/known_faces/children
```

2. **Add photos:**
- Staff: `data/known_faces/staff/john_doe.jpg`
- Children: `data/known_faces/children/child_name.jpg` (with parent consent)

3. **Photo requirements:**
- Clear, front-facing photos
- Good lighting
- One person per photo
- Filename = person's name

---

## 📖 Usage Guide

### Dashboard Navigation

1. **Dashboard Tab**: Overview with stats and recent alerts
2. **Live Feed Tab**: Real-time video streams from all cameras
3. **Analytics Tab**: Heatmaps and activity charts
4. **Alerts Tab**: Full alert history with filtering
5. **Settings Tab**: Configuration and preferences

### Alert Management

**Alert Severity Colors:**
- 🔴 **CRITICAL**: Red - Immediate action required
- 🟠 **HIGH**: Orange - Urgent attention needed
- 🟡 **MEDIUM**: Yellow - Should be addressed soon
- 🟢 **LOW**: Green - Informational

**Alert Actions:**
- Click alert to view details
- Mark as reviewed/resolved
- Export alert reports
- View associated video clip (if recording enabled)

### Heatmap Analysis

1. Navigate to **Analytics** tab
2. Select date range
3. Choose zone (Outdoor, Classroom, etc.)
4. View activity density heatmap
5. Identify popular areas for facility improvement

---

## 🔌 API Documentation

### REST Endpoints

#### Get System Stats
```http
GET /stats
```
**Response:**
```json
{
  "active_cameras": 4,
  "total_alerts": 127,
  "uptime": 86400
}
```

#### Get Alerts
```http
GET /alerts?zone=outdoor_play&severity=critical&limit=50
```
**Response:**
```json
[
  {
    "id": 1,
    "timestamp": "2025-12-08T12:30:00",
    "zone": "outdoor_play",
    "scenario": "fence_damage",
    "severity": "critical",
    "event": "Fence Defect: HOLE",
    "details": "Detected HOLE with 0.92 confidence",
    "status": "Review"
  }
]
```

#### Video Feed
```http
GET /video_feed?camera_id=0
```
**Response:** MJPEG stream

### WebSocket Endpoint

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const alert = JSON.parse(event.data);
  console.log('New alert:', alert);
};
```

---

## 📁 Project Structure

```
CCTV_Dashcam_project/
├── Backend/
│   ├── main.py                 # FastAPI application
│   ├── database.py             # Database models & ORM
│   ├── auth.py                 # JWT authentication
│   ├── websocket_manager.py    # WebSocket connections
│   ├── models/
│   │   ├── fence_detector.py   # Fence defect detection
│   │   ├── person_classifier.py # Staff/child classification
│   │   ├── uniform_detector.py # Uniform compliance
│   │   └── zone_manager.py     # Zone-based routing
│   ├── scenarios/
│   │   ├── fence_safety.py     # Fence monitoring logic
│   │   ├── child_safety.py     # Child safety scenarios
│   │   └── adult_monitoring.py # Adult detection logic
│   └── Models/
│       └── AI_models.py        # Legacy detection engine
├── Frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── components/         # UI components
│   │   └── index.css           # Tailwind styles
│   ├── package.json
│   └── vite.config.js
├── data/
│   ├── known_faces/
│   │   ├── staff/              # Staff photos
│   │   └── children/           # Child photos
│   └── training_images/        # Training data
├── config.py                   # Central configuration
├── requirements.txt            # Python dependencies
├── start.sh                    # Startup script
├── README.md                   # This file
└── LICENSE                     # MIT License
```

---

## 🔒 Privacy & Compliance

### Legal Requirements

This system processes personal data and biometric information. Ensure compliance with:

- ✅ **GDPR** (if in EU): Data protection regulations
- ✅ **CCPA** (if in California): Consumer privacy act
- ✅ **Local Privacy Laws**: Check your jurisdiction
- ✅ **Childcare Regulations**: Facility-specific requirements

### Required Consents

1. **Parent Consent**: Written permission for child face recognition
2. **Staff Consent**: Employee agreement for monitoring
3. **Visitor Notification**: Clear signage about surveillance
4. **Data Retention**: Define and enforce retention policies

### Data Protection

- 🔐 **Encryption**: All face encodings stored encrypted
- 🗑️ **Right to Deletion**: Ability to remove person data
- 📊 **Access Logs**: Track who accesses what data
- 🔒 **Authentication**: JWT-based API security

### Best Practices

1. **Minimize Data Collection**: Only collect necessary information
2. **Secure Storage**: Encrypt database and backups
3. **Access Control**: Role-based permissions
4. **Regular Audits**: Review data usage and compliance
5. **Transparency**: Clear privacy policy for parents

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript/React
- Write unit tests for new features
- Update documentation for API changes

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Roboflow**: Fence defect dataset
- **Ultralytics**: YOLOv8 framework
- **FastAPI**: Modern Python web framework
- **React Team**: UI library

---

## 📞 Support

For issues, questions, or feature requests:
- 📧 Email: support@sparrowchildcare.com
- 🐛 Issues: [GitHub Issues](https://github.com/Harsh9660/CCTV_DeshCam/issues)
- 📖 Docs: [Full Documentation](https://docs.sparrowchildcare.com)

---

**Made with ❤️ for safer childcare facilities**

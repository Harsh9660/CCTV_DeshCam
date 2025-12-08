# 🏫 Sparrow Childcare Safety Monitoring System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-FF0000?style=for-the-badge&logo=yolo&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An **AI-powered safety monitoring system** specifically designed for childcare facilities. Monitors critical safety scenarios including fence integrity, unsupervised children, unauthorized adults, and staff compliance.

---

## 🎯 Safety Scenarios

### 🚧 Outdoor Play Area
- **Fence Damage Detection**: Identifies HOLE, BENT, BROKEN, or COLLAPSED fence sections
- **Climbing Hazard Alert**: Detects objects near fence that children could use to climb
- **Unsupervised Child**: Alerts when children are in outdoor area without staff
- **Emergency Route**: Monitors for obstructions blocking evacuation paths

### 🏫 Classrooms
- **Unsupervised Child**: Detects children alone in unattended classrooms
- **Restricted Area Entry**: Alerts when children enter unauthorized areas
- **Unauthorized Adult**: Identifies unknown adults in the facility

### 👔 Staff Monitoring
- **Location Tracking**: Logs staff presence in different zones
- **Uniform Compliance**: Detects if educators are wearing Sparrow uniforms
- **Ratio Auditing**: Tracks staff-to-child ratios

### 📊 Analytics
- **Activity Heatmaps**: Visualizes popular areas and equipment
- **Usage Patterns**: Identifies most-used spaces for facility improvement

---

## 🛠️ Tech Stack

### AI Models
- **YOLOv8**: Object detection (people, furniture, hazards)
- **Custom Fence Model**: Trained on fence defect dataset
- **FaceNet**: Staff and child identification
- **OpenCV**: Heatmap generation and image processing

### Backend
- **FastAPI**: High-performance API
- **SQLAlchemy**: Database ORM
- **WebSockets**: Real-time alert streaming
- **SQLite**: Data persistence

### Frontend
- **React + Vite**: Modern UI
- **Tailwind CSS**: Styling
- **Recharts**: Data visualization
- **React Hot Toast**: Real-time notifications

---

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Harsh9660/CCTV_DeshCam.git
    cd CCTV_DeshCam
    ```

2.  **Setup Backend Environment**
    ```bash
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
    ```

3.  **Setup Frontend Dependencies**
    ```bash
    cd Frontend
    npm install
    cd ..
    ```

4.  **Configure Zones** (Optional)
    Edit `config.py` to map cameras to zones:
    ```python
    CAMERA_ZONES = {
        0: Zone.OUTDOOR_PLAY,
        1: Zone.CLASSROOM,
        2: Zone.STAFF_ROOM,
    }
    ```

## 🚦 Usage

### Quick Start
```bash
./start.sh
```

### Manual Start
**Backend:**
```bash
source env/bin/activate
cd Backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend:**
```bash
cd Frontend
npm run dev
```

Access the dashboard at `http://localhost:5173`

---

## ⚙️ Configuration

### Zone Setup
Define monitoring zones in `config.py`:
- `OUTDOOR_PLAY`: Outdoor play areas
- `CLASSROOM`: Indoor classrooms
- `STAFF_ROOM`: Staff-only areas
- `HALLWAY`: Corridors and passages
- `ENTRANCE`: Entry/exit points

### Alert Severity
- **CRITICAL**: Immediate action required (fence damage, unsupervised child)
- **HIGH**: Urgent attention (climbing hazard, restricted entry)
- **MEDIUM**: Should be addressed (uniform violation)
- **LOW**: Informational (staff location logs)

### Face Recognition
Add staff and child photos to:
- `data/known_faces/staff/` - Staff member photos
- `data/known_faces/children/` - Child photos (with parent consent)

---

## 📊 Features

✅ **Zone-Based Monitoring**: Different scenarios for different areas  
✅ **Multi-Model AI**: Specialized detectors for each scenario  
✅ **Real-Time Alerts**: Instant notifications via WebSocket  
✅ **Persistent Storage**: All alerts saved to database  
✅ **Activity Heatmaps**: Visualize facility usage patterns  
✅ **Staff Tracking**: Monitor educator locations and ratios  
✅ **Compliance Monitoring**: Uniform and safety checks  

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔒 Privacy & Compliance

This system is designed for childcare facility safety monitoring. Ensure compliance with:
- Local privacy laws
- Parent consent for child face recognition
- Data retention policies
- Staff notification requirements

**Note**: Always consult legal counsel before deploying surveillance systems in childcare facilities.

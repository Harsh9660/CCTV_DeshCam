# 📹 CCTV AI Dashcam System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![YOLOv8](https://img.shields.io/badge/YOLO-v8-FF0000?style=for-the-badge&logo=yolo&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

A state-of-the-art **AI-powered Surveillance System** that combines real-time object detection, face recognition, and a modern dashboard for monitoring. Built with performance and usability in mind.

---

## 🚀 Features

- **Real-time Object Detection**: Powered by **YOLOv8**, capable of detecting persons, weapons, fire, and more with high accuracy.
- **Face Recognition**: Identifies known individuals and alerts on unknown faces.
- **Live Video Streaming**: Low-latency MJPEG streaming from webcam or video files.
- **Interactive Dashboard**: A beautiful **React** frontend to view live feeds, system stats, and alerts.
- **Instant Alerts**: Logs critical events (e.g., weapon detected, unknown person) in real-time.
- **Easy Deployment**: One-click startup script for the entire stack.

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI**: High-performance web framework for building APIs.
- **Ultralytics YOLOv8**: SOTA object detection model.
- **OpenCV**: Image processing and video capture.
- **Face Recognition**: Dlib-based face recognition library.

### Frontend
- **React**: Modern UI library.
- **Vite**: Next-generation frontend tooling.
- **Tailwind CSS**: Utility-first CSS framework for stunning designs.

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

## 🚦 Usage

### The Easy Way (Recommended)
Simply run the startup script to launch both the Backend and Frontend:
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

Access the dashboard at `http://localhost:5173` (or the port shown in your terminal).

---

## ⚙️ Configuration

You can customize the system behavior in `config.py`:

- **`YOLO_MODEL_PATH`**: Path to your YOLO model (default: `yolov8n.pt`).
- **`KNOWN_FACES_DIR`**: Directory to store images of people you want the system to recognize.
- **`CRITICAL_CLASSES`**: List of objects that trigger alerts (e.g., `['person', 'knife', 'fire']`).
- **`CAMERA_INDEX`**: Camera source ID (default: `0` for webcam).

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

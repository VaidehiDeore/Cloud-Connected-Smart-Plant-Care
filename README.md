# 🌱 Cloud-Connected Smart Plant Care & Watering System

> An IoT-inspired smart plant monitoring and automated watering platform built with Python, FastAPI, React, SQLite, REST APIs, and virtual IoT sensor simulation.

**Built by:** Vaidehi Deore  
**Project Type:** IoT + Cloud Computing + Full-Stack Web Application  
**Hardware Required:** No  
**Status:** Working Virtual IoT Simulation

## 📌 Overview

The **Cloud-Connected Smart Plant Care & Watering System** monitors plant conditions and automates watering based on soil moisture levels.

A Python-based virtual IoT simulator generates sensor readings for soil moisture, temperature, humidity, and light. These readings are sent to the FastAPI backend through REST APIs, stored in the database, processed by the automation engine, and displayed through a modern React dashboard.

When soil moisture falls below the configured threshold, the system can automatically activate a virtual water pump. Users can also manually trigger watering from the dashboard.

The architecture is designed to be extended to real IoT hardware such as ESP32 and cloud services such as Firebase/Firestore.

## ✨ Key Features

- 🔐 JWT-based authentication
- 🌱 Virtual plant and device management
- 📡 Virtual IoT sensor simulation
- 💧 Soil moisture monitoring
- 🌡️ Temperature monitoring
- 💦 Humidity monitoring
- ☀️ Light-level monitoring
- 🤖 Automatic moisture-based watering
- 🚰 Manual Water Now control
- 🔄 Virtual pump simulation
- 🚨 Plant-health alerts
- 🔔 Alert acknowledgement
- 📶 Device online/offline monitoring
- 📊 Historical sensor analytics
- 📈 Sensor trend visualization
- 📝 Watering-event history
- ⚙️ Configurable moisture threshold
- 🧪 Automated backend testing
- ☁️ Cloud-ready architecture

## 🏗️ System Architecture

    Virtual Sensors
           ↓
    Python Simulator
           ↓
       REST / HTTP
           ↓
    FastAPI Backend
           ↓
    ┌──────┴──────┐
    ↓             ↓
  SQLite      Automation
  Database       Engine
                  ↓
            Virtual Pump
                  ↓
          React Dashboard

## 🔄 How It Works

    Virtual Sensor Simulation
              ↓
    Sensor Data Generated
              ↓
           REST API
              ↓
       FastAPI Backend
              ↓
       Database Storage
              ↓
    Moisture Threshold Check
              ↓
       ┌───────────────┐
       │               │
     Normal         Too Dry
       │               │
       │               ▼
       │         Virtual Pump
       │               │
       └───────┬───────┘
               ▼
     Dashboard + Alerts + Analytics

## 🛠️ Technology Stack

### Frontend
- React
- Vite
- JavaScript
- Axios
- Recharts
- Lucide React
- CSS

### Backend
- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- JWT
- Bcrypt

### Database
- SQLite
- SQLAlchemy ORM

### IoT Simulation
- Python
- REST/HTTP
- Virtual sensors
- Virtual pump

### Testing
- Pytest

### Development
- PowerShell
- Git
- GitHub

## 📂 Project Structure

    Cloud-Connected-Smart-Plant-Care/
    │
    ├── automation/
    ├── backend/
    ├── frontend/
    ├── sensor_simulator/
    ├── tests/
    ├── ss/
    │   ├── 01-login.png
    │   ├── 02-overview.png
    │   ├── 03-analytics.png
    │   ├── 04-alerts.png
    │   └── 05-simulator.png
    │
    ├── .env.example
    ├── .gitignore
    ├── README.md
    ├── requirements.txt
    ├── run_backend.ps1
    ├── run_simulator.ps1
    ├── START_HERE.md
    └── VERSION.txt

## 🚀 Getting Started

### Requirements

- Python 3.11+
- Node.js
- npm
- Git
- Windows PowerShell

### Clone the Repository

    git clone <YOUR_GITHUB_REPOSITORY_URL>
    cd Cloud-Connected-Smart-Plant-Care

### Create Virtual Environment

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

### Install Backend Dependencies

    pip install -r requirements.txt

### Configure Environment

Create `.env` from `.env.example` and configure the required values.

**Never commit `.env` to GitHub.**

## ▶️ Run the Project

### 1. Start Backend

    cd backend
    python -m uvicorn app:app --reload --port 8000

Backend:

`http://127.0.0.1:8000`

FastAPI documentation:

`http://127.0.0.1:8000/docs`

### 2. Start Sensor Simulator

Open another PowerShell window:

    cd sensor_simulator
    python simulator.py --url http://127.0.0.1:8000 --interval 5

### 3. Start Frontend

Open another PowerShell window:

    cd frontend
    npm install
    npm run dev

Open:

`http://localhost:5173`

## 📡 Sensor Data

Example virtual sensor payload:

    {
      "device_id": "PLANT-001",
      "soil_moisture": 34.69,
      "temperature": 26.75,
      "humidity": 59.48,
      "light_level": 94.94
    }

The backend receives and processes these readings through the sensor ingestion API.

## 🚨 Alerts & Monitoring

The system provides alerts for important plant and device conditions, including low soil moisture.

Users can:

- View active alerts
- Review alert information
- Acknowledge alerts
- Monitor device status

## 📊 Analytics

The dashboard provides historical information including:

- Soil moisture trends
- Temperature trends
- Humidity
- Sensor statistics
- Watering history

## 🔐 Security

The project includes:

- JWT authentication
- Password hashing
- Protected API endpoints
- Environment-based configuration
- `.env` protection
- Database exclusion from Git
- Private-key protection

Sensitive files are excluded through `.gitignore`.

## 🧪 Testing

Run:

    python -m pytest -q

Current test status:

    4 passed

## ☁️ Cloud-Ready Architecture

The current implementation runs locally using virtual IoT sensors while maintaining a cloud-ready architecture.

Potential future integrations:

- Firebase Authentication
- Firestore
- Firebase Hosting
- Cloud Run
- MQTT
- ESP32

These are future extension points and are not represented as completed features of the current local implementation.

## 🔮 Future Scope

- ESP32 hardware integration
- MQTT communication
- Firebase/Firestore integration
- Multiple plants and devices
- Water-reservoir monitoring
- Push notifications
- Email alerts
- Weather-aware watering
- Camera-based plant monitoring
- Machine-learning-based watering prediction
- Mobile application
- Full cloud deployment

## 📸 Project Screenshots

| Screenshot | Description |
|---|---|
| `01-login.png` | Authentication screen |
| `02-overview.png` | Main plant dashboard |
| `03-analytics.png` | Sensor analytics |
| `04-alerts.png` | Plant-health alerts |
| `05-simulator.png` | Virtual IoT simulator |

## 🎯 Industry Relevance

This project demonstrates practical skills in:

**IoT • Cloud Computing • Python • FastAPI • REST APIs • React • SQLite • Authentication • Automation • Data Analytics • System Architecture • Testing • Git/GitHub**

Potential application areas include:

- Smart agriculture
- Smart irrigation
- Greenhouse monitoring
- Indoor plant management
- Environmental monitoring

## 📌 Resume Description

**Cloud-Connected Smart Plant Care & Watering System**

Built an IoT-inspired plant monitoring and automated watering platform using Python, FastAPI, React, SQLite, JWT authentication, REST APIs, and virtual sensor simulation. Implemented sensor telemetry, moisture-based watering automation, virtual pump control, alerts, device monitoring, historical analytics, and a professional React dashboard with a cloud-ready architecture.

## 👩‍💻 Author

**Vaidehi Deore**

Cloud-Connected Smart Plant Care & Watering System

---

⭐ If you find this project useful, consider giving the repository a star.

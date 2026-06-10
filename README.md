# 🧠 Smart Productivity and Study Optimization AI System

> An IoT-based real-time work environment quality assessment system using Edge Machine Learning deployed on Arduino Nano 33 BLE Sense.

---

## 📌 Project Overview

This project monitors your workspace environment in real time and classifies it as **GOOD FOR WORK**, **MODERATE**, or **BAD FOR WORK** using a neural network model trained in Edge Impulse and deployed directly on an Arduino microcontroller — no cloud required.

The system reads four environmental parameters every 2 seconds, runs on-device inference, and streams results to a live web dashboard with colour-coded status indicators.

---

## 👥 Team Members

| Name | Role |
|------|------|
| Shaheer Khan | Project Lead & Embedded Developer |
| Fatiqa Munir | ML Model Training & Edge Impulse |
| Usama Sikandar | Dashboard & Serial Communication |

**Course:** Embedded AI

---

## 🔧 Hardware Used

- **Arduino Nano 33 BLE Sense**
- HS300x Sensor — Temperature & Humidity
- LPS22HB Sensor — Atmospheric Pressure
- PDM Microphone — Ambient Noise Level

---

## 📊 Input Features

| Feature | Sensor | Unit |
|---------|--------|------|
| Temperature | HS300x | °C |
| Humidity | HS300x | % |
| Pressure | LPS22HB | kPa |
| Noise Level | PDM Microphone | Raw Amplitude |

---

## 🤖 ML Model

- **Platform:** Edge Impulse
- **Model Type:** Fully Connected Neural Network (INT8 Quantized)
- **Training Labels:** 3 (normal, hot, noise)
- **Test Accuracy:** **87.4%**
- **Deployment:** Arduino Nano 33 BLE Sense (Cortex-M4)

| Metric | Training | Validation | Test |
|--------|----------|------------|------|
| Accuracy | 97.2% | 89.1% | **87.4%** |
| Precision | 96.8% | 88.7% | 86.9% |
| Recall | 97.0% | 89.3% | 87.1% |
| F1 Score | 96.9% | 89.0% | 87.0% |

---

## 🚦 Classification Logic

| Priority | Condition | Result |
|----------|-----------|--------|
| 1 | Raw noise > hardware threshold | 🔴 BAD — Too Noisy |
| 2 | Model predicts `hot` ≥ 70% confidence | 🔴 BAD — Too Hot |
| 3 | Model predicts `noise` ≥ 70% confidence | 🔴 BAD — Too Noisy |
| 4 | Model predicts `normal` ≥ 70% confidence | 🟢 GOOD FOR WORK |
| 5 | Confidence below 70% | 🟡 MODERATE |

---

## 🗂️ Project Structure

```
smart-productivity-ai/
│
├── README.md
├── arduino/
│   ├── environment_monitor.ino                  # Main Arduino sketch
│   └── shaheerkhan-project-1_inferencing.zip    # Edge Impulse model library
│
├── dashboard/
│   ├── arduino_server.py                        # Python serial-bridge server
│   └── dashboard.html                           # Live web dashboard
│
├── edge_impulse/
│   └── model_info.md                            # Model architecture & training details
│
└── report/
    └── Smart_Productivity_AI_Report.pdf
```

---

## 🚀 How to Run

### 1. Install the Model Library
- Open **Arduino IDE**
- Go to **Sketch → Include Library → Add .ZIP Library**
- Select `arduino/shaheerkhan-project-1_inferencing.zip`

### 2. Install Arduino Board Libraries
In Arduino IDE go to **Tools → Manage Libraries** and install:
- `Arduino_HS300x`
- `Arduino_LPS22HB`

### 3. Flash Arduino
- Open `arduino/environment_monitor.ino`
- Select board: **Arduino Nano 33 BLE Sense**
- Select correct COM port under **Tools → Port**
- Click **Upload**

### 4. Install Python Dependencies
```bash
pip install pyserial
```

### 5. Run the Dashboard Server
```bash
cd dashboard
python arduino_server.py
```

### 6. Open the Dashboard
Open your browser and go to:
```
http://localhost:5000
```

> ⚠️ Make sure Arduino IDE Serial Monitor is **closed** before running the server — both cannot use the same COM port simultaneously.

---

## 🖥️ Dashboard Features

- 🟢 🟡 🔴 Colour-coded environment status (GOOD / MODERATE / BAD)
- Live temperature, humidity, pressure, and noise readings
- ML model prediction label and confidence score
- Auto-refreshes every 2 seconds
- No internet connection required

---

## 📦 Requirements

| Tool | Version |
|------|---------|
| Arduino IDE | 2.x |
| Python | 3.8+ |
| pyserial | latest |

---

## 🔮 Future Work

- Expand dataset for better generalisation across all three labels
- Replace USB serial with wireless BLE transmission
- Mobile app with real-time push notifications
- Add temperature-humidity comfort index as a derived feature

---

## 📄 License

This project was developed for academic purposes as part of the Embedded AI course.

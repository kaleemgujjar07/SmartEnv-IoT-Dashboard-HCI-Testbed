# 🏢 IoT Building Monitor

A simulated smart-building sensor dashboard — live readings across multiple zones (temperature, energy, air quality, humidity), an alerts panel, and historical trend charts. Built specifically to double as the task environment for an HCI usability comparison (mouse vs. gesture-based interaction).

**🔗 Live demo:** https://smartenv-iot-dashboard-pevbox8zp4p9hhmf4sz4mj.streamlit.app

## Why this project covers two domains at once

1. **IoT**: realistic simulated sensor monitoring across zones, with anomaly detection and alerting — the core interface pattern of real IoT dashboards
2. **HCI**: the Alerts tab is a deliberately designed usability task (find and acknowledge every active alert, timed), used to compare interaction methods — specifically, a normal mouse vs. the [Virtual Mouse](https://github.com/kaleemgujjar07/Real-Time-Virtual-Mouse-HCI) gesture-control project. Since Virtual Mouse controls the real OS cursor, it works on this dashboard exactly as it works on any other on-screen application — no integration needed, just run both at once.

## Data note

Sensor readings are **simulated**, not from real hardware — connecting physical IoT sensors was out of scope for this timeline. Anomalies are injected with realistic, physically-plausible bounds (e.g., air quality index can't go negative). The dashboard's design and interaction logic — the actual point of this project — work identically whether the data source is real or simulated; swapping in a real sensor feed later is a natural extension.

## Features

- **Live Overview**: current readings across 5 zones × 4 metrics, with anomalies visually flagged
- **Alerts (usability task)**: timed task — acknowledge every active alert as quickly and accurately as possible; used for the mouse-vs-gesture comparison
- **History**: 24-hour trend charts per zone/metric

## Running locally

```bash
git clone https://github.com/kaleemgujjar07/SmartEnv-IoT-Dashboard-HCI-Testbed.git
cd SmartEnv-IoT-Dashboard
pip install -r requirements.txt
streamlit run app.py
```

To run the interaction comparison: open this dashboard in your browser, then separately run the Virtual Mouse script (`python gesture_app.py` from that project) to control the cursor via gestures instead of your physical mouse.

## Project structure

```
SmartEnv-IoT-Dashboard/
├── app.py                    # Streamlit dashboard
├── requirements.txt
└── src/
    └── sensor_simulator.py    # simulated sensor data generation

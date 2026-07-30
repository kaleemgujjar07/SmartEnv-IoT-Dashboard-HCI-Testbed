"""
sensor_simulator.py
Generates simulated live IoT sensor data -- temperature, energy usage,
air quality, and humidity across multiple rooms/zones. Includes
occasional anomalies (spikes/drops) so the dashboard has something
real to detect and surface to the user.

Honesty note: this is simulated data, not a real IoT deployment,
because building/connecting real sensors is out of scope for a
portfolio timeline. The dashboard UI and interaction design (the
actual HCI/IoT research question) work identically whether the data
is real or simulated -- the sensor source is a swappable component.
"""

import random
import time
from datetime import datetime, timedelta

random.seed()  # allow different randomness each run, unlike training-data generators

ZONES = ["Living Room", "Kitchen", "Bedroom", "Server Room", "Garage"]

METRICS = {
    "temperature": {"unit": "°C", "normal_range": (18, 26), "anomaly_chance": 0.05, "min_value": -10, "max_value": 45},
    "energy_usage": {"unit": "kWh", "normal_range": (0.5, 4.0), "anomaly_chance": 0.04, "min_value": 0, "max_value": 15},
    "air_quality": {"unit": "AQI", "normal_range": (10, 50), "anomaly_chance": 0.06, "min_value": 0, "max_value": 300},
    "humidity": {"unit": "%", "normal_range": (30, 60), "anomaly_chance": 0.03, "min_value": 0, "max_value": 100},
}


def generate_reading(metric_name: str, zone: str):
    """Generates one simulated sensor reading, occasionally injecting
    an anomaly (value far outside the normal range) so the dashboard
    has real alerts to display."""
    config = METRICS[metric_name]
    low, high = config["normal_range"]

    is_anomaly = random.random() < config["anomaly_chance"]
    if is_anomaly:
        # push the value well outside normal range in either direction,
        # but clamp to physically plausible bounds (e.g. AQI can't be negative)
        direction = random.choice([-1, 1])
        magnitude = random.uniform(1.5, 3.0)
        midpoint = (low + high) / 2
        span = (high - low) / 2
        value = midpoint + direction * span * magnitude
        value = max(config["min_value"], min(config["max_value"], value))
    else:
        value = random.uniform(low, high)

    return {
        "timestamp": datetime.now().isoformat(),
        "zone": zone,
        "metric": metric_name,
        "value": round(value, 1),
        "unit": config["unit"],
        "is_anomaly": is_anomaly,
        "normal_range": f"{low}-{high}",
    }


def generate_snapshot():
    """One reading per metric per zone -- a full snapshot of the
    simulated building's current sensor state."""
    readings = []
    for zone in ZONES:
        for metric in METRICS:
            readings.append(generate_reading(metric, zone))
    return readings


def generate_history(hours: int = 24, interval_minutes: int = 15):
    """Generates a historical time series for charting -- one zone,
    one metric at a time, at regular intervals going back `hours`."""
    now = datetime.now()
    n_points = int((hours * 60) / interval_minutes)
    history = {}

    for zone in ZONES:
        for metric in METRICS:
            key = f"{zone}_{metric}"
            points = []
            for i in range(n_points, 0, -1):
                t = now - timedelta(minutes=i * interval_minutes)
                config = METRICS[metric]
                low, high = config["normal_range"]
                is_anomaly = random.random() < config["anomaly_chance"]
                if is_anomaly:
                    direction = random.choice([-1, 1])
                    value = (low + high) / 2 + direction * (high - low)
                    value = max(config["min_value"], min(config["max_value"], value))
                else:
                    value = random.uniform(low, high)
                points.append({"timestamp": t.isoformat(), "value": round(value, 1), "is_anomaly": is_anomaly})
            history[key] = points

    return history

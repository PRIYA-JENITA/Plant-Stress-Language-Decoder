"""
Plant Stress Language Decoder - Backend API
Fetches real-time sensor data from Blynk, runs ELSA model inference,
and serves results to the frontend.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import pickle
import numpy as np
import os
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ─── Blynk Config (matches Arduino) ───────────────────────────────────────────
BLYNK_AUTH_TOKEN = "thA5Vc7-J4UzBeOhx43z2EDtSy5pT0cJ"
BLYNK_BASE_URL   = "https://blynk.cloud/external/api"

# Virtual pins
PIN_TEMPERATURE = "V0"
PIN_HUMIDITY    = "V1"
PIN_SOIL        = "V2"
PIN_RAIN        = "V3"

# ─── Load ELSA Model ──────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "elsa_model.pkl")
with open(MODEL_PATH, "rb") as f:
    model_data = pickle.load(f)

WEIGHTS = np.array(model_data["weights"])  # [temp, humidity, soil, rain]
MAX_SCORE = float(WEIGHTS.sum())


# ─── Blynk helpers ────────────────────────────────────────────────────────────
def fetch_blynk_pin(pin: str) -> float | None:
    url = f"{BLYNK_BASE_URL}/get?token={BLYNK_AUTH_TOKEN}&{pin}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        val = resp.json()
        if isinstance(val, list) and val:
            return float(val[0])
        return float(val)
    except Exception as e:
        print(f"[Blynk] Error reading {pin}: {e}")
        return None


# ─── ELSA Inference ───────────────────────────────────────────────────────────
def normalize_features(temp, humidity, soil, rain):
    """Normalize sensor readings to [0, 1] range."""
    temp_n    = max(0.0, min(1.0, (temp - 15.0) / 25.0))   # 15°C – 40°C
    hum_n     = max(0.0, min(1.0, humidity / 100.0))
    soil_n    = max(0.0, min(1.0, soil / 1023.0))
    rain_n    = float(rain)
    return np.array([temp_n, hum_n, soil_n, rain_n])


def classify_stress(score: float, max_score: float) -> dict:
    """Map weighted score to stress level, label, and treatment."""
    ratio = score / max_score  # 0..1

    if ratio < 0.30:
        return {
            "level": "CRITICAL",
            "label": "Severe Stress",
            "severity": 4,
            "color": "#ff2d2d",
            "description": "Plant is under severe stress. Immediate intervention required.",
            "treatment": [
                "🚨 Irrigate immediately – soil moisture critically low",
                "🌡️ Move plant to a shaded area if temperature > 38°C",
                "💧 Apply foliar spray to reduce heat stress",
                "🧪 Check for root rot if soil is waterlogged",
                "📋 Monitor every 30 minutes until values stabilize"
            ]
        }
    elif ratio < 0.50:
        return {
            "level": "HIGH",
            "label": "High Stress",
            "severity": 3,
            "color": "#ff7a00",
            "description": "Plant is showing signs of significant stress. Action needed soon.",
            "treatment": [
                "💧 Increase watering frequency – soil is drying out",
                "🌿 Ensure humidity is above 50% – use a humidifier if indoors",
                "🌡️ Maintain temperature between 20°C–30°C",
                "🧴 Apply a balanced NPK fertilizer (diluted)",
                "📅 Re-evaluate conditions within 6 hours"
            ]
        }
    elif ratio < 0.70:
        return {
            "level": "MODERATE",
            "label": "Moderate Stress",
            "severity": 2,
            "color": "#f5c518",
            "description": "Plant is experiencing mild stress. Monitor and adjust conditions.",
            "treatment": [
                "💦 Water if soil moisture is below 40%",
                "🌤️ Ensure adequate sunlight (6–8 hrs/day)",
                "🌬️ Improve airflow around the plant",
                "🧹 Check for early signs of pests or fungus",
                "📊 Log readings for trend analysis"
            ]
        }
    else:
        return {
            "level": "HEALTHY",
            "label": "Healthy",
            "severity": 1,
            "color": "#2ecc71",
            "description": "Plant is in good health. Maintain current conditions.",
            "treatment": [
                "✅ Continue current watering schedule",
                "🌱 Apply compost tea once a week for nutrients",
                "☀️ Maintain current light and temperature levels",
                "🔍 Routine inspection for pests every 3 days",
                "📝 Keep a plant journal to track long-term health"
            ]
        }


# ─── API Routes ───────────────────────────────────────────────────────────────
@app.route("/api/realtime", methods=["GET"])
def realtime():
    """Fetch live sensor data from Blynk and run ELSA model inference."""
    temp     = fetch_blynk_pin(PIN_TEMPERATURE)
    humidity = fetch_blynk_pin(PIN_HUMIDITY)
    soil     = fetch_blynk_pin(PIN_SOIL)
    rain_raw = fetch_blynk_pin(PIN_RAIN)

    # Fallback demo values if Blynk is unreachable
    if temp is None:     temp     = 27.5
    if humidity is None: humidity = 55.0
    if soil is None:     soil     = 420.0
    if rain_raw is None: rain_raw = 0.0

    rain = int(rain_raw)

    features = normalize_features(temp, humidity, soil, rain)
    score    = float(np.dot(WEIGHTS, features))

    stress   = classify_stress(score, MAX_SCORE)

    soil_pct = round((1 - soil / 1023) * 100, 1)  # higher analog = drier

    return jsonify({
        "timestamp": datetime.now().isoformat(),
        "sensors": {
            "temperature": round(temp, 1),
            "humidity":    round(humidity, 1),
            "soil_raw":    round(soil, 0),
            "soil_pct":    soil_pct,
            "rain":        rain,
            "rain_label":  "Detected" if rain == 1 else "None"
        },
        "model": {
            "score":     round(score, 4),
            "max_score": round(MAX_SCORE, 4),
            "ratio":     round(score / MAX_SCORE, 4),
            "weights":   WEIGHTS.tolist()
        },
        "stress": stress
    })


@app.route("/api/history", methods=["GET"])
def history():
    """Return last 20 readings (in-memory ring buffer)."""
    return jsonify({"readings": list(reading_buffer)})


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": True, "weights": WEIGHTS.tolist()})


# ─── Background logger (optional in-memory ring buffer) ──────────────────────
from collections import deque
import threading

reading_buffer = deque(maxlen=20)

def background_logger():
    """Log a reading every 10 seconds into the ring buffer."""
    while True:
        try:
            import urllib.request, json as _json
            url = "http://localhost:5000/api/realtime"
            with urllib.request.urlopen(url, timeout=6) as r:
                data = _json.loads(r.read())
                reading_buffer.append(data)
        except Exception:
            pass
        time.sleep(10)

logger_thread = threading.Thread(target=background_logger, daemon=True)
logger_thread.start()


if __name__ == "__main__":
    print("🌿 Plant Stress Language Decoder – Backend starting…")
    print(f"   ELSA weights loaded: {WEIGHTS}")
    app.run(host="0.0.0.0", port=5000, debug=True)

# ==============================
# AUSTIN SIGNAL SERVER (FRESH)
# Receives trading signals
# Works on Render
# ==============================

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# ---------------- CONFIG ----------------

SIGNAL_LOG = "signals.json"


# ---------------- DATABASE ----------------

def load_signals():
    if os.path.exists(SIGNAL_LOG):
        with open(SIGNAL_LOG, "r") as f:
            return json.load(f)
    return []

def save_signals(data):
    with open(SIGNAL_LOG, "w") as f:
        json.dump(data, f, indent=4)


# ---------------- HOME ROUTE ----------------
# This stops "Not Found" error on Render

@app.route("/", methods=["GET"])
def home():
    return "Austin Signal Server is LIVE"


# ---------------- SIGNAL RECEIVER ----------------
# TradingView / AI / Telegram will send signals here

@app.route("/signal", methods=["POST"])
def receive_signal():

    data = request.json

    if not data:
        return jsonify({"status": "error", "message": "No JSON received"}), 400

    required = ["pair", "direction", "timeframe", "strength"]

    if not all(field in data for field in required):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    signals = load_signals()
    signals.append(data)
    save_signals(signals)

    print("NEW SIGNAL RECEIVED:", data)

    return jsonify({"status": "success", "message": "Signal stored"}), 200


# ---------------- GET LAST SIGNAL ----------------
# Client bot will read this

@app.route("/latest", methods=["GET"])
def latest_signal():

    signals = load_signals()

    if not signals:
        return jsonify({"status": "empty"})

    return jsonify(signals[-1])


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    print("Starting Austin Signal Server...")

    # Render gives automatic port
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)

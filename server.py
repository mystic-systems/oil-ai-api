from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import numpy as np

app = Flask(__name__)
CORS(app)

# -------------------------
# PRICE (WTI OIL)
# -------------------------
def get_oil_price():
    data = yf.download("CL=F", period="1d", interval="5m", auto_adjust=True)
    return data["Close"].iloc[-1].item()

# -------------------------
# USD proxy
# -------------------------
def get_usd():
    data = yf.download("DX-Y.NYB", period="1d", interval="5m", auto_adjust=True)
    return data["Close"].iloc[-1].item()

# -------------------------
# SIMPLE AI MODEL
# -------------------------
def compute_signal(oil, usd):

    oil_momentum = (oil - 70) / 10      # normalizat
    usd_pressure = -(usd - 100) / 10
    

    score = oil_momentum + usd_pressure 

    score = max(-5, min(5, score))  # clamp

    prob = 1 / (1 + np.exp(-score))

    signal = "BUY" if score > 0 else "SELL"

    return score, prob, signal

# -------------------------
# API
# -------------------------
@app.route("/signal")
def signal():

    oil = get_oil_price()
    usd = get_usd()

    score, prob, sig = compute_signal(oil, usd)

    return jsonify({
        "oil_price": oil,
        "usd": usd,
        "score": round(score, 2),
        "probability": round(prob * 100, 1),
        "signal": sig
    })

if __name__ == "__main__":
    app.run(port=5000, debug=True)
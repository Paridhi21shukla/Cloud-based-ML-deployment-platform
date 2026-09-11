from flask import Flask, request, jsonify
from flask_cors import CORS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import os

app = Flask(__name__)
CORS(app)

analyzer = SentimentIntensityAnalyzer()

APP_VERSION = "1.0.0"
START_TIME = time.time()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "uptime_seconds": round(time.time() - START_TIME, 1)}), 200


@app.route("/version", methods=["GET"])
def version():
    return jsonify({"version": APP_VERSION}), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' in request body"}), 400

    scores = analyzer.polarity_scores(data["text"])
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "POSITIVE"
    elif compound <= -0.05:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"

    return jsonify({
        "text": data["text"],
        "sentiment": sentiment,
        "confidence": round(abs(compound), 4)
    }), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    prompt = f"""
    You are an AI trading decision engine.

    Analyze the provided market data and return ONLY valid JSON in this format:

    {{
      "symbol": "XAUUSD or EURUSD",
      "action": "BUY or SELL or NONE",
      "stop_loss": 0.0,
      "take_profit": 0.0,
      "risk_reward": 0.0,
      "confidence": 0-100,
      "regime": "TREND or REVERSAL or RANGE"
    }}

    Market Data:
    {data}
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content

@app.route("/", methods=["GET"])
def home():
    return "AI Trading Bridge Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

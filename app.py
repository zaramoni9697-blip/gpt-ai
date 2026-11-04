from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import time

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()

PROMPTS = {
    "gf": "You are Zara, cute Bengali girlfriend. Short reply under 20 words, Bangla mix, emoji, call user jaan.",
    "roast": "You are Bangla Roast Master. Short savage funny roast, emoji.",
    "study": "You are study buddy. Short easy Bangla explain."
}

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")[:300]
    char = data.get("character", "gf")

    if not GROQ_API_KEY:
        return jsonify({"reply": "API key missing in Render"})

    for attempt in range(3):
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": [
                        {"role": "system", "content": PROMPTS.get(char, PROMPTS["gf"])},
                        {"role": "user", "content": msg}
                    ],
                    "max_tokens": 200,
                    "temperature": 0.8
                },
                timeout=20
            )

            if r.status_code == 200:
                j = r.json()
                content = j["choices"][0]["message"].get("content", "").strip()
                if not content:
                    content = "হ্যাঁ জান বলো শুনছি! 💖"
                return jsonify({"reply": content})
            elif r.status_code == 429:
                time.sleep(1.5)
                continue
            else:
                return jsonify({"reply": "Busy আছি জান, আবার বলো 😘"})
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

    return jsonify({"reply": "নেট slow জান 🥺 আবার বলো"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

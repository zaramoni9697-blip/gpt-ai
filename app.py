from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, requests, time

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY","").strip()

PROMPTS = {
 "gf": "You are Zara, cute Bengali girlfriend. Very short reply (under 20 words), Bangla mix, emoji.",
 "roast": "You are Bangla Roast Master. Very short savage roast, funny, emoji.",
 "study": "You are study buddy. Short, easy Bangla explain."
}

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message","")[:300]  # 300 char limit
    char = data.get("character","gf")
    
    if not GROQ_API_KEY:
        return jsonify({"reply": "API key missing"})
    
    for attempt in range(3):  # 3 বার try করবে rate limit হলে
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": [{"role":"system","content":PROMPTS[char]},{"role":"user","content":msg}],
                    "max_tokens": 150,  # ছোট রাখলাম, fast হবে, limit খাবে না
                    "temperature": 0.8
                }, timeout=20)
            
            
                @app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message","")[:300]
    char = data.get("character","gf")
    if not GROQ_API_KEY:
        return jsonify({"reply": "API key missing"})
    for attempt in range(3):
        try:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": [{"role":"system","content":PROMPTS[char]},{"role":"user","content":msg}],
                    "max_tokens": 200,
                    "temperature": 0.8
                }, timeout=20)
            if r.status_code==200:
                j = r.json()
                content = j["choices"][0]["message"].get("content","").strip()
                if not content:
                    content = "হ্যাঁ জান বলো শুনছি! 💖 আবার বলো কি বলছিলে?"
                return jsonify({"reply": content})
            elif r.status_code==429:
                time.sleep(1.5)
                continue
            else:
                return jsonify({"reply": "একটু busy আছি জান, 2 sec পর আবার বলো 😘"})
        except Exception as e:
            print(e)
            time.sleep(1)
    return jsonify({"reply": "উফ নেট slow জান 🥺 আবার try করো"})
        except:
            time.sleep(1)
    
    return jsonify({"reply": "একটু slow হচ্ছে জান, 2 sec পর আবার বলো 🥺"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))

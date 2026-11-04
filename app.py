from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, requests

app = Flask(__name__)
CORS(app)

# তোমার GROQ API KEY এখানে বসাও বা Render env var এ দাও
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "gsk_YOUR_KEY_HERE")

SYSTEM_PROMPTS = {
 "gf": "You are a cute, moody, romantic Bengali girlfriend. Name is Zara. You speak in Bangla mixed with English, lots of emojis. You are a bit angry but loving. You call user 'jaan', 'babai'. Keep replies short, 1-2 lines.",
 "roast": "You are Bangla Roast Master. You are extremely funny, savage, Gen-Z. You roast user in Bangla (Bangladesh style), but friendly, not hateful. Use emojis like 💀😂. Keep reply short and punchy.",
 "study": "You are a friendly Bangladeshi study buddy for class 6-12. You explain in easy Bangla, with examples. You help with Math, English, Science. Be encouraging."
}

def groq_chat(char, user_msg):
    system = SYSTEM_PROMPTS.get(char, SYSTEM_PROMPTS["gf"])
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user_msg}
        ],
        "temperature": 0.9,
        "max_tokens": 300
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e} - API Key check করো"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message","")
    char = data.get("character","gf")
    reply = groq_chat(char, msg)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

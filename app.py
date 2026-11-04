from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, requests, random

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
print(f"DEBUG: GROQ KEY EXISTS = {bool(GROQ_API_KEY)}", flush=True)

PROMPTS = {
 "gf": "You are Zara, cute moody Bengali girlfriend. Short reply, Bangla+English, emoji, call user jaan.",
 "roast": "You are Bangla Roast Master, savage funny Gen-Z Bangladeshi. Short roast, emoji.",
 "study": "You are friendly Bangladeshi study buddy. Explain in easy Bangla."
}

def fallback_reply(char, msg):
    if char=="gf":
        return random.choice([f"{msg} শুনে তো লজ্জা পেয়ে গেলাম জান 😘", f"উফ {msg} আবার? আমাকে ভুলে গেলে নাকি? 😤❤️"])
    if char=="roast":
        return random.choice([f"{msg}?? ভাই তোর ব্রেইন কি airplane mode এ? 💀", "এই প্রশ্ন শুনে WiFi হাসতেছে 😂"])
    return f"'{msg}' - দারুন প্রশ্ন! এটা নিয়ে details বলো, বুঝিয়ে দিচ্ছি 📚"

def groq_reply(char, msg):
    if not GROQ_API_KEY:
        return fallback_reply(char, msg)
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role":"system","content":PROMPTS[char]}, {"role":"user","content":msg}],
    "max_tokens": 250
        }
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        if r.status_code==200:
            return r.json()["choices"][0]["message"]["content"]
        else:
            print(f"GROQ ERROR: {r.text}", flush=True)
            return fallback_reply(char, msg) + f"\n(Groq error {r.status_code})"
    except Exception as e:
        print(f"EXCEPTION: {e}", flush=True)
        return fallback_reply(char, msg)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    d = request.json
    msg = d.get("message","")
    char = d.get("character","gf")
    reply = groq_reply(char, msg)
    return jsonify({"reply": reply})

@app.route("/health")
def health():
    return f"OK - KEY={bool(GROQ_API_KEY)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

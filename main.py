from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # môžeš nechať ako je
        "X-Title": "KickBotAI"
    }

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return jsonify({"response": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

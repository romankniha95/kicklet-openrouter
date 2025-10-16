from flask import Flask, request, jsonify
import requests
import os
import datetime

app = Flask(__name__)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "KickBotAI"
    }

    # Dnešný dátum pre systémovú správu
    today = datetime.datetime.now().strftime("%d.%m.%Y")

    payload = {
        "model": "openai/gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": f"Si užitočný, vtipný a stručný slovenský chatbot. Odpovedaj vždy po slovensky. Dnešný dátum je {today}. Odpovede nepresahujú 950 znakov."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "max_tokens": 1000,  # bezpečnostné nastavenie – max tokens
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]

        # Skráť odpoveď na max. 950 znakov (bez useknutia slova)
        if len(content) > 950:
            content = content[:947].rsplit(" ", 1)[0] + "..."

        return jsonify({"response": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask štart
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

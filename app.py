from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

REFERER_URL = "https://yourdomain.com"  # поменяй на свой домен
SITE_TITLE = "AI Объявления"

PROMPT_TEMPLATE = """
Ты опытный маркетолог и копирайтер. Преобразуй этот текст в продающее объявление, используя техники Игоря Манна, триггеры выгоды, эмоции, ограниченность. Добавь рекомендации по улучшению фотографий.
Вот описание от пользователя: "{}"
"""

def generate_ai_response(user_input):
    prompt = PROMPT_TEMPLATE.format(user_input)

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": REFERER_URL,
        "X-Title": SITE_TITLE,
    }

    payload = {
        "model": "meta-llama/llama-3.1-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Ошибка {response.status_code}: {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form["user_input"]
        result = generate_ai_response(user_input)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

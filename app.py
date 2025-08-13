from flask import Flask, render_template, request
import requests
import json
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
REFERER_URL = "https://yourdomain.com"  # замените на свой домен
SITE_TITLE = "AI-Obyavleniya"

PROMPT_TEMPLATE = """
Ты опытный маркетолог и копирайтер.
Преобразуй этот текст в продающее объявление, используя техники Игоря Манна, триггеры выгоды, эмоции, ограниченность.
Добавь рекомендации по улучшению фотографий.
Весь текст объявления должен быть компактным — не более 250-300 символов.
Вот описание от пользователя: "{}"
"""

MAX_INPUT_LENGTH = 500
MAX_OUTPUT_LENGTH = 500

def generate_ai_response(user_input: str) -> str:
    if not OPENROUTER_API_KEY:
        return "❌ Ошибка: API-ключ не задан. Добавьте OPENROUTER_API_KEY в переменные окружения."

    if not user_input.strip():
        return "⚠️ Пожалуйста, введите описание товара."

    if len(user_input) > MAX_INPUT_LENGTH:
        return f"⚠️ Описание слишком длинное. Максимум {MAX_INPUT_LENGTH} символов."

    prompt = PROMPT_TEMPLATE.format(user_input.strip())

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

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        data = response.json()
    except requests.RequestException as e:
        return f"❌ Ошибка сети: {e}"
    except json.JSONDecodeError:
        return f"❌ API вернул некорректный JSON: {response.text}"

    if "choices" in data and data["choices"]:
        result_text = data["choices"][0]["message"]["content"].strip()
        if len(result_text) > MAX_OUTPUT_LENGTH:
            result_text = result_text[:MAX_OUTPUT_LENGTH - 3] + "..."
        return result_text
    elif "error" in data:
        return f"❌ Ошибка API: {data['error']}"
    else:
        return f"❌ Неожиданный ответ API: {data}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        result = generate_ai_response(user_input)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)

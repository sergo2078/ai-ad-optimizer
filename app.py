import os
import openai
from flask import Flask, request, jsonify, send_from_directory

openai.api_key = os.getenv("KIMI_API_KEY")
openai.api_base = "https://api.moonshot.cn/v1"

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text", "")
    prompt = f"""
Ты профессиональный маркетолог, эксперт по продаже на Авито. Используя техники Игоря Манна, дай краткие советы (не более 200 слов):
1. Проблемы текста и лучший вариант текста.
2. Улучшенный вариант заголовка.
3. Что сделать с фото.
Новый текст объявления: {text}
"""
    resp = openai.ChatCompletion.create(
        model="moonshot-v1-8k",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )
    advice = resp["choices"][0]["message"]["content"]
    return jsonify({"advice": advice.replace("\n", "<br>")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

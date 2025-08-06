import os
import openai  # можно оставить openai-библиотеку

openai.api_key = os.getenv("KIMI_API_KEY")
openai.api_base = "https://api.moonshot.cn/v1"   # ← новый endpoint

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text", "")
    prompt = f"""
Ты профессиональный маркетолог, эксперт по продаже на Авито. Используя техники Игоря Манна Дай краткие советы (не более 200 слов):
1. Проблемы текста. Лучший вариант текста.
2. Улучшенный вариант заголовка.
3. Что сделать с фото.
Новый кекст объявления: {text}
"""
   resp = openai.ChatCompletion.create(
    model="moonshot-v1-8k",   # или moonshot-v1-32k
    messages=[{"role": "user", "content": prompt}],
    max_tokens=400,
    temperature=0.7
)
    advice = resp["choices"][0]["message"]["content"]
    return jsonify({"advice": advice.replace("\n", "<br>")})

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
# новый маршрут
from flask import send_from_directory

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


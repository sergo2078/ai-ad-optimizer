from flask import Flask, request, jsonify
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def analyze():
    text = request.json.get("text", "")
    prompt = f"""
Ты эксперт по продаже на Авито. Дай краткие советы (не более 200 слов):
1. Проблемы текста.
2. Улучшенный вариант заголовка.
3. Что сделать с фото.
Текст объявления: {text}
"""
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400,
        temperature=0.7
    )
    advice = resp["choices"][0]["message"]["content"]
    return jsonify({"advice": advice.replace("\n", "<br>")})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
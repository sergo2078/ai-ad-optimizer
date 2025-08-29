from flask import Flask, render_template, request
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env для локальной разработки
load_dotenv()

app = Flask(__name__)

# Настраиваем API-ключ Google
# На Render его нужно будет добавить в Environment Variables под именем GOOGLE_API_KEY
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # Эта ошибка будет видна при запуске, если ключ не найден
    print("❌ Ошибка: GOOGLE_API_KEY не найден. Убедитесь, что он задан в переменных окружения.")


# Обновленный промпт с фокусом на краткость и советы по фото
PROMPT_TEMPLATE = """
Ты — профессиональный копирайтер, который создает короткие и эффективные объявления для Avito.

Твоя задача — на основе данных от пользователя создать продающее объявление и дать советы по фото.

**Правила для объявления:**
1.  **Заголовок:** До 50 символов. Яркий, с ключевым словом. Без восклицательных знаков.
2.  **Цена:** Укажи как есть.
3.  **Описание:** Строго до 250 символов.
    * Один-два коротких абзаца.
    * Первый абзац — ключевая выгода.
    * Второй — характеристики и призыв к действию.
    * Используй 1-2 эмодзи для акцентов.
    * Не используй слова «б/у», «старый». Заменяй на «в отличном состоянии», «надежный».
4.  **Хэштеги:** 3-4 релевантных хэштега в конце.

**Правила для советов по фото:**
* Дай 2-3 коротких, но полезных совета, как лучше сфотографировать именно этот товар.

**Формат вывода (строго соблюдай его):**

**Заголовок:** <текст заголовка>
**Цена:** <цена> руб.

**Описание:**
<текст описания>

#<хэштег1> #<хэштег2> #<хэштег3>

---
**💡 Советы по фото:**
* <Совет 1>
* <Совет 2>

**Входные данные от пользователя:** "{}"
"""

MAX_INPUT_LENGTH = 500

def generate_ai_response(user_input: str) -> str:
    """
    Генерирует ответ от Google Gemini API с обработкой ошибок.
    """
    if not api_key:
        return "❌ Ошибка: API-ключ для Google не настроен. Проверьте переменные окружения на сервере."

    if not user_input.strip():
        return "⚠️ Пожалуйста, введите описание вашего товара."

    if len(user_input) > MAX_INPUT_LENGTH:
        return f"⚠️ Ваше описание слишком длинное. Максимальная длина — {MAX_INPUT_LENGTH} символов."

    prompt = PROMPT_TEMPLATE.format(user_input.strip())

    try:
        # Инициализируем модель
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Генерируем контент
        response = model.generate_content(prompt)
        
        # Возвращаем текст ответа
        return response.text.strip()

    except Exception as e:
        # Обработка общих ошибок API
        return f"❌ Произошла ошибка при обращении к Gemini API: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    # Инициализируем user_input здесь, чтобы она всегда существовала
    user_input = "" 
    
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        result = generate_ai_response(user_input)
        
    # Теперь эта строка будет работать и для GET, и для POST запросов
    return render_template("index.html", result=result, user_input=user_input)


if __name__ == "__main__":
    # debug=False лучше для продакшена, но для локальной отладки True удобнее
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

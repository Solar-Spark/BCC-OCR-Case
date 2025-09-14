import os
import json
from docx import Document
from dotenv import load_dotenv
import google.generativeai as genai

# 🔑 Загружаем токен из .env
load_dotenv()
token = os.getenv("GEMINI_API_KEY")
if not token:
    raise ValueError("❌ Не найден GEMINI_API_KEY в .env")

# ⚙️ Настройка клиента Gemini
genai.configure(api_key=token)
model = genai.GenerativeModel("gemini-1.5-flash")  # можно "gemini-1.5-pro"

# 📑 читаем docx
def load_docx_text(path: str, max_chars: int = 14000) -> str:
    doc = Document(path)
    text = "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    return text[:max_chars]

contract_text = load_docx_text("8A16.ocr (1).docx")

# 🎯 JSON Schema (как словарь)
schema = {
    "type": "object",
    "properties": {
        "contract_number": {"type": "string"},
        "contract_date": {"type": "string", "description": "Дата заключения в формате YYYY-MM-DD"},
        "end_date": {"type": "string", "description": "Дата окончания в формате YYYY-MM-DD"},
        "counterparty": {"type": "string"},
        "country": {"type": "string"},
        "amount": {"type": "string", "description": "Сумма и валюта, например: '100000000 российские рубли'"},
        "contract_currency": {"type": "string"},
        "payment_currency": {"type": "string"},
    },
    "required": [
        "contract_number",
        "contract_date",
        "end_date",
        "counterparty",
        "country",
        "amount",
        "contract_currency",
        "payment_currency",
    ]
}


# 🚀 Запрос к Gemini
response = model.generate_content(
    contents=f"""
Ты — помощник для извлечения реквизитов договора.
Заполни все поля строго по тексту договора.

Извлеки из текста договора следующие данные:
- № контракта
- дата заключения (YYYY-MM-DD)
- дата окончания (YYYY-MM-DD)
- контрагент
- страна контрагента
- сумма договора (число и валюта, например: "100000000 российские рубли")
- валюта контракта
- валюта платежа

Текст договора:
{contract_text}
""",
    generation_config=genai.GenerationConfig(
        response_schema=schema,
        response_mime_type="application/json",
    ),
)

# 📝 structured output → JSON
result_json = json.loads(response.text)

print("\n=== Ответ модели ===")
print(json.dumps(result_json, ensure_ascii=False, indent=2))

# 💾 сохраняем
with open("contract_gemini.json", "w", encoding="utf-8") as f:
    json.dump(result_json, f, ensure_ascii=False, indent=2)

print("✅ JSON сохранен в contract_gemini.json")

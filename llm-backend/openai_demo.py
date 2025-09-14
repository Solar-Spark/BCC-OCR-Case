import os
import json
from docx import Document
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

# 🔑 Загружаем токен из .env
load_dotenv()
token = os.getenv("GITHUB_API_KEY")
if not token:
    raise ValueError("Не найден GITHUB_API_KEY в .env")

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4o-mini" 

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

def load_docx_text(path: str) -> str:
    doc = Document(path)
    text = "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    return text

contract_text = load_docx_text("8A16.ocr(1).docx")

examples = """
Пример:
Текст: "Контракт №12345 заключён 12 апреля 2024 года между ОАО БМЗ и ТОО «АзияМетизКомплект». 
Договор действует до 31 декабря 2025 года. 
Сумма договора 100 000 000 российских рублей. 
Валюта договора и платежа — российские рубли."
JSON:
{{
  "contract_number": "12345",
  "contract_date": "2024-04-12",
  "end_date": "2025-12-31",
  "counterparty": "ОАО БМЗ",
  "country": "Республика Беларусь",
  "amount": "100000000 российские рубли",
  "contract_currency": "российские рубли",
  "payment_currency": "российские рубли"
}}
"""

# 🚀 запрос в LLM
response = client.complete(
    model=model,
    messages=[
        SystemMessage(
            f"""Ты — помощник для извлечения реквизитов договора.
Отвечай строго в формате JSON и заполняй все поля точно по тексту договора.
Правила:
- Даты всегда в формате ГГГГ-ММ-ДД (например: 2024-04-12).
- Сумму извлекай только как число с указанием валюты (например: "100000000 российские рубли").
- Валюта контракта и валюта платежа должны быть явно названы ("российские рубли", "доллары США"), а не "валюта договора".
- Контрагента указывай полностью, без сокращений или выдуманных данных.

{examples}
"""
        ),
        UserMessage(
            f"""Извлеки из текста договора и заполни следующие поля:
- № контракта
- дата заключения договора (формат: YYYY-MM-DD)
- дата окончания договора (формат: YYYY-MM-DD)
- контрагент (полное название)
- страна контрагента
- сумма контракта (только число и валюта, например: "100000000 российские рубли")
- валюта контракта (например: "российские рубли")
- валюта платежа (например: "российские рубли")

Текст договора:
{contract_text}
"""
        )
    ],
    temperature=0.2,
    top_p=1.0,
)

result_text = response.choices[0].message.content
print("\n=== Ответ модели ===")
print(result_text)

try:
    result_json = json.loads(result_text)
    with open("contract_openai4omini.json", "w", encoding="utf-8") as f:
        json.dump(result_json, f, ensure_ascii=False, indent=2)
    print("✅ JSON сохранен в contract_openai.json")
except Exception as e:
    print("⚠️ Ошибка при сохранении JSON:", e)

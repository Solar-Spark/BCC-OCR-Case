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
    raise ValueError("❌ Не найден GITHUB_API_KEY в .env")

endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

# 📑 читаем docx (обрезаем по символам, чтобы не перегружать модель)
def load_docx_text(path: str, max_chars: int = 14000) -> str:
    doc = Document(path)
    text = "\n".join([para.text.strip() for para in doc.paragraphs if para.text.strip()])
    return text[:max_chars]

contract_text = load_docx_text("8A16.ocr (1).docx")

# 🎯 JSON Schema для structured output
schema = {
    "name": "ContractInfo",
    "schema": {
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
            "payment_currency"
        ],
        "additionalProperties": False
    }
}

# 🚀 запрос в LLM c structured outputs
response = client.complete(
    model=model,
    messages=[
        SystemMessage(
            """Ты — помощник для извлечения реквизитов договора.
Заполни все поля строго по тексту договора.
"""
        ),
        UserMessage(
            f"""Извлеки из текста договора следующие данные:
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
"""
        )
    ],
    temperature=0.2,
    top_p=1.0,
    response_format={
        "type": "json_schema",
        "json_schema": schema
    }
)

# 📝 structured output уже гарантированно JSON
result_json = response.choices[0].message.parsed

print("\n=== Ответ модели ===")
print(json.dumps(result_json, ensure_ascii=False, indent=2))

# 💾 сохраняем
with open("contract_deepseek.json", "w", encoding="utf-8") as f:
    json.dump(result_json, f, ensure_ascii=False, indent=2)

print("✅ JSON сохранен в contract_deepseek.json")

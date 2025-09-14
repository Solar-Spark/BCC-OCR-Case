import os
import json
from dotenv import load_dotenv
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential

load_dotenv()
token = os.getenv("GITHUB_API_KEY")
if not token:
    raise ValueError("❌ Не найден GITHUB_API_KEY в .env")

endpoint = "https://models.github.ai/inference"
model = "openai/gpt-4o-mini"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
)

examples = """
Пример:
Текст: "Контракт №12345 заключён 12 апреля 2024 года между ОАО БМЗ и ТОО «АзияМетизКомплект». 
Договор действует до 31 декабря 2025 года. 
Сумма договора 100 000 000 российских рублей. 
Валюта договора и платежа — российские рубли."
JSON:
{
  "contract_number": "12345",
  "contract_date": "2024-04-12",
  "end_date": "2025-12-31",
  "counterparty": "ОАО БМЗ",
  "country": "Республика Беларусь",
  "amount": "100000000 российские рубли",
  "contract_currency": "российские рубли",
  "payment_currency": "российские рубли"
}
"""

def extract_contract_json(text: str) -> dict:
    """
    Extract structured contract data from any text input.
    
    Args:
        text (str): Contract text to extract info from.
    
    Returns:
        dict: JSON with extracted fields.
    """
    response = client.complete(
        model=model,
        messages=[
            SystemMessage(
                f"""Ты — помощник для извлечения реквизитов договора.
Отвечай строго в формате JSON и заполняй все поля точно по тексту договора.
Правила:
- Даты всегда в формате ГГГГ-ММ-ДД.
- Сумму извлекай только как число с указанием валюты.
- Валюта контракта и платежа должны быть явно названы.
- Контрагента указывай полностью, без сокращений.

{examples}
"""
            ),
            UserMessage(
                f"""Извлеки из текста договора и заполни поля:

Текст договора:
{text}
"""
            )
        ],
        temperature=0.2,
        top_p=1.0,
    )

    result_text = response.choices[0].message.content.strip()
    if result_text.startswith("```json"):
        result_text = result_text[len("```json"):].strip()
    elif result_text.startswith("```"):
        result_text = result_text[3:].strip()
    if result_text.endswith("```"):
        result_text = result_text[:-3].strip()

   
    return json.loads(result_text)

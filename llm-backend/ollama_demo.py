import json
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field  
from docx import Document  

class ContractInfo(BaseModel):
    contract_number: str = Field(..., description="№ контракта")
    contract_date: str = Field(..., description="Дата заключения контракта")
    end_date: str = Field(..., description="Дата окончания срока действия контракта")
    counterparty: str = Field(..., description="Наименование иностранного контрагента")
    country: str = Field(..., description="Страна контрагента")
    amount: str = Field(..., description="Сумма контракта")
    contract_currency: str = Field(..., description="Валюта контракта")
    payment_currency: str = Field(..., description="Валюта платежа")

llm = ChatOllama(model="Nemo-12B", temperature=0)
structured_llm = llm.with_structured_output(ContractInfo)

examples = """
Пример:
Текст: "Договор №12345 от 12 04 2024 года.
Срок действия до 31 декабря 2025 года. 
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

# 🔧 Промпт
prompt = ChatPromptTemplate.from_messages([
    ("system", f"""Ты — помощник для извлечения реквизитов договора.
Отвечай строго в формате JSON и заполняй все поля точно по тексту договора.
Правила:
- Даты всегда в формате ГГГГ-ММ-ДД (например: 2024-04-12).
- Сумму извлекай только как число с указанием валюты (например: "100000000 российские рубли").
- Валюта контракта и валюта платежа должны быть явно названы ("российские рубли", "доллары США"), а не "валюта договора".
- Контрагента указывай полностью, без сокращений или выдуманных данных.

{examples}
"""),
    ("user", """Извлеки из текста договора и заполни следующие поля:
- № контракта
- дата заключения договора (формат: YYYY-MM-DD)
- дата окончания договора (формат: YYYY-MM-DD)
- контрагент (полное название)
- страна контрагента
- сумма контракта (только число и валюта, например: "100000000 российские рубли")
- валюта контракта (например: "российские рубли")
- валюта платежа (например: "российские рубли")

Текст договора:
{contract_text}""")
])

chain = prompt | structured_llm

def load_docx_text(path: str) -> str:
    doc = Document(path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

contract_text = load_docx_text("8A16.ocr (1).docx")

# 🔍 печатаем то, что уходит в LLM
messages = prompt.format_messages(contract_text=contract_text)
print("\n=== Сообщения для LLM ===")
for msg in messages:
    print(f"[{msg.type.upper()}]\n{msg.content[:2000]}\n")

# 🚀 отправляем запрос
result = chain.invoke({"contract_text": contract_text})

with open("contract_info.json", "w", encoding="utf-8") as f:
    json.dump(result.dict(), f, ensure_ascii=False, indent=2)

print("✅ JSON сохранен в contract_info.json")

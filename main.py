import cv2
from pathlib import Path
from doc_preprocess import preprocess_document
from ocr import ocr_image, ocr_images
from llm.llm_pipeline import extract_contract_json
import json

pdf_path = Path(__file__).parent / "examples" / "1.pdf"
images = preprocess_document(pdf_path)
print(ocr_images(images))

contract_text = ocr_images(images)
print("=== OCR Text ===")
print(contract_text)

contract_json = extract_contract_json(contract_text)

with open("contract_from_main.json", "w", encoding="utf-8") as f:
    json.dump(contract_json, f, ensure_ascii=False, indent=2)

print("✅ JSON saved:", contract_json)
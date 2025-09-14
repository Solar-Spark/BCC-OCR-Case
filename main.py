import cv2
from pathlib import Path
from doc_preprocess import preprocess_document
from ocr import ocr_image, ocr_images

pdf_path = Path(__file__).parent / "examples" / "1.pdf"
images = preprocess_document(pdf_path)
print(ocr_images(images))
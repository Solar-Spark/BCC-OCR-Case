import cv2
from pathlib import Path
from doc_preprocess import preprocess_document

pdf_path = Path(__file__).parent / "examples" / "1.pdf"
images = preprocess_document(pdf_path)
for page in images:
    cv2.imshow("", page)
    cv2.waitKey(0)
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
import asyncio
import shutil
import mimetypes
from ocr import ocr_images
from doc_preprocess import preprocess_document
from llm.llm_pipeline import extract_contract_json
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads"); UPLOAD_DIR.mkdir(exist_ok=True)
CLEANED_DIR = Path("cleaned"); CLEANED_DIR.mkdir(exist_ok=True)

app.mount("/cleaned", StaticFiles(directory=CLEANED_DIR), name="cleaned")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    upload_path = UPLOAD_DIR / file.filename
    with upload_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    cleaned_name = f"preview_of_{file.filename}"
    cleaned_path = CLEANED_DIR / cleaned_name
    shutil.copy(upload_path, cleaned_path)

    contract_json = extract_contract_json(ocr_images(preprocess_document(cleaned_path)))

    mime, _ = mimetypes.guess_type(cleaned_path.name)

    return JSONResponse({
        "cleaned_url": f"/cleaned/{cleaned_name}",
        "mime": mime or "application/pdf",
        "fields": contract_json
    })
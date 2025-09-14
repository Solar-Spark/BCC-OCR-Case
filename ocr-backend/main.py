from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path
import shutil
import mimetypes

app = FastAPI()

# --- CORS (allow your Vite dev server) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Folders ---
UPLOAD_DIR = Path("uploads"); UPLOAD_DIR.mkdir(exist_ok=True)
CLEANED_DIR = Path("cleaned"); CLEANED_DIR.mkdir(exist_ok=True)

# --- Serve cleaned files at /cleaned/... ---
app.mount("/cleaned", StaticFiles(directory=CLEANED_DIR), name="cleaned")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Save uploaded file
    upload_path = UPLOAD_DIR / file.filename
    with upload_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    # Create cleaned file (you will process this in real case)
    cleaned_name = f"preview_of_{file.filename}"
    cleaned_path = CLEANED_DIR / cleaned_name
    shutil.copy(upload_path, cleaned_path)

    mime, _ = mimetypes.guess_type(cleaned_path.name)

    # Send back the cleaned file URL and metadata
    return JSONResponse({
        "cleaned_url": f"/cleaned/{cleaned_name}",  # Make sure this path works in the frontend
        "mime": mime or "application/pdf",
        "fields": {
            "document_type": "invoice",
            "invoice_number": "INV-1024",
            "date": "2025-09-14",
            "total_amount": 12345.67,
            "currency": "KZT",
            "vendor": "ACME Bank"
        },
        "metrics": {
            "cer": 0.121,
            "wer": 0.198,
            "exactMatchPct": 72.5,
            "jsonValidityPct": 96.0,
            "macroF1": 0.883,
            "fieldsF1": { "total_amount": 0.92, "date": 0.89, "invoice_number": 0.86 },
            "noisy": { "cer": 0.163, "wer": 0.241 }
        }
    })

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
    # Save upload
    upload_path = UPLOAD_DIR / file.filename
    with upload_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    # “Cleaning” mock: copy to cleaned/
    cleaned_name = f"cleaned_{file.filename}"
    cleaned_path = CLEANED_DIR / cleaned_name
    shutil.copy(upload_path, cleaned_path)

    mime, _ = mimetypes.guess_type(cleaned_path.name)
    return JSONResponse({
        "message": "File uploaded successfully",
        "cleaned_url": f"/cleaned/{cleaned_name}",
        "mime": mime or "application/octet-stream"
    })

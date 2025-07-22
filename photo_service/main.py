from fastapi import FastAPI, UploadFile, File, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from shared.config import decode_access_token

app = FastAPI(title="Photo Service")

UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload")
async def upload_photo(file: UploadFile = File(...), authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        username = payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_dir = UPLOAD_DIR / username
    user_dir.mkdir(parents=True, exist_ok=True)
    dest = user_dir / file.filename

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "user": username}

@app.get("/photos")
def list_photos(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        username = payload["sub"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_dir = UPLOAD_DIR / username
    if not user_dir.exists():
        return []

    return [f.name for f in user_dir.iterdir() if f.is_file()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

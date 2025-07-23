# 📸 main.py – Photo Upload + Retrieval API 

from fastapi import FastAPI, UploadFile, File, HTTPException, Header
# UploadFile lets users upload image files
# Header is used to read the Authorization: Bearer <token> header 

from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path
import shutil
# Standard Python libraries for handling file paths and copying files

from shared.config import decode_access_token
# JWT helper that verifies tokens and extracts the username

app = FastAPI(title="Photo Service")
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# Creates the FastAPI app
# Ensures static/uploads exists (this is where we’ll store photos)


# 🖼️ /upload – Upload a Photo
#
# @app.post("/upload")
# async def upload_photo(file: UploadFile = File(...), authorization: str = Header(...)):
#
# Step-by-step:
#   📥 Takes a file as form-data (i.e. uploaded file)
#   🔐 Extracts the JWT token from the Authorization header
#   ✅ Validates the token and gets the username (payload["sub"])
#   📁 Creates a user-specific folder if it doesn’t exist
#   💾 Saves the uploaded file under static/uploads/<username>/
#
# Example curl:
#   curl -X POST http://localhost:8003/upload \
#        -H "Authorization: Bearer <token>" \
#        -F "file=@test_photo.jpg"
# Response `{"filename": "test_photo.jpg", "user": "alice"}`
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


# 🧾 /photos – List Uploaded Photos
#
# @app.get("/photos")
# def list_photos(authorization: str = Header(...)):
#
# Step-by-step:
#   🔐 Reads the JWT from the header and validates it
#   👤 Gets the username
#   📂 Checks static/uploads/<username>/ for files
#   📤 Returns a list of uploaded photo filenames
# Example curl: `curl -H "Authorization: Bearer <token>" http://localhost:8003/photos`
#   Response: `["test_photo.jpg"]`
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

# Allows browser apps (like a frontend on localhost) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

"""
| Endpoint       | Auth Required | Purpose               |
| -------------- | ------------- | --------------------- |
| `POST /upload` | ✅ Yes        | Uploads a photo       |
| `GET /photos`  | ✅ Yes        | Lists uploaded photos |

🧠 Access control is enforced via token (Authorization header)
📁 File storage is per-user (isolated folders)

🔧 What Can Be Improved
| Area                | Fix Suggestion                                |
| ------------------- | --------------------------------------------- |
| File validation     | Reject `.exe`, limit size, check MIME type    |
| Storage backend     | Use Amazon S3 or MinIO for real deployments   |
| Auth checks         | Move to a `@require_auth` decorator for reuse |
| Duplicate filenames | Auto-rename or reject                         |
| File download       | Add endpoint like `/photo/<name>`             |
| Database            | Track photo metadata in DB (e.g. upload time) |

"""
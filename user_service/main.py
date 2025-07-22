from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from shared.config import decode_access_token

app = FastAPI(title="User Service")

# Fake user profile store
user_profiles = {}

@app.get("/me")
def read_profile(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        username = payload["sub"]
        return {"username": username, "profile": user_profiles.get(username, {})}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/me")
def update_profile(data: dict, authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        username = payload["sub"]
        user_profiles[username] = data
        return {"status": "updated"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

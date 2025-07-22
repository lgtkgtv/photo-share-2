from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from shared.config import create_access_token, verify_password, hash_password
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Auth Service")

# In-memory user store (replace with DB later)
users = {}

class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@app.post("/register", response_model=TokenResponse)
def register(user: UserCreate):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user.username] = hash_password(user.password)
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)

@app.post("/login", response_model=TokenResponse)
def login(user: UserCreate):
    if user.username not in users or not verify_password(user.password, users[user.username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)

# CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

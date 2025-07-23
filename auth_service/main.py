# 🧠 High-level Overview
#   Let users register (POST /auth/register)
#   Let users login (POST /auth/login)
#   Generate a JWT token (digital key) on login
#
#   uses:
#   pydantic models for input validation
#   JWT for secure authentication
#   Password hashing and verification

from fastapi import FastAPI, HTTPException, Depends
# FastAPI: to create the API app
# HTTPException: to raise proper error messages
# Depends: used for dependency injection (not used yet but useful for token auth)
    
from pydantic import BaseModel
# uses pydantic models for input validation -- this is a common practice in FastAPI 
# BaseModel is used to define request/response shapes

from shared.config import create_access_token, verify_password, hash_password
# These are helper functions defined in **shared/config.py**:
#   create_access_token(data):      Signs and returns a JWT token
#   hash_password(pwd):             Turns plain password into a secure hashed string
#   verify_password(plain, hashed): Checks if user input matches stored hash

from fastapi.middleware.cors import CORSMiddleware
# Adds CORS support so the frontend (running on another port) can make API calls.

import os
# We’re importing os to maybe use environment variables (not yet used here).


# 🏗️ FastAPI app setup - Creates a web app with a title (seen in Swagger docs).
app = FastAPI(title="Auth Service")

# In-memory user store (replace with DB later)
# ⚠️ This is a temporary fake database. When you stop the server, the users disappear.
# In the future, you'll use PostgreSQL, SQLite, or Redis instead.
users = {}

# 🧾 Pydantic Models (Schemas)

# Defines the request body for both /register and /login.
# Only allows JSON with username and password.
class UserCreate(BaseModel):
    username: str
    password: str

# Defines the response format for both endpoints.
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
# Example
# {
#  "access_token": "eyJhbGciOiJIUzI1NiIsInR5...",
#  "token_type": "bearer"
# }

# 📝 /register API Endpoint
#        This creates a POST /register endpoint
#        It accepts JSON with username and password
#        It returns a token using TokenResponse
@app.post("/register", response_model=TokenResponse)
def register(user: UserCreate):
    # Avoid duplicate registration
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    # Stores the hashed version of the password, not the plain one.
    users[user.username] = hash_password(user.password)
    # Creates a JWT token with the username embedded as the "subject" claim
    token = create_access_token({"sub": user.username})
    # Returns the token in the response - so you can use it in future requests
    return TokenResponse(access_token=token)

# 🔐 /login Endpoint
# Same as /register, it takes JSON like:
# {
#  "username": "alice",
#  "password": "secret"
# }
@app.post("/login", response_model=TokenResponse)
def login(user: UserCreate):
    # Checks if username exists and if the hashed password matches
    if user.username not in users or not verify_password(user.password, users[user.username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Gives you a new JWT token on successful login
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)

# CORS for development
# 🌍 CORS Middleware (Cross-Origin Resource Sharing)
# This allows frontend apps (like React or NiceGUI) on a different port (e.g., localhost:3000) 
# to call this API during development. For production, you’ll restrict allow_origins to only your own frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

""" This is a multiline comment that explains the Workflow

✅ Example Workflow

1. Register a user

curl -X POST http://localhost:8080/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret"}'

2. Login and get token

curl -X POST http://localhost:8080/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret"}'

3. Use token for future requests

Authorization: Bearer <your_token_here>

4. Access protected routes (not implemented yet, but you can use Depends for token auth)
# You can use Depends to create protected routes that require a valid token.
# For example, you can create a function that checks the token and use it as a dependency
# in your route handlers.
  
"""


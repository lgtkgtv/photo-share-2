"""
# This is a configuration file for the authentication service.
# It contains functions to create JWT tokens, hash passwords, and verify them.
# The JWT_SECRET and JWT_ALGORITHM can be set via environment variables for security.
# The TOKEN_EXPIRY_SECONDS defines how long the token is valid.
#
# | Function                | Purpose                             |
# | ----------------------- | ----------------------------------- |
# | `create_access_token()` | Creates a login token (JWT)         |
# | `decode_access_token()` | Reads and verifies a token          |
# | `hash_password()`       | Hashes a password (SHA-256)         |
# | `verify_password()`     | Checks if a password matches a hash |
"""
import os
import jwt
import hashlib
# from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone

"""
# These Variables are read from environment variables.
# If not set, they fallback to safe development defaults.
# | Variable               | Description                                   |
# | ---------------------- | --------------------------------------------- |
# | `JWT_SECRET`           | Secret key used to **sign and verify** tokens |
# | `JWT_ALGORITHM`        | Method used to sign (typically HS256)         |
# | `TOKEN_EXPIRY_SECONDS` | How long the token lasts (default 1 hour)     |
"""
JWT_SECRET = os.getenv("JWT_SECRET", "defaultsecret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRY_SECONDS = int(os.getenv("TOKEN_EXPIRY_SECONDS", "3600"))

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=TOKEN_EXPIRY_SECONDS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

# This function creates a JWT token (string)
# Uses the same JWT_SECRET to verify it
# Returns the original payload (e.g. { "sub": "alice", "exp": ... })
def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

def hash_password(password: str) -> str:
    # Hashes the password using SHA-256
    # ⚠️ Note: SHA-256 is okay for prototypes, but in real-world apps you should use 
    # bcrypt, argon2, or another slow hash that protects against brute-force attacks.
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


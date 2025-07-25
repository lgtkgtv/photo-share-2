# PhotoShare App - Milestone 2 -- Design Detail 

---
<div style="page-break-after: always;"></div>

## 🧱 Step 1: What is this app?

This is a **photo-sharing app** broken into microservices:

* Each part of the app (like login, profile, upload) is its own small program.
* They all run in separate containers using Docker.
* They talk to each other using HTTP APIs.
* There's a `gateway` that routes requests to the correct backend service.

---
<div style="page-break-after: always;"></div>

## 🧱 Step 2: What does each part do?

### 🔐 `auth_service/`

* Lets you **register** and **login**.
* Returns a **JWT token** (like a digital key) you use for other requests.

### 👤 `user_service/`

* Lets you **update your profile** (like name, bio).
* Reads that profile when you ask.

### 📸 `photo_service/`

* Lets you **upload photos**.
* Stores them in folders based on your username.
* Lets you list your uploaded files.

### 🌐 `gateway/`

* Uses NGINX to act as a **reverse proxy**.
* Sends `/auth/...` requests to the `auth_service`, `/users/...` to the `user_service`, etc.
* Exposes everything on one port: `http://localhost:8080`

---
<div style="page-break-after: always;"></div>

## ⚙️ Step 3: `docker-compose.yml`

This file defines and starts all 4 services. It looks like this (simplified):

```yaml
services:
  auth_service:
    build: ./auth_service
    ports:
      - "8001:8001"
    env_file: .env

  user_service:
    build: ./user_service
    ports:
      - "8002:8002"
    env_file: .env
    depends_on:
      - auth_service

  photo_service:
    build: ./photo_service
    ports:
      - "8003:8003"
    env_file: .env
    volumes:
      - ./photo_service/static/uploads:/app/static/uploads
    depends_on:
      - user_service

  gateway:
    build: ./gateway
    ports:
      - "8080:80"
    volumes:
      - ./gateway/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - auth_service
      - user_service
      - photo_service
```

Each service:

* Is built from its own folder
* Has its own port
* Depends on other services so startup happens in order
* Can share files (like uploads) using volumes

---
<div style="page-break-after: always;"></div>

## 📦 Step 4: How to run the app?

1. Open a terminal
2. Go to the app folder
3. Run:

```bash
docker compose up --build
```

This builds the containers and runs the services.

---

## 🧪 Step 5: How to test?

Use the test script:

```bash
./test_services.sh
```

This script will:

1. Register a new user
2. Login and get a token
3. Update your profile
4. Upload a fake photo
5. List the uploaded files

You’ll see printed output showing each step.

---

## 📁 Step 6: File/Folder Overview

```
photo-sharing/
├── auth_service/      🔐 Handles login & registration
├── user_service/      👤 Handles user profiles
├── photo_service/     📸 Handles uploads
├── gateway/           🌐 Routes traffic
├── .env               🌍 Shared config variables
├── docker-compose.yml ⚙ Defines how to run everything
├── test_services.sh   ✅ Script to test all APIs
└── readme-milestone-2.md 📘 Documentation
```

========================================================================================================================
<div style="page-break-after: always;"></div>



# app initialization 
---

## 1. Docker Compose Startup

- You run `docker compose up --build` in the project root.
- Docker Compose reads docker-compose.yml and builds four services:
  - auth_service
  - user_service
  - photo_service
  - gateway (NGINX)

Each service is built from its own directory and started in its own container. 
The gateway depends on the other three, so they start first.

---

## 2. Service Initialization

### a. **auth_service**
- FastAPI app starts (main.py).
- Loads environment variables (e.g., `JWT_SECRET`) from .env.
- Sets up in-memory user store.
- Adds CORS middleware for development.
- Exposes `/auth/register` and `/auth/login` endpoints.

### b. **user_service**
- FastAPI app starts (main.py).
- Loads JWT config from .env via config.py.
- Sets up in-memory user profile store.
- Adds CORS middleware.
- Exposes `/users/me` (GET/POST) endpoints, requiring JWT.

### c. **photo_service**
- FastAPI app starts (main.py).
- Loads JWT config from .env via config.py.
- Ensures `static/uploads/` directory exists.
- Adds CORS middleware.
- Exposes `/photos/upload` and `/photos/photos` endpoints, requiring JWT.

### d. **gateway**
- NGINX starts with config from `nginx.conf`.
- Routes `/auth/*` to auth_service, `/users/*` to user_service, `/photos/*` to photo_service.
- Exposes everything on port 8080.

---

## 3. Ready for Requests

- All APIs are now accessible via `http://localhost:8080` through the gateway.
- Each service is isolated, but the gateway makes them appear as a single API surface.

---

## 4. Testing

- You can run test_services.sh to exercise the full workflow: register, login, update profile, upload photo, list photos.

========================================================================================================================
<div style="page-break-after: always;"></div>

# Explanation `docker-compose.yml`:

## Services

### 1. auth_service
- **Builds from:** auth_service
- **Exposes port:** 8001 (container:host)
- **Loads env vars from:** .env

### 2. user_service
- **Builds from:** user_service
- **Exposes port:** 8002
- **Loads env vars from:** .env
- **Depends on:** auth_service (starts after auth)

### 3. photo_service
- **Builds from:** photo_service
- **Exposes port:** 8003
- **Loads env vars from:** .env
- **Mounts volume:** Maps uploads on the host to `/app/static/uploads` in the container (for persistent photo storage)
- **Depends on:** user_service (starts after user)

### 4. gateway
- **Builds from:** gateway
- **Exposes port:** 8080 (host) mapped to 80 (container)
- **Mounts config:** Maps nginx.conf to the container’s NGINX config (read-only)
- **Depends on:** All three backend services (starts last)

---

## How it works

- **Startup order:** auth_service → user_service → photo_service → gateway
- **Networking:** All services are on the same Docker network and can communicate by service name.
- **Gateway:** NGINX routes incoming requests to the correct backend service based on the URL path.

========================================================================================================================
<div style="page-break-after: always;"></div>

# auth service initialization

```
auth_service/
    ├── Dockerfile
    ├── main.py
    ├── models
    ├── routes
    ├── shared
    │   └── config.py
    └── static
        └── uploads

shared
    ├── config.py
    ├── models
    ├── routes
    └── static
        └── uploads
```


```Dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY ./shared /app/shared
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn python-multipart pyjwt

ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## auth_service/main.py

commented inline

## shared/config.py 

| Function                         | Purpose                        |
| -------------------------------- | ------------------------------ |
| `create_access_token(data)`      | Creates a signed JWT           |
| `hash_password(password)`        | Hashes a password securely     |
| `verify_password(plain, hashed)` | Verifies password against hash |

🧠 Concepts You Need First
JWT (JSON Web Token) = a signed digital string that proves who you are.  
Hashing = turning your password into a secret string that cannot be reversed.  
bcrypt = secure hashing method for passwords.  
SECRET_KEY = like a signing key or password for your app.  

========================================================================================================================
<div style="page-break-after: always;"></div>

#  `test_services.sh` with comment 

#!/bin/bash
# Exit immediately if any command fails
set -e

## 🧠 Tips for Understanding
#
#   curl -s:        makes a silent HTTP request (no progress bar)
#   jq:             command-line JSON processor (used to format/parse response)
#   Bearer $TOKEN:  is how the JWT token is sent to authenticate Alice

# Base URL of the gateway where all services are routed through
BASE_URL="http://localhost:8080"

# ---------------------------------------------------------------
# ✅ STEP 1: Register a new user called "alice"
# Sends a POST request to /auth/register with JSON payload
# The response will include a JWT token
echo "✅ Registering user 'alice'..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "password123"}' \
  | jq -r .access_token)

# Save and display the access token
echo "🔑 Got token: $TOKEN"

# ---------------------------------------------------------------
# 📝 STEP 2: Update Alice's profile
# Sends a POST request to /users/me with authorization header and new profile data
echo "📝 Updating profile..."
curl -s -X POST "$BASE_URL/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice", "bio": "Photographer"}' \
  | jq .

# ---------------------------------------------------------------
# 📄 STEP 3: Fetch Alice's profile
# Sends a GET request to /users/me with the same token
echo "📄 Fetching profile..."
curl -s -X GET "$BASE_URL/users/me" \
  -H "Authorization: Bearer $TOKEN" \
  | jq .

# ---------------------------------------------------------------
# 📸 STEP 4: Upload a test photo
# Sends a multipart POST request to /photos/upload with image file
echo "📸 Uploading photo..."
curl -s -X POST "$BASE_URL/photos/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test_photo.jpg" \
  | jq .

# ---------------------------------------------------------------
# 🖼️ STEP 5: List uploaded photos
# Sends a GET request to /photos/photos to list all uploaded images for Alice
echo "🖼️  Listing uploaded photos..."
curl -s -X GET "$BASE_URL/photos/photos" \
  -H "Authorization: Bearer $TOKEN" \
  | jq .



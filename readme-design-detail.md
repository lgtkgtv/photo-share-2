# PhotoShare App - Milestone 2 -- Design Detail 

---

## 🧱 Step 1: What is this app?

This is a **photo-sharing app** broken into microservices:

* Each part of the app (like login, profile, upload) is its own small program.
* They all run in separate containers using Docker.
* They talk to each other using HTTP APIs.
* There's a `gateway` that routes requests to the correct backend service.

---

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

Would you like to walk through one folder at a time (e.g., `auth_service/`) next? I can explain what’s in `main.py`, how JWT works, or even how `test_services.sh` does each step. Just say the word!

========================================================================================================================

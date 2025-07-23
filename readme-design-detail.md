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

---

Would you like to walk through one folder at a time (e.g., `auth_service/`) next? I can explain what’s in `main.py`, how JWT works, or even how `test_services.sh` does each step. Just say the word!


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

---

# Explanation `docker-compose.yml`:

---

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

---

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

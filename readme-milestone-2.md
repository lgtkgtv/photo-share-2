# 📸 Photo Sharing App – Milestone 2

This is a working **microservices-based photo sharing app** with JWT-based user authentication, profile management, and secure photo uploads — all containerized using Docker Compose.

---

## ✅ Features Implemented

- 📦 Dockerized microservices for auth, user, and photo APIs
- 🔐 JWT-based user registration & login (in-memory)
- 👤 User profile read/update via token auth
- 📸 Photo upload and listing per authenticated user
- 📂 File system-based photo storage
- 🌐 NGINX-based gateway routing
- 🧪 Automated test script: `./test_services.sh`

---

## 🏗️ Architecture & Design

```
                       +------------------------+
                       |     NGINX Gateway      |
                       |  (localhost:8080)      |
                       +-----------+------------+
                                   |
       +-----------+--------------+-------------+------------+
       |           |                            |            |
+------+     /auth/* APIs               /users/* APIs     /photos/* APIs
|           |                            |            |
|  Auth     v                            v            v   Photo
| Service   +----------------+   +----------------+   +----------------+
| 8001      | Register/Login |   | Profile API    |   | Upload/Listing |
+-----------+----------------+   +----------------+   +----------------+
             returns JWT            token auth          token auth
```

Each service is independently deployed and can scale horizontally.

---

## 🗂️ Project Structure

```
photo-sharing/
├── auth_service/
│   ├── main.py              # Register/Login
│   ├── shared/config.py     # JWT logic
│   └── Dockerfile
│
├── user_service/
│   ├── main.py              # /me profile APIs
│   ├── shared/config.py     # JWT decode
│   └── Dockerfile
│
├── photo_service/
│   ├── main.py              # upload/list endpoints
│   ├── static/uploads/      # per-user folders
│   ├── shared/config.py     # JWT decode
│   └── Dockerfile
│
├── gateway/
│   ├── nginx.conf           # reverse proxy routes
│   └── Dockerfile
│
├── docker-compose.yml       # compose services on port 8080
├── .env                     # shared config vars
├── test_services.sh         # automated test script
└── test_photo.jpg           # test upload image
```

---

## 🐳 Docker Compose

```yaml
services:
  auth_service:    localhost:8001  → /auth/*
  user_service:    localhost:8002  → /users/*
  photo_service:   localhost:8003  → /photos/*
  gateway:         localhost:8080  → public entrypoint
```

Start it with:

```bash
docker compose up --build
```

Access via: [http://localhost:8080](http://localhost:8080)

---

## 🔁 API Summary

### 🔐 Auth API (`/auth/`)
| Method | Endpoint     | Description        |
|--------|--------------|--------------------|
| POST   | /register     | Create user, returns JWT |
| POST   | /login        | Authenticate user, returns JWT |

---

### 👤 User API (`/users/`)
| Method | Endpoint     | Description        |
|--------|--------------|--------------------|
| GET    | /me          | Get current user profile (JWT required) |
| POST   | /me          | Update profile (JWT required) |

---

### 📸 Photo API (`/photos/`)
| Method | Endpoint     | Description        |
|--------|--------------|--------------------|
| POST   | /upload      | Upload file (JWT required) |
| GET    | /photos      | List user's uploaded photos |

---

## ✅ Testing Instructions

After `docker compose up --build`, run:

```bash
chmod +x test_services.sh
./test_services.sh
```

This script:
1. Registers user `alice`
2. Logs in and gets JWT token
3. Updates and fetches profile
4. Uploads a test image
5. Lists uploaded photos

---

## ⚠️ Known Limitations

| Area             | Limitation                                  |
|------------------|----------------------------------------------|
| Auth             | No persistent user DB                        |
| Photo Storage    | Stored on local volume (not S3/MinIO)        |
| Profiles         | Stored in memory only                        |
| UI               | No front-end yet                             |
| API Docs         | No Swagger/OpenAPI routes yet                |

---

## 🚀 Planned Enhancements

- 🧠 NiceGUI or React UI frontend
- 📦 SQLite or PostgreSQL for user/profile/photo metadata
- 🪣 MinIO or AWS S3 for image storage
- 🔐 OAuth2 login (e.g. Google)
- 🔍 Swagger UI for dev/testing
- 🧪 GitHub Actions CI for API testing

---

Built with ❤️ for modularity, security, and simplicity.

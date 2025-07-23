# Copilot Coding Agent Instructions for Photo Share 2

## Overview
This repository implements a microservices-based photo sharing app, with each service in its own directory and containerized using Docker Compose. The system is designed for modularity, security, and ease of local development.

## Architecture
- **Services:**
  - `auth_service/`: Handles user registration and login, issues JWT tokens.
  - `user_service/`: Manages user profiles (read/update), requires JWT authentication.
  - `photo_service/`: Handles photo uploads and listing, stores files per user, requires JWT authentication.
  - `gateway/`: NGINX reverse proxy, routes `/auth/*`, `/users/*`, `/photos/*` to the correct backend service, exposes everything on port 8080.
- **Shared Logic:** Each service has a `shared/config.py` for JWT and password logic. These are nearly identical and use environment variables for secrets.
- **Data Storage:** All data is in-memory or on local disk (no persistent DB yet). User and profile data will be lost on restart.

## Developer Workflows
- **Build & Run:**
  - Use `docker compose up --build` from the project root to build and start all services.
  - All services are accessible via the gateway at `http://localhost:8080`.
- **Testing:**
  - Run `./test_services.sh` to exercise registration, login, profile update, photo upload, and listing. This script uses `curl` and expects the gateway to be running.
- **Environment Variables:**
  - Secrets and config (e.g., `JWT_SECRET`, `JWT_ALGORITHM`, `TOKEN_EXPIRY_SECONDS`) are set via `.env` and loaded in each service's `shared/config.py`.

## Project Conventions & Patterns
- **Endpoints:**
  - Auth: `/auth/register`, `/auth/login` (POST)
  - User: `/users/me` (GET/POST, JWT required)
  - Photo: `/photos/upload` (POST, JWT required), `/photos/photos` (GET, JWT required)
- **JWT Auth:**
  - All protected endpoints expect `Authorization: Bearer <token>` header.
  - JWT payload uses `sub` claim for username.
- **Password Hashing:**
  - Uses SHA-256 (see `shared/config.py`).
- **CORS:**
  - All services enable permissive CORS for development.
- **File Uploads:**
  - Photos are stored in `photo_service/static/uploads/<username>/`.
- **No Persistent DB:**
  - All user, profile, and photo metadata is ephemeral.

## Integration Points
- **NGINX Gateway:**
  - Configured in `gateway/nginx.conf` to route requests to the correct service.
- **Shared JWT Logic:**
  - Each service has a local copy of `shared/config.py` for token handling.

## Examples
- Register and login via `/auth/register` and `/auth/login` to get a JWT.
- Use the JWT to call `/users/me` or `/photos/upload`.
- See `test_services.sh` for a full workflow example.

## Limitations
- No persistent storage or database.
- No frontend UI.
- No Swagger/OpenAPI docs yet.

---
For more details, see `readme-milestone-2.md` and `readme-design-detail.md`.

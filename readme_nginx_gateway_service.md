## 🌐 gateway service
```
📦 NGINX
 ├── /auth/   ➝ auth_service (port 8001)
 ├── /users/  ➝ user_service (port 8002)
 └── /photos/ ➝ photo_service (port 8003)
```
The gateway exposes one public port (80) and hides the internal service ports.

```Dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
```
- nginx:alpine: lightweight Nginx image
- Copies your custom config into /etc/nginx/nginx.conf inside the container

### 🧠 nginx.conf — Explained Step-by-Step  

events {}  
- Required section for Nginx (can be empty for basic setups)

🌍 http block  
```
http {
```
- This is where all routing logic goes.

🔁 Upstream declarations  
```
    upstream auth_service {
        server auth_service:8001;
    }
    upstream user_service {
        server user_service:8002;
    }
    upstream photo_service {
        server photo_service:8003;
    }
```
- Each upstream defines how to reach a **Docker service** by name and port
- These names `(auth_service, user_service, photo_service)` must match service names in `docker-compose.yml` 

🌐 Server block — External HTTP listener  
```
    server {
        listen 80;
```
This tells Nginx to:  
  Accept HTTP traffic on port 80 (inside container)  
  Docker will map it to localhost:8080 on your host  

🔀 Location blocks — URL path routing  

🔐 /auth/ ➝ auth_service
```
        location /auth/ {
            proxy_pass http://auth_service/;
            proxy_set_header Host $host;
        }
```

Any request like `/auth/login` or `/auth/register` is proxied to:
```
http://auth_service:8001/login
```

👤 /users/ ➝ user_service
```
        location /users/ {
            proxy_pass http://user_service/;
            proxy_set_header Host $host;
        }
```

🖼️ /photos/ ➝ photo_service
```
        location /photos/ {
            proxy_pass http://photo_service/;
            proxy_set_header Host $host;
        }
```

📈 How It All Connects (ASCII Diagram)
```
          ┌────────────┐
          │   Client   │
          └─────┬──────┘
                │
         HTTP @ localhost:8080
                ▼
        ┌───────────────┐
        │   GATEWAY     │  (nginx)
        │ listens on 80 │
        └────┬─────┬────┘
             │     │
   ┌─────────┘     └─────────┐
   ▼                         ▼
AUTH SERVICE         ┌──────────────┐
 (localhost:8001) ◄──│ /auth/...    │
                     └──────────────┘

USER SERVICE         ┌──────────────┐
 (localhost:8002) ◄──│ /users/...   │
                     └──────────────┘

PHOTO SERVICE        ┌──────────────┐
 (localhost:8003) ◄──│ /photos/...  │
                     └──────────────┘

```

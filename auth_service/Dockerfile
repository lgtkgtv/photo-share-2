FROM python:3.12-slim
#  Uses a lightweight Python 3.12 base image.

WORKDIR /app
#  Sets the working directory inside the container to `/app`.

COPY ./shared /app/shared
#  Copies the shared code (like JWT/password logic) into the container.

COPY . /app
#  Copies the rest of the auth_service code into the container.

RUN pip install --no-cache-dir fastapi uvicorn python-multipart pyjwt
#  Installs all required Python packages for the service:  
#  - `fastapi` (web framework)  
#  - `uvicorn` (ASGI server)  
#  - `python-multipart` (for file uploads, though not used in auth)  
#  - `pyjwt` (for JWT token handling)

ENV PYTHONPATH=/app
#  Ensures Python can import modules from `/app`.

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
#   Starts the FastAPI app using Uvicorn, listening on port 8001.
#  The `main:app` refers to the FastAPI application instance defined in `main.py`.
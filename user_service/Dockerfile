FROM python:3.12-slim

WORKDIR /app

COPY ./shared /app/shared
# Copies shared logic (like JWT helpers) and all service code into the container.
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn python-multipart pyjwt

ENV PYTHONPATH=/app
# Tells Python to look for imports inside /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

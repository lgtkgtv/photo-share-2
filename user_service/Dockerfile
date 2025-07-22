FROM python:3.12-slim

WORKDIR /app

COPY ./shared /app/shared
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn python-multipart pyjwt

ENV PYTHONPATH=/app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

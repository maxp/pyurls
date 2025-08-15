FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/var

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

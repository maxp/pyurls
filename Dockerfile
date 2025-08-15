FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# NOTE: ?exclude non production code?
COPY . .

CMD ["fastapi", "run" "app/main.py", "--host", "0.0.0.0", "--port", "8000"]

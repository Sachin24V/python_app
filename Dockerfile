FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -e .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}"]

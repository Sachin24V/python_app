FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    poppler-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project files
COPY . .

# Install Python deps
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

# Run with Railway's PORT or fallback
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

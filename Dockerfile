# Use official Python image
FROM python:3.11-slim

# Install system dependencies including tesseract
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose default port (Railway dynamically sets it anyway)
EXPOSE 8000

# Start app with shell-expansion for PORT
CMD ["sh", "-c", "uvicorn main:app --host=0.0.0.0 --port=${PORT}"]

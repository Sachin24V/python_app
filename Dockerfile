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

# Expose the port Railway will use
EXPOSE 8000

# Run the app with the correct dynamic port
CMD ["sh", "-c", "uvicorn main:app --host=0.0.0.0 --port=$PORT"]

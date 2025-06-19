FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ✅ Copy all files (including README.md, main.py, etc.) before install
COPY . .

# ✅ Now install project with README.md available
RUN pip install -e .

EXPOSE 8000

# ✅ Use shell form to allow Railway's $PORT variable (optional)
CMD ["sh", "-c", "uvicorn main:app --host=0.0.0.0 --port=${PORT:-8000}"]

# Deployment Guide

## GitHub Upload Instructions

### 1. Initialize Git Repository

```bash
git init
git add .
git commit -m "Initial commit: Medical OCR Extractor API"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click "New repository" or use the "+" button
3. Repository name: `medical-ocr-extractor`
4. Description: `FastAPI service for extracting structured medical data from reports using OCR`
5. Choose Public or Private
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### 3. Connect Local Repository to GitHub

```bash
git remote add origin https://github.com/yourusername/medical-ocr-extractor.git
git branch -M main
git push -u origin main
```

Replace `yourusername` with your actual GitHub username.

## Production Deployment Options

### Option 1: Replit Deployment
- Your project is already running on Replit
- Use Replit's deployment feature for instant hosting
- Automatic HTTPS and domain provided

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
RUN pip install -e .

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Option 3: Cloud Platforms

**Heroku:**
```bash
# Install Heroku CLI and login
heroku create medical-ocr-extractor
git push heroku main
```

**Railway:**
```bash
# Install Railway CLI
railway login
railway deploy
```

**Digital Ocean App Platform:**
- Connect GitHub repository
- Auto-deploys on push

## Environment Variables

For production deployment, set these environment variables:

```bash
export MAX_FILE_SIZE=10485760  # 10MB in bytes
export LOG_LEVEL=INFO
export HOST=0.0.0.0
export PORT=8000
```

## System Requirements

- Python 3.11+
- Tesseract OCR
- 512MB RAM minimum
- 1GB storage for temporary files

## Monitoring and Logging

The API includes built-in logging. For production:

1. Set `LOG_LEVEL=INFO` or `ERROR`
2. Configure log rotation
3. Monitor endpoints: `/health` for health checks
4. Track file processing metrics

## Security Considerations

- File size limits are enforced (10MB default)
- Temporary files are automatically cleaned up
- Input validation on all endpoints
- Consider rate limiting for production use

## Performance Optimization

- Use async file operations
- Implement caching for frequently processed reports
- Consider worker processes for high load
- Monitor memory usage during PDF processing
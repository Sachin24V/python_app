# Medical Report OCR Extractor API

## Overview

This is a FastAPI-based web service that extracts structured medical data from PDF and image reports using Tesseract OCR. The system processes uploaded medical documents and returns structured data including patient information and report details using regex-based field parsing.

## System Architecture

The application follows a modular microservice architecture with clear separation of concerns:

### Backend Architecture
- **Framework**: FastAPI with Python 3.11
- **OCR Engine**: Tesseract OCR for text extraction
- **PDF Processing**: PyMuPDF (fitz) for PDF to image conversion
- **Image Processing**: Pillow (PIL) for image manipulation
- **Data Validation**: Pydantic models for request/response validation
- **File Handling**: aiofiles for asynchronous file operations

### Core Components
1. **API Layer** (`main.py`) - FastAPI application with endpoints
2. **OCR Service** (`ocr_service.py`) - Text extraction from PDFs and images
3. **Field Parser** (`field_parser.py`) - Regex-based medical field extraction
4. **Data Models** (`models.py`) - Pydantic models for structured data
5. **Utilities** (`utils.py`) - File validation and handling utilities

## Key Components

### API Endpoints
- `GET /` - Root endpoint with API information
- `GET /health` - Health check endpoint
- `POST /extract` - Main endpoint for medical report processing

### OCR Processing Pipeline
1. File upload validation (format, size limits)
2. Text extraction using Tesseract OCR
3. PDF conversion to images when necessary
4. Structured field parsing using regex patterns
5. Response formatting with Pydantic models

### Data Models
- **PatientInfo**: Patient demographics and identifiers
- **ReportDetails**: Report metadata and institutional information
- **MedicalReportData**: Complete structured response
- **ErrorResponse**: Standardized error handling

## Data Flow

1. **File Upload**: Client uploads PDF/image file via POST /extract
2. **Validation**: File format and size validation
3. **Temporary Storage**: File saved to temporary location
4. **OCR Processing**: Text extraction using Tesseract
5. **Field Parsing**: Regex-based extraction of medical fields
6. **Response**: Structured JSON response with extracted data
7. **Cleanup**: Temporary files removed

## External Dependencies

### Core Libraries
- **FastAPI**: Web framework for API development
- **Uvicorn**: ASGI server for running the application
- **Tesseract**: OCR engine for text extraction
- **PyMuPDF**: PDF processing and conversion
- **Pillow**: Image processing and manipulation
- **Pydantic**: Data validation and serialization
- **aiofiles**: Asynchronous file operations

### System Dependencies
- Tesseract OCR engine and language packs
- Various image processing libraries (freetype, harfbuzz, etc.)
- PDF processing tools (mupdf, openjpeg)

## Deployment Strategy

### Development Environment
- **Runtime**: Python 3.11 with Nix package management
- **Server**: Uvicorn ASGI server on port 8000
- **File Limits**: 10MB maximum file size
- **Supported Formats**: PDF, PNG, JPG, JPEG

### Production Considerations
- File size limits configurable via MAX_FILE_SIZE
- Logging configured for monitoring and debugging
- Error handling with structured error responses
- Temporary file cleanup for resource management

### Key Architectural Decisions

**OCR Engine Choice**: Tesseract was chosen for its medical text recognition capabilities and open-source nature. The service uses specific OCR configuration optimized for medical documents.

**PDF Processing Strategy**: PDFs are converted to images before OCR processing to ensure consistent text extraction quality across different PDF types.

**Field Extraction Approach**: Regex-based parsing was chosen for its speed and reliability with structured medical reports, though it requires maintenance of pattern definitions.

**Async File Handling**: aiofiles is used for non-blocking file operations to maintain API responsiveness during large file processing.

## Changelog

- June 16, 2025: Initial setup - FastAPI OCR service with Tesseract
- June 16, 2025: Updated response format to return only patient_info and report_details (removed metadata fields per user request)

## User Preferences

Preferred communication style: Simple, everyday language.
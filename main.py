import os
import tempfile
import json
from typing import List, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
import logging

from models import MedicalReportData, MedicalReportDataDetailed, ErrorResponse
from ocr_service import OCRService
from field_parser import FieldParser
from utils import validate_file, save_uploaded_file, format_medical_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Medical Report OCR Extractor",
    description="A FastAPI service that extracts structured medical data from PDF and image reports using Tesseract OCR",
    version="1.0.0"
)

# Initialize services
ocr_service = OCRService()
field_parser = FieldParser()

# File size limit (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg'}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Medical Report OCR Extractor API",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/extract",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Medical Report OCR Extractor"}

@app.post("/extract", response_model=MedicalReportData)
async def extract_medical_data(file: UploadFile = File(...)):
    """
    Extract structured medical data from uploaded PDF or image file
    
    Args:
        file: Uploaded file (PDF, PNG, JPG, JPEG)
    
    Returns:
        MedicalReportData: Structured medical report data
    """
    try:
        # Validate file
        validation_error = validate_file(file, MAX_FILE_SIZE, ALLOWED_EXTENSIONS)
        if validation_error:
            raise HTTPException(status_code=400, detail=validation_error)
        
        logger.info(f"Processing file: {file.filename}")
        
        # Save uploaded file temporarily
        filename = file.filename or "unknown"
        file_ext = os.path.splitext(filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
            temp_file_path = temp_file.name
            await save_uploaded_file(file, temp_file_path)
        
        try:
            # Extract text using OCR
            extracted_text = ocr_service.extract_text(temp_file_path)
            
            if not extracted_text.strip():
                raise HTTPException(
                    status_code=422, 
                    detail="No text could be extracted from the uploaded file. Please ensure the file contains readable text."
                )
            
            logger.info(f"Extracted text length: {len(extracted_text)} characters")
            
            # Parse medical fields from extracted text
            medical_data = field_parser.parse_medical_fields(extracted_text)
            
            logger.info(f"Successfully processed file: {filename}")
            
            # Format response using utility function for better readability
            formatted_response = format_medical_response(medical_data)
            
            # Return with formatted JSON and proper content type
            return JSONResponse(
                content=formatted_response,
                status_code=200,
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error while processing file: {str(e)}"
        )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=exc.detail,
            status_code=exc.status_code
        ).dict()
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

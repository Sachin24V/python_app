import os
from typing import Set, Optional
from fastapi import UploadFile
import aiofiles
import logging

logger = logging.getLogger(__name__)

def validate_file(file: UploadFile, max_size: int, allowed_extensions: Set[str]) -> Optional[str]:
    """
    Validate uploaded file for size and format
    
    Args:
        file: Uploaded file object
        max_size: Maximum file size in bytes
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        Optional[str]: Error message if validation fails, None if valid
    """
    # Check if file is provided
    if not file or not file.filename:
        return "No file provided"
    
    # Check file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        return f"File format not supported. Allowed formats: {', '.join(allowed_extensions)}"
    
    # Check file size (this is approximate as we haven't read the file yet)
    if hasattr(file, 'size') and file.size and file.size > max_size:
        return f"File size exceeds maximum allowed size of {max_size // (1024 * 1024)}MB"
    
    return None

async def save_uploaded_file(file: UploadFile, file_path: str) -> None:
    """
    Save uploaded file to specified path
    
    Args:
        file: Uploaded file object
        file_path: Path where file should be saved
    """
    try:
        async with aiofiles.open(file_path, 'wb') as f:
            # Read file in chunks to handle large files
            while chunk := await file.read(8192):  # 8KB chunks
                await f.write(chunk)
        
        logger.info(f"File saved successfully to {file_path}")
        
    except Exception as e:
        logger.error(f"Error saving file to {file_path}: {str(e)}")
        raise

def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format
    
    Args:
        size_bytes: File size in bytes
        
    Returns:
        str: Formatted file size
    """
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

def clean_extracted_text(text: str) -> str:
    """
    Clean and normalize extracted text
    
    Args:
        text: Raw extracted text
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Replace multiple spaces with single space
    text = ' '.join(text.split())
    
    # Remove excessive newlines
    text = '\n'.join(line.strip() for line in text.split('\n') if line.strip())
    
    return text

def get_file_info(file_path: str) -> dict:
    """
    Get file information
    
    Args:
        file_path: Path to file
        
    Returns:
        dict: File information
    """
    if not os.path.exists(file_path):
        return {}
    
    stat = os.stat(file_path)
    return {
        'size': stat.st_size,
        'size_formatted': format_file_size(stat.st_size),
        'extension': os.path.splitext(file_path)[1].lower(),
        'basename': os.path.basename(file_path)
    }

def format_medical_response(data) -> dict:
    """
    Format medical report response with proper spacing and readable structure
    
    Args:
        data: Medical report data object
        
    Returns:
        dict: Formatted response dictionary
    """
    return {
        "patient_info": {
            "name": data.patient_info.name or "",
            "id": data.patient_info.id or "",
            "sex": data.patient_info.sex or "",
            "birthdate_age": data.patient_info.birthdate_age or "",
            "accession_number": data.patient_info.accession_number or "",
            "referring_physician": data.patient_info.referring_physician or "",
            "study_id": data.patient_info.study_id or "",
            "height": data.patient_info.height or "",
            "weight": data.patient_info.weight or "",
            "bsa": data.patient_info.bsa or "",
            "acquisition_date": data.patient_info.acquisition_date or "",
            "comments": data.patient_info.comments or ""
        },
        "report_details": {
            "user_name": data.report_details.user_name or "",
            "created_on": data.report_details.created_on or "",
            "license_id": data.report_details.license_id or "",
            "physician": data.report_details.physician or "",
            "institution_name": data.report_details.institution_name or "",
            "institution_address": data.report_details.institution_address or "",
            "department_name": data.report_details.department_name or ""
        }
    }
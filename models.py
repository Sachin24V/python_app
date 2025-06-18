from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class PatientInfo(BaseModel):
    """Patient information model"""
    name: Optional[str] = Field(None, description="Patient's full name")
    id: Optional[str] = Field(None, description="Patient ID number")
    sex: Optional[str] = Field(None, description="Patient's sex/gender")
    birthdate_age: Optional[str] = Field(None, description="Patient's birthdate and age")
    accession_number: Optional[str] = Field(None, description="Accession number")
    referring_physician: Optional[str] = Field(None, description="Referring physician")
    study_id: Optional[str] = Field(None, description="Study ID")
    height: Optional[str] = Field(None, description="Patient height")
    weight: Optional[str] = Field(None, description="Patient weight")
    bsa: Optional[str] = Field(None, description="Body surface area")
    acquisition_date: Optional[str] = Field(None, description="Acquisition date")
    comments: Optional[str] = Field(None, description="Comments")

class ReportDetails(BaseModel):
    """Report details model"""
    user_name: Optional[str] = Field(None, description="User name")
    created_on: Optional[str] = Field(None, description="Report creation date")
    license_id: Optional[str] = Field(None, description="License ID")
    physician: Optional[str] = Field(None, description="Physician name")
    institution_name: Optional[str] = Field(None, description="Institution or hospital name")
    institution_address: Optional[str] = Field(None, description="Institution address")
    department_name: Optional[str] = Field(None, description="Department name")

class MedicalReportData(BaseModel):
    """Complete medical report data model"""
    patient_info: PatientInfo = Field(default_factory=lambda: PatientInfo(), description="Patient information")
    report_details: ReportDetails = Field(default_factory=lambda: ReportDetails(), description="Report details")

class MedicalReportDataDetailed(BaseModel):
    """Detailed medical report data model with metadata"""
    patient_info: PatientInfo = Field(default_factory=lambda: PatientInfo(), description="Patient information")
    report_details: ReportDetails = Field(default_factory=lambda: ReportDetails(), description="Report details")
    raw_text: Optional[str] = Field(None, description="Raw extracted text from OCR")
    source_filename: Optional[str] = Field(None, description="Original filename")
    extraction_confidence: Optional[str] = Field(None, description="Confidence level of extraction")
    processed_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Processing timestamp")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="Error timestamp")

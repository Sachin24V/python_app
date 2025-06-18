import re
from typing import Dict, Optional, List
from models import MedicalReportData, PatientInfo, ReportDetails
import logging

logger = logging.getLogger(__name__)

class FieldParser:
    """Parser for extracting structured medical report fields from text"""
    
    def __init__(self):
        """Initialize field parser with regex patterns"""
        self.patterns = self._compile_patterns()
    
    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """
        Compile regex patterns for medical field extraction
        
        Returns:
            Dict[str, re.Pattern]: Compiled regex patterns
        """
        patterns = {
            # Report Details Patterns
            'user_name': re.compile(
                r'(?:username|user\s*name)\s*:?\s*([A-Za-z0-9\s\-._]+?)(?:\n|created|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'created_on': re.compile(
                r'(?:created\s*on|createdon)\s*:?\s*(\d{1,2}\/\d{1,2}\/\d{4}\s*\d{1,2}:\d{2}:\d{2}|\d{1,2}\/\d{1,2}\/\d{4})',
                re.IGNORECASE
            ),
            'license_id': re.compile(
                r'(?:license\s*id|licenseid)\s*:?\s*(\d+)',
                re.IGNORECASE
            ),
            'physician': re.compile(
                r'(?:physician)\s+((?:DR\.\s*[A-Z]+\/)*DR\.\s*[A-Z]+)',
                re.IGNORECASE | re.MULTILINE
            ),
            'institution_name': re.compile(
                r'(?:institution\s*name|institutionname)\s*:?\s*([A-Z\s]+?)(?:\n|institution\s*address|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'institution_address': re.compile(
                r'(?:institution\s*address|institutionaddress)\s*:?\s*([A-Za-z0-9\s,.-]*?)(?:\n|department|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'department_name': re.compile(
                r'(?:department\s*name|departmentname)\s*:?\s*([A-Z0-9\s]+?)(?:\n|patient|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            
            # Patient Information Patterns
            'patient_name': re.compile(
                r'(?:name|patient\s*name)\s+([A-Z\s\.]+?)\s+(?:sex\s+|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'patient_id': re.compile(
                r'([A-Z]{1,3}\/\d+\/\d+[YM]?)',
                re.MULTILINE
            ),
            'sex': re.compile(
                r'(?:sex\s+|gender\s+)(male|female|m|f)\b',
                re.IGNORECASE
            ),
            'birthdate_age': re.compile(
                r'birthdate\s*\(age\)\s+([^:\n\r]+?)(?:\s*accession|\s*$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'accession_number': re.compile(
                r'(?:accession\s*number|accessionnumber)\s*:?\s*([A-Z0-9]+)',
                re.IGNORECASE
            ),
            'referring_physician': re.compile(
                r'(?:referring\s*physician|referringphysician)\s*:?\s*([A-Za-z\s,.-]*?)(?:\n|study|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'study_id': re.compile(
                r'(?:study\s*id|studyid)\s*:?\s*([A-Z0-9]+)',
                re.IGNORECASE
            ),
            'height': re.compile(
                r'(?:height)\s*:?\s*([^:\n]*?)(?:\n|weight|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'weight': re.compile(
                r'(?:weight)\s*:?\s*([^:\n]*?)(?:\n|bsa|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'bsa': re.compile(
                r'(?:bsa)\s*:?\s*([^:\n]*?)(?:\n|acquisition|$)',
                re.IGNORECASE | re.MULTILINE
            ),
            'acquisition_date': re.compile(
                r'(?:acquisition\s*date|acquisitiondate)\s*:?\s*(\d{1,2}\/\d{1,2}\/\d{4})',
                re.IGNORECASE
            ),
            'comments': re.compile(
                r'(?:comments)\s*:?\s*([^:\n]*?)(?:\n|$)',
                re.IGNORECASE | re.MULTILINE
            )
        }
        
        return patterns
    
    def parse_medical_fields(self, text: str) -> MedicalReportData:
        """
        Parse medical fields from extracted text
        
        Args:
            text: Raw text from OCR extraction
            
        Returns:
            MedicalReportData: Structured medical report data
        """
        logger.info("Parsing medical fields from extracted text")
        
        # Extract patient information
        patient_info = PatientInfo(
            name=self._extract_field('patient_name', text),
            id=self._extract_field('patient_id', text),
            sex=self._extract_field('sex', text),
            birthdate_age=self._extract_field('birthdate_age', text),
            accession_number=self._extract_field('accession_number', text),
            referring_physician=self._extract_field('referring_physician', text),
            study_id=self._extract_field('study_id', text),
            height=self._extract_field('height', text),
            weight=self._extract_field('weight', text),
            bsa=self._extract_field('bsa', text),
            acquisition_date=self._extract_field('acquisition_date', text),
            comments=self._extract_field('comments', text)
        )
        
        # Extract report details
        report_details = ReportDetails(
            user_name=self._extract_field('user_name', text),
            created_on=self._extract_field('created_on', text),
            license_id=self._extract_field('license_id', text),
            physician=self._extract_field('physician', text),
            institution_name=self._extract_field('institution_name', text),
            institution_address=self._extract_field('institution_address', text),
            department_name=self._extract_field('department_name', text)
        )
        
        # Create medical report data
        medical_data = MedicalReportData(
            patient_info=patient_info,
            report_details=report_details
        )
        
        # Log extraction results
        extracted_fields = self._count_extracted_fields(medical_data)
        logger.info(f"Successfully extracted {extracted_fields} fields from medical report")
        
        return medical_data
    
    def _extract_field(self, field_name: str, text: str) -> Optional[str]:
        """
        Extract a specific field from text using regex pattern
        
        Args:
            field_name: Name of the field to extract
            text: Text to search in
            
        Returns:
            Optional[str]: Extracted field value or None
        """
        if field_name not in self.patterns:
            return None
        
        pattern = self.patterns[field_name]
        match = pattern.search(text)
        
        if match:
            value = match.group(1).strip()
            # Clean up the extracted value
            value = re.sub(r'\s+', ' ', value)  # Replace multiple spaces with single space
            value = value.strip('.,:-')  # Remove trailing punctuation
            
            if value and len(value) > 1:  # Ensure we have meaningful content
                return value
        
        return None
    
    def _count_extracted_fields(self, medical_data: MedicalReportData) -> int:
        """
        Count the number of successfully extracted fields
        
        Args:
            medical_data: Medical report data object
            
        Returns:
            int: Number of extracted fields
        """
        count = 0
        
        # Count patient info fields
        for field_name, field_value in medical_data.patient_info.dict().items():
            if field_value is not None:
                count += 1
        
        # Count report details fields
        for field_name, field_value in medical_data.report_details.dict().items():
            if field_value is not None:
                count += 1
        
        return count

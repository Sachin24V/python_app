# Medical Report OCR Extractor API

A FastAPI-based web service that extracts structured medical data from PDF and image reports using Tesseract OCR. The system processes uploaded medical documents and returns structured data including patient information and report details.

## Features

- 🏥 **Medical Report Processing**: Extract structured data from scanned medical reports
- 📄 **Multi-format Support**: Supports PDF, PNG, JPG, and JPEG files
- 🔍 **OCR Technology**: Uses Tesseract OCR for accurate text extraction
- 📊 **Structured Output**: Returns clean JSON with patient info and report details
- 🚀 **Fast API**: Built with FastAPI for high performance and automatic documentation
- ✅ **Field Validation**: Comprehensive data validation using Pydantic models

## Extracted Fields

### Patient Information
- Patient Name
- Patient ID
- Sex/Gender
- Birthdate and Age
- Accession Number
- Referring Physician
- Study ID
- Height, Weight, BSA
- Acquisition Date
- Comments

### Report Details
- User Name
- Creation Date
- License ID
- Physician Name
- Institution Name & Address
- Department Name

## Quick Start

### Prerequisites
- Python 3.11+
- Tesseract OCR installed on your system

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/medical-ocr-extractor.git
cd medical-ocr-extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Usage

### Endpoints

- **GET** `/` - API information
- **GET** `/health` - Health check
- **POST** `/extract` - Extract medical data from uploaded file
- **GET** `/docs` - Interactive API documentation

### Extract Medical Data

**Endpoint:** `POST /extract`

**Request:**
- Content-Type: `multipart/form-data`
- Body: File upload with key `file`

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/extract" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@medical_report.pdf"
```

**Response:**
```json
{
  "patient_info": {
    "name": "DORI VANUBHAI M",
    "id": "CAG/25047/63Y",
    "sex": "Male",
    "birthdate_age": "- (-)",
    "accession_number": "A202504182017466",
    "referring_physician": "-",
    "study_id": "R202504182017466",
    "height": "-",
    "weight": "-",
    "bsa": "-",
    "acquisition_date": "4/18/2025",
    "comments": ""
  },
  "report_details": {
    "user_name": "DESKTOP-925APFBVivaanImaging",
    "created_on": "4/19/2025 11:14:39",
    "license_id": "932827031611748662",
    "physician": "DR. ALOK RANJAN/DR. VISHAL VANANI/DR. NIKITA CHATURVEDI",
    "institution_name": "KIRAN HOSPITAL SURAT",
    "institution_address": "",
    "department_name": "CATHLAB1"
  }
}
```

## Project Structure

```
medical-ocr-extractor/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic data models
├── ocr_service.py       # OCR text extraction service
├── field_parser.py      # Medical field parsing logic
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

## Architecture

- **Framework**: FastAPI with Python 3.11
- **OCR Engine**: Tesseract OCR for text extraction
- **PDF Processing**: PyMuPDF for PDF to image conversion
- **Image Processing**: Pillow for image manipulation
- **Data Validation**: Pydantic models for structured data
- **File Handling**: aiofiles for async operations

## Configuration

- **File Size Limit**: 10MB (configurable in `main.py`)
- **Supported Formats**: PDF, PNG, JPG, JPEG
- **Server Port**: 8000 (configurable)

## Error Handling

The API returns structured error responses:

```json
{
  "error": "Error message",
  "status_code": 400,
  "timestamp": "2025-06-16T10:30:00"
}
```

## Use Cases

- 🏥 **Hospital Data Entry Automation**
- 👨‍⚕️ **Patient Data Portal Backend**
- 📋 **EMR Integration**
- 🔄 **Legacy Report Digitization**

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions, please open an issue in the GitHub repository.
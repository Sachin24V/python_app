import os
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import tempfile
import logging
from typing import List

logger = logging.getLogger(__name__)

class OCRService:
    """Service for OCR text extraction from PDFs and images"""
    
    def __init__(self):
        """Initialize OCR service with Tesseract configuration"""
        # Configure Tesseract path if needed (usually not required on Linux)
        # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
        
        # OCR configuration for better medical text recognition
        self.ocr_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:-/() '
    
    def extract_text(self, file_path: str) -> str:
        """
        Extract text from PDF or image file
        
        Args:
            file_path: Path to the file to process
            
        Returns:
            str: Extracted text content
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._extract_from_pdf(file_path)
            elif file_extension in ['.png', '.jpg', '.jpeg']:
                return self._extract_from_image(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            raise
    
    def _extract_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file by converting pages to images
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            str: Extracted text from all pages
        """
        extracted_text = []
        
        try:
            # Open PDF document
            doc = fitz.open(pdf_path)
            logger.info(f"Processing PDF with {len(doc)} pages")
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Convert page to image
                mat = fitz.Matrix(2, 2)  # 2x zoom for better OCR accuracy
                pix = page.get_pixmap(matrix=mat)
                
                # Save as temporary image
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_img:
                    temp_img_path = temp_img.name
                    pix.save(temp_img_path)
                
                try:
                    # Extract text from image
                    page_text = self._extract_from_image(temp_img_path)
                    if page_text.strip():
                        extracted_text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                        logger.info(f"Extracted {len(page_text)} characters from page {page_num + 1}")
                finally:
                    # Clean up temporary image
                    if os.path.exists(temp_img_path):
                        os.unlink(temp_img_path)
            
            doc.close()
            return '\n\n'.join(extracted_text)
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise
    
    def _extract_from_image(self, image_path: str) -> str:
        """
        Extract text from image file using Tesseract OCR
        
        Args:
            image_path: Path to image file
            
        Returns:
            str: Extracted text content
        """
        try:
            # Open and preprocess image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Enhance image quality for better OCR
            image = self._preprocess_image(image)
            
            # Extract text using Tesseract
            text = pytesseract.image_to_string(image, config=self.ocr_config)
            
            logger.info(f"Extracted {len(text)} characters from image")
            return text
            
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            raise
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR results
        
        Args:
            image: PIL Image object
            
        Returns:
            Image.Image: Preprocessed image
        """
        # Convert to grayscale for better OCR
        if image.mode != 'L':
            image = image.convert('L')
        
        # Resize if image is too small (minimum 300 DPI equivalent)
        width, height = image.size
        if width < 1000 or height < 1000:
            scale_factor = max(1000 / width, 1000 / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image

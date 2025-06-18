# Contributing to Medical OCR Extractor

Thank you for your interest in contributing to the Medical OCR Extractor project! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/medical-ocr-extractor.git
   cd medical-ocr-extractor
   ```
3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Tesseract OCR installed on your system
  - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
  - **macOS**: `brew install tesseract`
  - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)

### Running the Development Server
```bash
python main.py
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## Code Style

This project follows Python best practices:

- Use **Black** for code formatting: `black .`
- Use **flake8** for linting: `flake8 .`
- Use **mypy** for type checking: `mypy .`
- Follow PEP 8 conventions
- Use type hints for all functions
- Write descriptive docstrings

## Testing

Before submitting a pull request, ensure all tests pass:

```bash
pytest
```

### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and error cases
- Mock external dependencies appropriately

## Submitting Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure they follow the coding standards

3. Add or update tests as needed

4. Update documentation if necessary

5. Commit your changes with a clear message:
   ```bash
   git commit -m "Add feature: description of what you added"
   ```

6. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

7. Create a Pull Request on GitHub

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure all checks pass (tests, linting, etc.)
- Keep PRs focused on a single feature or fix
- Update documentation as needed

## Reporting Issues

When reporting issues:

- Use a clear, descriptive title
- Provide steps to reproduce the issue
- Include relevant error messages
- Specify your environment (OS, Python version, etc.)
- Include sample files if the issue is related to OCR processing

## Feature Requests

For feature requests:

- Explain the use case and benefits
- Provide examples if possible
- Consider backwards compatibility
- Discuss implementation approach if you have ideas

## Code Organization

```
medical-ocr-extractor/
├── main.py              # FastAPI application entry point
├── models.py            # Pydantic data models
├── ocr_service.py       # OCR processing logic
├── field_parser.py      # Medical field extraction
├── utils.py             # Utility functions
├── tests/               # Test files
├── docs/                # Additional documentation
└── examples/            # Usage examples
```

## Areas for Contribution

- **OCR Accuracy**: Improve text extraction for different report formats
- **Field Parsing**: Add support for new medical field types
- **Performance**: Optimize processing speed for large files
- **Documentation**: Improve guides and examples
- **Testing**: Increase test coverage
- **Error Handling**: Better error messages and recovery
- **Security**: Input validation and security improvements

## Getting Help

- Check existing issues and discussions
- Join our community discussions
- Ask questions in issues with the "question" label

Thank you for contributing to Medical OCR Extractor!
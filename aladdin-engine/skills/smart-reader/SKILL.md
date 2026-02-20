---
name: smart-reader
description: Universal document reader with intelligent content extraction. Handles PDF, DOCX, TXT, MD, and images with OCR. Automatically extracts structured data, identifies key sections, and provides summaries. Use when Codex needs to read, analyze, or extract information from any document format including resumes, reports, contracts, and scanned documents.
---

# Smart Reader

Universal document reading and intelligent content extraction.

## Capabilities

- **PDF**: Text extraction, form data, multi-page documents
- **DOCX/DOC**: Full document parsing, tables, formatting
- **Images**: OCR text extraction (PNG, JPG, WEBP)
- **Text**: Plain text and Markdown files

## Quick Start

```python
from smart_reader import DocumentReader

reader = DocumentReader()
result = reader.read_file("document.pdf")

if result['success']:
    print(result['content'])
```

## Usage Patterns

### Extract Resume Information
```python
reader = DocumentReader()
cv = reader.read_resume("cv.pdf")
# Returns: name, email, phone, experience, education
```

### Batch Process Documents
```python
reader = DocumentReader()
results = reader.batch_process("/path/to/documents/")
```

### Extract Structured Data
```python
reader = DocumentReader()
data = reader.extract_structure("contract.docx")
# Returns: sections, tables, key-value pairs
```

## Scripts

- `scripts/document_reader.py` - Main reading engine
- `scripts/resume_parser.py` - Specialized resume/CV extraction
- `scripts/ocr_engine.py` - Image text extraction

## Installation

System dependencies:
```bash
apt-get install poppler-utils tesseract-ocr
pip install python-docx pdfplumber Pillow pytesseract
```

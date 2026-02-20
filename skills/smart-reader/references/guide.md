# Smart Reader Reference

## Supported Formats

| Format | Extension | Method | Notes |
|--------|-----------|--------|-------|
| PDF | .pdf | pdfplumber/pdftotext | Multi-page, forms |
| Word | .docx, .doc | python-docx | Tables, formatting |
| Text | .txt, .md | Direct read | UTF-8 encoding |
| Images | .png, .jpg, .webp | pytesseract | OCR required |

## Common Patterns

### Extract All Text
```python
reader = DocumentReader()
result = reader.read_file("doc.pdf")
text = result['content']
```

### Batch Processing
```python
results = reader.batch_process("/docs/")
for r in results:
    if r['success']:
        process(r['content'])
```

### Resume Parsing
```python
parser = ResumeParser()
cv = parser.parse("resume.docx")
print(cv['personal_info']['email'])
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "Unsupported format" | File extension not recognized | Check file extension |
| "OCR requires tesseract" | OCR not installed | apt install tesseract-ocr |
| "PDF extraction failed" | Encrypted/corrupted PDF | Try alternative tool |

## Installation

```bash
# System packages
sudo apt-get install poppler-utils tesseract-ocr

# Python packages
pip install python-docx pdfplumber Pillow pytesseract
```

import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\Sound Scape Equipment May 2026.pdf"

print("Checking available libraries...")
libraries = ['pypdf', 'pdfplumber', 'fitz', 'pdfminer']
available = {}
for lib in libraries:
    try:
        __import__(lib)
        available[lib] = True
        print(f"  {lib}: Available")
    except ImportError:
        available[lib] = False
        print(f"  {lib}: Not available")

if available.get('pypdf'):
    import pypdf
    print("\n--- Extracting text using pypdf ---")
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"\n--- PAGE {idx + 1} ---")
        print(text[:1000]) # Print first 1000 chars of page
elif available.get('pdfplumber'):
    import pdfplumber
    print("\n--- Extracting text using pdfplumber ---")
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Total pages: {len(pdf.pages)}")
        for idx, page in enumerate(pdf.pages):
            text = page.extract_text()
            print(f"\n--- PAGE {idx + 1} ---")
            print(text[:1000])
elif available.get('fitz'):
    import fitz # PyMuPDF
    print("\n--- Extracting text using fitz (PyMuPDF) ---")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    for idx in range(len(doc)):
        page = doc[idx]
        text = page.get_text()
        print(f"\n--- PAGE {idx + 1} ---")
        print(text[:1000])
else:
    print("\nNo specialized PDF parsing libraries found. Attempting to install pypdf...")
    # We will let the execution script run pip install if needed, or we can just try to run pip install

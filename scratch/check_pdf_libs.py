import sys

libs = ['fitz', 'pdfplumber', 'pypdf', 'PyPDF2', 'pdf2image', 'pdfimages', 'pdfminer']

print("Checking available libraries:")
for lib in libs:
    try:
        __import__(lib)
        print(f"  {lib}: AVAILABLE")
    except ImportError:
        print(f"  {lib}: NOT AVAILABLE")

print("\nChecking system tools:")
import shutil
for tool in ['pdfimages', 'pdftoppm', 'gs']:
    path = shutil.which(tool)
    print(f"  {tool}: {path if path else 'NOT FOUND'}")

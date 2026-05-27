import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = "Sound Scape Equipment May 2026.pdf"
try:
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    
    # We saw images on pages 7, 8, 9, 10, 11, 12, 13
    for page_num in range(6, min(14, len(reader.pages))):
        page = reader.pages[page_num]
        text = page.extract_text()
        print(f"\n========================================")
        print(f"PAGE {page_num + 1} TEXT:")
        print(text)
except Exception as e:
    print(f"Error reading PDF: {e}")

from pypdf import PdfReader
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = "Sound Scape Equipment May 2026.pdf"
reader = PdfReader(pdf_path)

print(f"Total Pages: {len(reader.pages)}")
for page_num, page in enumerate(reader.pages):
    print(f"\n--- PAGE {page_num + 1} ---")
    text = page.extract_text()
    if text:
        # Print first 500 characters of page text
        lines = text.strip().split('\n')
        for line in lines[:25]:
            print(f"  {line}")
        if len(lines) > 25:
            print(f"  ... ({len(lines) - 25} more lines)")
    else:
        print("  [No text found]")

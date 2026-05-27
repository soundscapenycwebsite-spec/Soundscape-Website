import sys
import os

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\Sound Scape Equipment May 2026.pdf"

try:
    import pypdf
    reader = pypdf.PdfReader(pdf_path)
    print(f"Total pages: {len(reader.pages)}")
    for idx, page in enumerate(reader.pages):
        text = page.extract_text()
        print(f"\n=================== PAGE {idx + 1} ===================")
        print(text)
except Exception as e:
    print("Error parsing PDF:", e)

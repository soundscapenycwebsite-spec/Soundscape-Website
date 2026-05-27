import sys
import re

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = "index.html"

# Detect encoding
encodings = ['utf-8', 'utf-16', 'utf-16-le', 'utf-16-be', 'latin-1']
content = None
detected_enc = None

for enc in encodings:
    try:
        with open(file_path, 'r', encoding=enc) as f:
            content = f.read()
            detected_enc = enc
            print(f"Successfully read index.html with encoding: {enc}")
            break
    except Exception:
        continue

if content is None:
    print("Failed to read index.html with any known encoding!")
    sys.exit(1)

# Find gear/image assets
print("\nScanning for images...")
matches = re.findall(r'[\'"][^\'"]*?\.(?:png|jpg|jpeg|gif|webp|svg)[\'"]', content, re.IGNORECASE)
print(f"Total image references found: {len(matches)}")
for idx, match in enumerate(matches[:30]):
    print(f"  [{idx}] {match}")

# Find any JSON blocks or catalog definitions
print("\nScanning for catalog variables...")
var_matches = re.findall(r'(?:const|let|var)\s+(\w+)\s*=', content)
print(f"Found variables: {var_matches}")

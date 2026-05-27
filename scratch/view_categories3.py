import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = "index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

found = False
for idx, line in enumerate(lines):
    if "CATEGORIES" in line:
        print(f"Line {idx+1}: {line.strip()}")
        found = True

if not found:
    print("CATEGORIES not found in lines.")

import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = "index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_line = None
for idx, line in enumerate(lines):
    if "const CATEGORIES" in line:
        start_line = idx
        break

if start_line is not None:
    print(f"CATEGORIES definition starting at line {start_line + 1}:")
    for i in range(start_line, min(start_line + 100, len(lines))):
        print(f"{i+1}: {lines[i]}", end="")
else:
    print("Could not find CATEGORIES definition!")

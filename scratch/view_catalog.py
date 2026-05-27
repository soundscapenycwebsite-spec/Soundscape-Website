import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = "index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_line = None
end_line = None

for idx, line in enumerate(lines):
    if "const GEAR_CATALOG" in line:
        start_line = idx
    if start_line is not None and "];" in line and idx > start_line:
        end_line = idx
        break

if start_line is not None and end_line is not None:
    print(f"GEAR_CATALOG starts at line {start_line + 1} and ends at line {end_line + 1}:")
    for i in range(start_line, end_line + 1):
        print(f"{i+1}: {lines[i]}", end="")
else:
    print("Could not find GEAR_CATALOG definition!")

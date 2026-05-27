import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

file_path = "index.html"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

script_start = None
for idx, line in enumerate(lines):
    if "<script>" in line:
        script_start = idx
    if script_start is not None and "const GEAR_CATALOG" in line:
        break

if script_start is not None:
    print(f"Script tag starts at line {script_start + 1}:")
    for i in range(script_start, min(script_start + 200, len(lines))):
        print(f"{i+1}: {lines[i]}", end="")
else:
    print("Could not find script start!")

import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = "assets"
if os.path.exists(assets_dir):
    print("Files in assets/:")
    for f in sorted(os.listdir(assets_dir)):
        p = os.path.join(assets_dir, f)
        if os.path.isfile(p):
            print(f"  {f} - {os.path.getsize(p)} bytes")
else:
    print("assets/ directory does not exist!")

import os
import re
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

html_path = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\index.html"
assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

# Read HTML and find GEAR_CATALOG array
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# We want to parse the GEAR_CATALOG array
catalog_match = re.search(r'const GEAR_CATALOG = \[(.*?)\];', content, re.DOTALL)
if not catalog_match:
    print("Could not find GEAR_CATALOG in HTML.")
    sys.exit(1)

catalog_text = catalog_match.group(1)

# Find all blocks like { id: "...", name: "...", ..., image: "..." }
items = []
blocks = re.findall(r'\{(.*?)\}', catalog_text, re.DOTALL)
print(f"Parsed {len(blocks)} items from GEAR_CATALOG in HTML.")

for block in blocks:
    item_id_m = re.search(r'id:\s*["\'](.*?)["\']', block)
    name_m = re.search(r'name:\s*["\'](.*?)["\']', block)
    image_m = re.search(r'image:\s*["\'](.*?)["\']', block)
    
    item_id = item_id_m.group(1) if item_id_m else "unknown"
    name = name_m.group(1) if name_m else "unknown"
    image = image_m.group(1) if image_m else "none"
    
    image_filename = os.path.basename(image) if image != "none" else ""
    image_path = os.path.join(assets_dir, image_filename) if image_filename else ""
    
    exists = os.path.exists(image_path) if image_path else False
    size = os.path.getsize(image_path) if exists else 0
    
    items.append({
        'id': item_id,
        'name': name,
        'image': image,
        'filename': image_filename,
        'exists': exists,
        'size': size
    })

print("\n--- Image Status Report ---")
missing_count = 0
for item in items:
    if item['image'] == 'none':
        print(f"[MISSING] {item['name']} ({item['id']}): No image defined")
        missing_count += 1
    elif not item['exists']:
        print(f"[NOT_FOUND] {item['name']} ({item['id']}): Image '{item['image']}' does NOT exist!")
        missing_count += 1
    elif item['size'] < 1000:
        print(f"[WARNING] {item['name']} ({item['id']}): Image '{item['image']}' is extremely small ({item['size']} bytes)")
        missing_count += 1
    else:
        print(f"[OK] {item['name']} ({item['id']}): {item['image']} ({item['size']} bytes)")

print(f"\nTotal items: {len(items)}")
print(f"Total problematic images: {missing_count}")

import urllib.request
import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Distributing entirely distinct stage/light scenes to guarantee zero image size collisions:
# 1. Concert Stage Platform -> A gorgeous wide concert stage with bright strobe lights
# 2. Scenic Wash Bar -> A vibrant multicolor wash lighting show scene
items = {
    "gear_steeldeck_platform.jpg": "https://images.unsplash.com/photo-1501386761578-eac5c94b800a?q=80&w=600&auto=format&fit=crop", # Vibrant stadium stage deck view
    "gear_washers12.jpg": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=600&auto=format&fit=crop" # Scenic multicolour stage wash
}

print("=== FIXING ALL COLLIDING SIZES ===")
for filename, url in items.items():
    dest_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            content = response.read()
            with open(dest_path, 'wb') as f:
                f.write(content)
            print(f"  [SUCCESS] Overwritten {filename} with unique image ({len(content)} bytes)!")
    except Exception as e:
        print(f"  [FAILED] {filename}: {e}")

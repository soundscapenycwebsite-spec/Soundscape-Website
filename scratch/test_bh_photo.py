import urllib.request
import sys
import os

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

products = {
    "gear_mesh_facade.jpg": "1018861",
    "gear_odyssey48.jpg": "1042732",
    "gear_proxvista.jpg": "1669460",
    "gear_co2cannon.jpg": "1221764",
    "gear_steeldeck_booth.jpg": "1647466",
    "gear_steeldeck_platform.jpg": "1792683",
    "gear_totem8ft.jpg": "1498687",
    "gear_totem6ft.jpg": "1498686",
    "gear_co2_gun.jpg": "1460515"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
}

os.makedirs("assets", exist_ok=True)

for name, pid in products.items():
    url = f"https://static.bhphotovideo.com/images/images500x500/{pid}.jpg"
    print(f"Testing {name} (B&H ID: {pid})...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read()
            # Save temporary file to verify size
            temp_path = os.path.join("assets", f"temp_{name}")
            with open(temp_path, "wb") as f:
                f.write(data)
            print(f"  [SUCCESS] Downloaded {len(data)} bytes from {url}")
            # Clean up temp
            os.remove(temp_path)
    except Exception as e:
        print(f"  [FAILED] Error: {e} for {url}")

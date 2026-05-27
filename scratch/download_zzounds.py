import urllib.request
import urllib.parse
import re
import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

os.makedirs("assets", exist_ok=True)

items = {
    "gear_mesh_facade.jpg": "https://www.zzounds.com/item--ODYSWF7246B",
    "gear_odysseymedia.jpg": "https://www.zzounds.com/item--ODYDJBOOTHM78",
    "gear_odyssey48.jpg": "https://www.zzounds.com/item--ODYSWF4846B",
    "gear_proxvista.jpg": "https://www.zzounds.com/item--PRXXFMESAMEDIAMK2",
    "gear_command_booth.jpg": "https://www.zzounds.com/item--PRXXSDJDKBL",
    "gear_totem8ft.jpg": "https://www.zzounds.com/item--PRXXTTOTEM8FT",
    "gear_totem6ft.jpg": "https://www.zzounds.com/item--PRXXTTOTEM6FT",
    "gear_co2cannon.jpg": "https://www.zzounds.com/item--ADJCO2JET"
}

def download_item(filename, url):
    print(f"\nFetching product page: {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Look for main product image. zZounds stores image URLs inside data-zoom-src or main-image class, or matching images.zzounds.com
            # Let's search for any image in zzounds.com/media/
            images = re.findall(r'(https://images\.zzounds\.com/media/[^"\']+\.(?:jpg|png|jpeg))', html)
            if not images:
                # Try relative images
                images = re.findall(r'src=["\'](/media/[^"\']+\.(?:jpg|png|jpeg))["\']', html)
                images = ["https://images.zzounds.com" + img for img in images]
            
            # Filter for larger images (usually contain 'large' or 'front' or 'main' or are simply not thumbs)
            clean_images = []
            for img in images:
                img_lower = img.lower()
                if "thumb" in img_lower or "icon" in img_lower or "logo" in img_lower:
                    continue
                clean_images.append(img)
            
            if clean_images:
                # Take the first matched image (zZounds serves main front view first)
                img_url = clean_images[0]
                print(f"  Found image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                    img_data = img_resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"  [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
                    return True
            else:
                print("  [FAILED] No images found on zZounds product page.")
    except Exception as e:
        print(f"  [FAILED] Error: {e}")
    return False

# Run zZounds downloader
for filename, url in items.items():
    download_item(filename, url)

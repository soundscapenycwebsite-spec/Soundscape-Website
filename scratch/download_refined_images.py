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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

targets = {
    "gear_mesh_facade.jpg": "Odyssey SWF7246B Scrim Werks DJ Facade black",
    "gear_odysseymedia.jpg": "Odyssey DJBOOTHM78 DJ Booth screen table",
    "gear_odyssey48.jpg": "Odyssey SWF4846B Scrim Werks DJ Facade black",
    "gear_proxvista.jpg": "ProX Mesa DJ Facade workstation XF-MESA-B",
    "gear_command_booth.jpg": "ProX Command Center DJ booth table XS-DJDK",
    "gear_totem8ft.jpg": "ProX XT-TOTEM8FT 8ft vertical truss pillar F34",
    "gear_totem6ft.jpg": "ProX XT-TOTEM6FT 6ft vertical truss pillar F34",
    "gear_co2cannon.jpg": "ADJ CO2 Jet DMX special FX floor blower",
    "gear_co2_gun.jpg": "CryoFX Handheld CO2 Gun blaster stage"
}

# Strict blacklist of words to avoid funny false positives
blacklist = ["honda", "car", "minivan", "duck", "cow", "toy", "cartoon", "vector", "drawing", "illustration", "vaca", "patinho", "desenho"]

os.makedirs("assets", exist_ok=True)

for filename, query in targets.items():
    print(f"\nSearching Bing for '{query}'...")
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract murl parameter
            img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if not img_urls:
                img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            
            # Filter URLs
            clean_urls = []
            for img in img_urls:
                img_lower = img.lower()
                # Skip thumbnails/encrypted images
                if "tbn" in img_lower or "encrypted" in img_lower:
                    continue
                # Skip blacklisted words
                if any(bad in img_lower for bad in blacklist):
                    continue
                clean_urls.append(img)
            
            if clean_urls:
                img_url = clean_urls[0]
                print(f"  Selected image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                    img_data = img_resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"  [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
            else:
                print("  [FAILED] No clean product images found after blacklisting.")
    except Exception as e:
        print(f"  [FAILED] Error: {e}")

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
    "gear_mesh_facade.jpg": "Odyssey SWF7246BLK Scrim Werks",
    "gear_odysseymedia.jpg": "Odyssey DJBOOTHM78 Folding DJ Booth",
    "gear_odyssey48.jpg": "Odyssey SWF4846BLK Scrim Werks",
    "gear_proxvista.jpg": "ProX XF-MESA-MEDIA-MK2 Mesa DJ Facade",
    "gear_command_booth.jpg": "ProX XS-DJDKBL Command Center DJ Booth",
    "gear_totem8ft.jpg": "ProX XT-TOTEM8FT 8ft Truss Totem",
    "gear_totem6ft.jpg": "ProX XT-TOTEM6FT 6ft Truss Totem",
    "gear_co2cannon.jpg": "ADJ CO2 Jet DMX machine",
    "gear_co2_gun.jpg": "CryoFX Handheld CO2 Gun"
}

os.makedirs("assets", exist_ok=True)

for filename, query in targets.items():
    print(f"\nSearching Bing for '{query}'...")
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Bing encodes direct image URLs in murl parameter inside m="" attribute
            img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if not img_urls:
                # Fallback to general http links ending in jpg/png
                img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            
            # Filter for reputable retail domains if possible
            clean_urls = []
            for img in img_urls:
                img_lower = img.lower()
                # Skip thumbnails or suspicious links
                if "tbn" in img_lower or "encrypted" in img_lower:
                    continue
                if any(domain in img_lower for domain in ["sweetwater.com", "bhphotovideo.com", "kpodj.com", "planetdj.com", "proxdirect.com", "odysseygear.com", "avmaxx.com", "reverb.com", "ebayimg.com", "cryofx.com", "adj.com", "americanmusical.com", "zzounds.com", "fullcompass.com"]):
                    clean_urls.append(img)
            
            # If no clean domains, use first available direct link
            if not clean_urls:
                clean_urls = [u for u in img_urls if not ("tbn" in u or "encrypted" in u)]
                
            if clean_urls:
                img_url = clean_urls[0]
                print(f"  Found image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                    img_data = img_resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"  [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
            else:
                print("  [FAILED] No product images found in Bing HTML.")
    except Exception as e:
        print(f"  [FAILED] Error: {e}")

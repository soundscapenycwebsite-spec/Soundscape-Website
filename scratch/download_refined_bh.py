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
    "gear_mesh_facade.jpg": "Odyssey SWF7246B Scrim Werks 72x46 DJ Facade black",
    "gear_odysseymedia.jpg": "Odyssey DJBOOTHM78 folding DJ workstation table",
    "gear_odyssey48.jpg": "Odyssey SWF4846B Scrim Werks 48x46 DJ Facade black",
    "gear_proxvista.jpg": "ProX Mesa DJ Facade workstation XF-MESA-B table",
    "gear_command_booth.jpg": "ProX Command Center DJ booth table XS-DJDKBL"
}

os.makedirs("assets", exist_ok=True)

for filename, query in targets.items():
    print(f"\nSearching Bing for '{query}' from B&H...")
    # Add site:bhphotovideo.com to query to get B&H's exact index page, which points to the CDN image!
    search_query = f"{query} site:bhphotovideo.com"
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(search_query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract murl parameter (original image URL)
            img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if not img_urls:
                img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            
            # Filter URLs containing bhphotovideo or bhphoto
            clean_urls = []
            for img in img_urls:
                img_lower = img.lower()
                if "bhphoto" in img_lower or "bhphotovideo" in img_lower:
                    clean_urls.append(img)
            
            # If no B&H image was directly indexed, try any reputable store (like planetdj, Sweetwater, Reverb, etc.)
            if not clean_urls:
                print("  No direct B&H image URL found in search index, expanding filters...")
                for img in img_urls:
                    img_lower = img.lower()
                    if "tbn" in img_lower or "encrypted" in img_lower:
                        continue
                    if any(x in img_lower for x in ["planetdj", "vipproaudio", "sweetwater", "reverb", "zzounds", "americanmusical", "proxdirect", "odysseygear", "hollywooddj", "idjnow"]):
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
                print("  [FAILED] No clean product images found from B&H or trusted sellers.")
    except Exception as e:
        print(f"  [FAILED] Error: {e}")

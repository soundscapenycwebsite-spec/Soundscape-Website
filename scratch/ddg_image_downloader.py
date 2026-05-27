import urllib.request
import urllib.parse
import re
import os
import sys
import json

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

os.makedirs("assets", exist_ok=True)

targets = {
    "gear_mesh_facade.jpg": "Odyssey SWF7246B Scrim Werks Facade black",
    "gear_odysseymedia.jpg": "Odyssey DJBOOTHM78 Folding DJ Booth",
    "gear_odyssey48.jpg": "Odyssey SWF4846B Scrim Werks Facade black",
    "gear_proxvista.jpg": "ProX XF-MESAMEDIAMK2 Mesa DJ Facade black",
    "gear_command_booth.jpg": "ProX XS-DJDKBL Command Center DJ Booth black",
    "gear_totem8ft.jpg": "ProX XT-TOTEM8FT 8ft Truss Totem",
    "gear_totem6ft.jpg": "ProX XT-TOTEM6FT 6ft Truss Totem",
    "gear_co2cannon.jpg": "ADJ CO2 Jet DMX machine floor mounted",
    "gear_co2_gun.jpg": "CryoFX Handheld CO2 Gun Blaster"
}

def search_and_download(filename, query):
    print(f"\nSearching DDG for '{query}'...")
    # Use DDG HTML search
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Look for image links or standard web links to extract clean images
            # Let's search for image urls in the HTML using regex
            links = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            if not links:
                # Fallback search for general links that might contain images
                links = re.findall(r'https?://[^\s"\'&]+', html)
            
            # Filter links to find high-res images from known clean domains (sweetwater, bhphoto, kpodj, planetdj, prox, odyssey, etc.)
            clean_links = []
            for link in links:
                link = link.lower()
                if any(domain in link for domain in ["sweetwater.com", "bhphotovideo.com", "kpodj.com", "planetdj.com", "proxdirect.com", "odysseygear.com", "avmaxx.com", "reverb.com", "ebayimg.com", "cryofx.com", "adj.com", "americanmusical.com", "zzounds.com"]):
                    if link.endswith(('.jpg', '.jpeg', '.png')):
                        clean_links.append(link)
            
            # If no clean domains matched, just use any direct jpg/png link
            if not clean_links:
                clean_links = [l for l in links if l.endswith(('.jpg', '.jpeg', '.png'))]
            
            if clean_links:
                # Take the first one and download
                img_url = clean_links[0]
                print(f"  Found image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                    img_data = img_resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"  [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
                    return True
            else:
                print("  [FAILED] No clean image links found in DDG search results.")
    except Exception as e:
        print(f"  [FAILED] Error: {e}")
    return False

# Also compile a list of fallback URLs that we know are absolute public direct links to these items
direct_fallbacks = {
    "gear_co2cannon.jpg": [
        "https://www.adj.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/c/o/co2_jet.jpg",
        "https://adj-public.s3.amazonaws.com/media/catalog/product/c/o/co2_jet.jpg"
    ],
    "gear_co2_gun.jpg": [
        "https://cryofx.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/c/r/cryofx-cryo-gun-co2-cannon.jpg",
        "https://www.cryofx.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/c/r/cryofx-cryo-gun-co2-cannon.jpg"
    ],
    "gear_mesh_facade.jpg": [
        "https://www.odysseygear.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/s/w/swf7246blk.jpg"
    ],
    "gear_odysseymedia.jpg": [
        "https://www.odysseygear.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/d/j/djboothm78.jpg"
    ],
    "gear_odyssey48.jpg": [
        "https://www.odysseygear.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/s/w/swf4846blk.jpg"
    ]
}

# Run search-based downloader first
for filename, query in targets.items():
    success = search_and_download(filename, query)
    if not success and filename in direct_fallbacks:
        print(f"  Attempting direct fallbacks for {filename}...")
        for url in direct_fallbacks[filename]:
            print(f"    Trying direct URL: {url}")
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    img_data = resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"    [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
                    break
            except Exception as e:
                print(f"    [FAILED] Error: {e}")

import urllib.request
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

urls = {
    "gear_mesh_facade.jpg": "https://www.vipproaudio.com/products/odyssey-swf7246b-scrim-werks-72-wide-x-46-high-folding-dj-facade",
    "gear_odyssey48.jpg": "https://www.vipproaudio.com/products/odyssey-swf4846b-scrim-werks-48-wide-x-46-high-folding-dj-facade",
    "gear_proxvista.jpg": "https://www.vipproaudio.com/products/prox-xf-vista-dj-booth-workstation-with-mesh-scrims",
    "gear_command_booth.jpg": "https://www.vipproaudio.com/products/prox-xs-djdkbl-command-center-dj-booth"
}

def download_booth(filename, url):
    print(f"\nFetching VIP Pro Audio page: {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Shopify pages host images on cdn.shopify.com/s/files/...
            images = re.findall(r'(https://cdn\.shopify\.com/s/files/[^"\']+\.(?:jpg|png|jpeg))', html)
            if not images:
                # Relative or general shopify CDN links
                images = re.findall(r'(//cdn\.shopify\.com/[^"\']+\.(?:jpg|png|jpeg))', html)
                images = ["https:" + img for img in images]
                
            clean_images = []
            for img in images:
                img_lower = img.lower()
                # Exclude logos, banners, thumbnails
                if any(x in img_lower for x in ["logo", "icon", "banner", "thumb", "small", "62x", "48x", "96x", "150x"]):
                    continue
                # Make sure it's a main product image (usually has /products/ in URL)
                if "/products/" in img_lower:
                    clean_images.append(img)
            
            # Fallback to any product image
            if not clean_images:
                clean_images = [img for img in images if not any(x in img.lower() for x in ["logo", "icon", "banner"])]
                
            if clean_images:
                # Remove shopify sizing queries if any (e.g. _1024x1024.jpg?v=...) to get ultra-high-res image
                img_url = clean_images[0]
                img_url = re.sub(r'_[0-9]+x[0-9]*\.', '.', img_url) # remove sizes like _480x.
                img_url = re.sub(r'_[0-9]+x\.', '.', img_url)
                print(f"  Selected image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                    img_data = img_resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"  [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
                    return True
            else:
                print("  [FAILED] No product images found on Shopify HTML page.")
    except Exception as e:
        print(f"  [FAILED] Error: {e}")
    return False

for filename, url in urls.items():
    download_booth(filename, url)

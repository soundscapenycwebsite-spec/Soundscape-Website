import urllib.request
import urllib.parse
import re
import os
import sys
import time

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

light_targets = [
    {
        "id": "movingheads450",
        "query": "site:sweetwater.com Chauvet DJ Intimidator Spot 375Z",
        "filename": "gear_moving_heads450.jpg"
    },
    {
        "id": "intimidatorspot200",
        "query": "site:sweetwater.com Chauvet DJ Intimidator Spot 260",
        "filename": "gear_intimidatorspot200.jpg"
    },
    {
        "id": "intimidatorbeam100",
        "query": "site:sweetwater.com Chauvet DJ Intimidator Beam 355",
        "filename": "gear_intimidatorbeam100.jpg"
    },
    {
        "id": "jmswebbmover",
        "query": "site:sweetwater.com Chauvet DJ Rogue R2X Wash",
        "filename": "gear_jmswebbmover.jpg"
    },
    {
        "id": "beam275",
        "query": "site:sweetwater.com Chauvet DJ Intimidator Beam",
        "filename": "gear_beam275.jpg"
    },
    {
        "id": "washerhead",
        "query": "site:sweetwater.com Chauvet DJ wash moving head",
        "filename": "gear_washerhead.jpg"
    },
    {
        "id": "motionstrip",
        "query": "site:sweetwater.com Chauvet DJ COLORband Pix",
        "filename": "gear_motionstrip.jpg"
    },
    {
        "id": "laser12w",
        "query": "site:sweetwater.com Chauvet DJ laser light",
        "filename": "gear_laser12w.jpg"
    },
    {
        "id": "uplights",
        "query": "site:sweetwater.com Chauvet DJ Freedom Par",
        "filename": "gear_uplight.jpg"
    },
    {
        "id": "washers12",
        "query": "site:sweetwater.com Chauvet DJ SlimPAR",
        "filename": "gear_washers12.jpg"
    },
    {
        "id": "barwash43",
        "query": "site:sweetwater.com Chauvet DJ COLORband",
        "filename": "gear_barwash43.jpg"
    },
    {
        "id": "gigbar2",
        "query": "site:sweetwater.com Chauvet DJ GigBAR Move",
        "filename": "gear_gigbar.jpg"
    },
    {
        "id": "stageplatforms",
        "query": "site:sweetwater.com Gator Frameworks stage platform",
        "filename": "gear_stage_platform.jpg"
    },
    {
        "id": "steeldeckbooth",
        "query": "site:sweetwater.com Gator Frameworks Utility Table",
        "filename": "gear_steeldeck_booth.jpg"
    },
    {
        "id": "command53",
        "query": "site:sweetwater.com Fastfold folding DJ table",
        "filename": "gear_command_booth.jpg"
    },
    {
        "id": "odysseymedia",
        "query": "site:sweetwater.com Gator Frameworks DJ Facade",
        "filename": "gear_odysseymedia.jpg"
    }
]

os.makedirs("assets", exist_ok=True)

def find_sweetwater_url(query):
    # Search Bing for the Sweetwater store URL
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract sweetwater.com/store/detail URLs
            urls = re.findall(r'(https://www\.sweetwater\.com/store/detail/[a-zA-Z0-9\-_]+)', html)
            if urls:
                return urls[0]
    except Exception as e:
        print(f"  Search failed: {e}")
    return None

def download_product_image(sw_url, filename):
    req = urllib.request.Request(sw_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Look for Sweetwater product images (typically media.sweetwater.com/m/products/image/ or similar)
            images = re.findall(r'(https://media\.sweetwater\.com/[^"\']+\.(?:jpg|png|jpeg))', html)
            if not images:
                images = re.findall(r'(https://[^"\']+/images/items/[^"\']+\.(?:jpg|png|jpeg))', html)
            
            # Filter out icons, favicons, backgrounds, logos
            clean_images = []
            for img in images:
                img_lower = img.lower()
                if "app-icons" in img_lower or "favicon" in img_lower or "logo" in img_lower or "banner" in img_lower or "pattern" in img_lower or "background" in img_lower or "snow" in img_lower:
                    continue
                clean_images.append(img)
            
            if clean_images:
                # Prioritize large images
                large_img = [i for i in clean_images if "large" in i.lower()]
                img_url = large_img[0] if large_img else clean_images[0]
                
                print(f"  Downloading: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=12) as img_resp:
                    img_data = img_resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"  [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
                    return True
            else:
                print("  No product images found on page.")
    except Exception as e:
        print(f"  Failed download: {e}")
    return False

for target in light_targets:
    print(f"\n========================================")
    print(f"Processing: {target['id']}")
    print(f"Querying Sweetwater page for: '{target['query']}'")
    
    sw_url = find_sweetwater_url(target['query'])
    if sw_url:
        print(f"Found Sweetwater page: {sw_url}")
        success = download_product_image(sw_url, target['filename'])
        if not success:
            print("Failed to download image from product page.")
    else:
        print("Could not find Sweetwater product page via search.")
    
    time.sleep(1)

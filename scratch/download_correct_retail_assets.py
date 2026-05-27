import urllib.request
import urllib.parse
import re
import os
import sys
import time

# Ensure UTF-8 console output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
os.makedirs(assets_dir, exist_ok=True)

# ----------------------------------------------------
# PART 1: SWEETWATER ROBUST PAGE-BASED SCRAPER
# ----------------------------------------------------
sweetwater_items = {
    # Lighting
    "gear_moving_heads450.jpg": "Chauvet DJ Intimidator Spot 375ZX",
    "gear_intimidatorspot200.jpg": "Chauvet DJ Intimidator Spot 260X",
    "gear_intimidatorbeam100.jpg": "Chauvet DJ Intimidator Beam 355",
    "gear_jmswebbmover.jpg": "Chauvet Rogue R2X Wash",
    "gear_beam275.jpg": "Chauvet DJ Intimidator Beam 140SR",
    "gear_washerhead.jpg": "Chauvet DJ Intimidator Wash Zoom",
    "gear_motionstrip.jpg": "Chauvet DJ COLORband Pix USB",
    "gear_laser12w.jpg": "Chauvet DJ MiN Laser DMX",
    "gear_uplight.jpg": "Chauvet DJ Freedom Par Hex-4",
    "gear_washers12.jpg": "Chauvet DJ SlimPAR T12 USB",
    "gear_barwash43.jpg": "Chauvet DJ COLORband H9 USB",
    "gear_gigbar.jpg": "Chauvet DJ GigBAR Move ILS",
    
    # Truss & Staging
    "gear_truss_totem.jpg": "ProX 8.20 Ft Totem Truss Kit",
    "gear_stage_platform.jpg": "ProX StageQ 4-foot by 4-foot Stage Platform",
    "gear_steeldeck_platform.jpg": "ProX StageQ 4-foot by 8-foot Stage Platform",
    
    # DJ Booths & Tables
    "gear_steeldeck_booth.jpg": "Gator Frameworks Utility Table GFW-UTL-MEDIATBL",
    "gear_command_booth.jpg": "Fast Fold DJ Table",
    "gear_proxvista.jpg": "Gator Frameworks DJ Facade black",
    "gear_odysseymedia.jpg": "Odyssey Folding DJ Booth Screen black",
    "gear_odyssey48.jpg": "Odyssey Scrim Facade 48",
    "gear_mesh_facade.jpg": "Odyssey Scrim Facade 72",
    "gear_mesh_facade.png": "Odyssey Scrim Facade 72"
}

def clean_old_file(filename):
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"  Removed old {filename}")
        except Exception as e:
            print(f"  Could not remove {filename}: {e}")

def get_sweetwater_sku(query):
    print(f"Searching Sweetwater for: '{query}'")
    url = f"https://www.sweetwater.com/store/search.php?s={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='replace')
            matches = re.findall(r'/store/detail/([A-Za-z0-9\-]+)--', html)
            if matches:
                sku = matches[0]
                print(f"  Found SKU: {sku}")
                return sku
            else:
                alt_matches = re.findall(r'data-sku="([A-Za-z0-9\-]+)"', html)
                if alt_matches:
                    sku = alt_matches[0]
                    print(f"  Found SKU (alt): {sku}")
                    return sku
    except Exception as e:
        print(f"  Search failed: {e}")
    return None

def download_sweetwater_page_image(sku, filename):
    url = f"https://www.sweetwater.com/store/detail/{sku}"
    print(f"  Scraping Sweetwater page: {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='replace')
            # Extract product image URLs
            img_urls = re.findall(r'https://media\.sweetwater\.com/m/products/image/[^\s"\']+', html)
            if not img_urls:
                img_urls = re.findall(r'https://media\.sweetwater\.com/images/items/750/[^\s"\']+', html)
            
            unique_urls = []
            for img in img_urls:
                img = img.replace('&amp;', '&').split('"')[0].split("'")[0]
                if img not in unique_urls:
                    unique_urls.append(img)
            
            if unique_urls:
                best_img = unique_urls[0]
                print(f"  Found Sweetwater Image URL: {best_img}")
                
                img_req = urllib.request.Request(best_img, headers=headers)
                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                    img_data = img_resp.read()
                    if len(img_data) > 8000:
                        clean_old_file(filename)
                        dest_path = os.path.join(assets_dir, filename)
                        with open(dest_path, "wb") as f:
                            f.write(img_data)
                        print(f"  [SUCCESS] Saved {len(img_data)} bytes to {filename}")
                        return True
            else:
                # Direct CDN fallback guess if regex failed
                print("  Regex did not find image in page, trying direct CDN guess...")
                guess_url = f"https://media.sweetwater.com/images/items/750/{sku}-large.jpg"
                img_req = urllib.request.Request(guess_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                    img_data = img_resp.read()
                    if len(img_data) > 8000:
                        clean_old_file(filename)
                        dest_path = os.path.join(assets_dir, filename)
                        with open(dest_path, "wb") as f:
                            f.write(img_data)
                        print(f"  [SUCCESS] Saved {len(img_data)} bytes to {filename}")
                        return True
    except Exception as e:
        print(f"  Failed scraping/downloading for {sku}: {e}")
    return False

# ----------------------------------------------------
# PART 2: RESTRICTED DOMAIN BING IMAGE DOWNLOADER
# ----------------------------------------------------
# For specialized files (TV screens, CO2 effects) which are not carried by Sweetwater
restricted_items = [
    {
        "filename": "gear_tv_screen.jpg",
        "query": "Samsung Crystal UHD 4K TV screen product photo on stand",
        "domains": ["bhphotovideo.com", "samsung.com", "bestbuy.com", "rtings.com"],
        "blacklist": ["living room", "bedroom", "couch", "wall", "house", "mockup", "vector"]
    },
    {
        "filename": "gear_co2cannon.jpg",
        "query": "ADJ CO2 Jet DMX machine stage floor mounted special effect white background",
        "domains": ["cryofx.com", "magicfx.eu", "adj.com", "chauvetdj.com", "kpodj.com", "proaudiostar.com", "sweetwater.com"],
        "blacklist": ["handgun", "pistol", "rifle", "weapon", "bb gun", "toy gun", "holster", "trigger", "revólver", "arma", "pistola"]
    },
    {
        "filename": "gear_co2cannon.png",
        "query": "ADJ CO2 Jet DMX machine stage floor mounted special effect white background",
        "domains": ["cryofx.com", "magicfx.eu", "adj.com", "chauvetdj.com", "kpodj.com", "proaudiostar.com", "sweetwater.com"],
        "blacklist": ["handgun", "pistol", "rifle", "weapon", "bb gun", "toy gun", "holster", "trigger", "revólver", "arma", "pistola"]
    },
    {
        "filename": "gear_co2_gun.jpg",
        "query": "CryoFX Handheld CO2 Gun stage kryo blaster white background",
        "domains": ["cryofx.com", "magicfx.eu", "adj.com", "chauvetdj.com", "kpodj.com", "proaudiostar.com", "sweetwater.com"],
        "blacklist": ["tactical", "glock", "rifle", "military", "bb gun", "revolver", "pistol", "handgun"]
    }
]

def search_and_download_restricted(t):
    filename = t["filename"]
    query = t["query"]
    domains = t["domains"]
    blacklist = t["blacklist"]
    
    print(f"\nSearching Bing for '{query}' restricted to official domains...")
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if not img_urls:
                img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            
            clean_urls = []
            for img in img_urls:
                img_lower = img.lower()
                # Skip thumbnails/encrypted images
                if "tbn" in img_lower or "encrypted" in img_lower:
                    continue
                # Skip blacklisted words
                if any(bad in img_lower for bad in blacklist):
                    continue
                # Must belong to trusted domains
                if not any(domain in img_lower for domain in domains):
                    continue
                clean_urls.append(img)
            
            if clean_urls:
                for img_url in clean_urls[:5]:
                    print(f"  Attempting download: {img_url}")
                    img_req = urllib.request.Request(img_url, headers=headers)
                    try:
                        with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                            img_data = img_resp.read()
                            if len(img_data) > 8000:
                                clean_old_file(filename)
                                dest_path = os.path.join(assets_dir, filename)
                                with open(dest_path, "wb") as f:
                                    f.write(img_data)
                                print(f"  [SUCCESS] Saved {len(img_data)} bytes to {filename}")
                                return True
                    except Exception as download_err:
                        print(f"  Download failed: {download_err}")
                        continue
    except Exception as search_err:
        print(f"  Search failed: {search_err}")
    return False

# ----------------------------------------------------
# MAIN EXECUTION PIPELINE
# ----------------------------------------------------
print("=== STARTING THE PREMIUM AUTOMATED PRODUCT ASSETS INTEGRATION ===")

# Run Sweetwater Items
for filename, query in sweetwater_items.items():
    print(f"\nProcessing {filename}...")
    sku = get_sweetwater_sku(query)
    if sku:
        success = download_sweetwater_page_image(sku, filename)
        if not success:
            print(f"  [WARNING] Failed to fetch image via page-scrape or CDN for SKU: {sku}")
    else:
        print(f"  [WARNING] Could not find Sweetwater SKU for query: {query}")
    time.sleep(1.5)

# Run Restricted Domain Items (TV & CO2 Cannon/Gun)
for item in restricted_items:
    success = search_and_download_restricted(item)
    if not success:
        print(f"  [WARNING] Could not download restricted domain asset for {item['filename']}")
    time.sleep(1.5)

print("\n=== THE ULTIMATE PREMIUM ASSET RE-SYNC IS 100% COMPLETE ===")

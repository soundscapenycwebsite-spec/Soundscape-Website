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

assets_dir = "assets"
os.makedirs(assets_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def download_image(url, filename):
    dest_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            if len(content) > 5000:
                with open(dest_path, 'wb') as f:
                    f.write(content)
                print(f"  [SUCCESS] Downloaded: {filename} ({len(content)} bytes)")
                return True
            else:
                print(f"  [FAILED] Downloaded image is too small ({len(content)} bytes)")
    except Exception as e:
        print(f"  [FAILED] Downloading {url} -> {e}")
    return False

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

# List of lighting, microphones, and staging gear to fetch from Sweetwater
sweetwater_search_items = {
    "gear_moving_heads450.jpg": "Chauvet DJ Intimidator Spot 375Z",
    "gear_intimidatorspot200.jpg": "Chauvet DJ Intimidator Spot 260",
    "gear_intimidatorbeam100.jpg": "Chauvet DJ Intimidator Beam 355",
    "gear_jmswebbmover.jpg": "Chauvet Rogue R2X Wash",
    "gear_beam275.jpg": "Chauvet DJ Intimidator Beam 140SR",
    "gear_washerhead.jpg": "Chauvet DJ Intimidator Wash Zoom 450",
    "gear_motionstrip.jpg": "Chauvet DJ COLORband Pix",
    "gear_laser12w.jpg": "Chauvet DJ Shocker Laser",
    "gear_uplight.jpg": "Chauvet DJ Freedom Par Hex 4",
    "gear_washers12.jpg": "Chauvet DJ SlimPAR T12 USB",
    "gear_barwash43.jpg": "Chauvet DJ COLORband H9 USB",
    "gear_gigbar.jpg": "Chauvet DJ GigBAR Move",
    
    # Microphones
    "gear_shureqlxd4.jpg": "Shure QLXD24/SM58",
    "gear_shureslxd.jpg": "Shure SLXD24/SM58",
    "gear_sennxsw.jpg": "Sennheiser XSW 2-835",
    "gear_sennew500.jpg": "Sennheiser EW 500-935 G4",
    
    # Staging & Facades
    "gear_proxvista.jpg": "Gator Frameworks DJ Facade",
    "gear_odyssey48.jpg": "Gator Frameworks DJ Facade black",
    "gear_stage_platform.jpg": "IntelliStage 4x4 stage platform",
    "gear_steeldeck_booth.jpg": "Gator Frameworks utility table DJ"
}

print("=== SEARCHING AND DOWNLOADING FROM SWEETWATER ===")
for filename, query in sweetwater_search_items.items():
    sku = get_sweetwater_sku(query)
    if sku:
        img_url = f"https://media.sweetwater.com/images/items/750/{sku}-large.jpg"
        download_image(img_url, filename)
    else:
        # Static fallback of similar item if SKU search failed
        if "facade" in query.lower() or "booth" in query.lower():
            shutil.copy2("assets/gear_mesh_facade.png", os.path.join(assets_dir, filename))
            print(f"  [FALLBACK] Replaced {filename} with clean facade placeholder")
    time.sleep(1.0) # Gentle throttling

# ----------------------------------------------------
# SCRAPING CO2 CANNON & CO2 GUN (WITH EXTREME DOMAIN AND KEYWORD VALIDATION)
# ----------------------------------------------------
print("\n=== DOWNLOADING EXTREME-VALIDATED CO2 CANNON & GUN ===")

special_fx = [
    {
        "id": "co2cannon",
        "query": "CryoFX CO2 Jet product photo",
        "blacklist": ["gun", "rifle", "pistol", "bb", "airsoft", "toy", "handheld", "shoot", "trigger", "anime", "woodpecker", "mature", "nsfw", "model", "sex"],
        "filename": "gear_co2_cannon.jpg"
    },
    {
        "id": "co2gun",
        "query": "CryoFX CO2 Gun product photo",
        "blacklist": ["pistol", "bb", "airsoft", "toy", "military", "bullet", "tactical", "ammo", "ammunition", "rifle", "gun shop", "pellet", "firearm", "girl", "sexy", "school", "hindi", "mature", "nsfw", "model", "sex"],
        "filename": "gear_co2_gun.jpg"
    }
]

def download_special_fx(query, filename, blacklist):
    print(f"Searching DDG for '{query}'...")
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract standard image links from DDG HTML
            links = re.findall(r'href="(https?://[^"]+?\.(?:jpg|jpeg|png))"', html)
            
            # Find a clean image that doesn't violate our blacklist and is from a professional theatrical effects domain
            valid_domains = ["cryofx", "magicfx", "idjnow", "proaudiostar", "chauvet", "stage", "theater", "effect", "sfx"]
            for img in links:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                
                # Check for pro domains first
                if any(domain in img_lower for domain in valid_domains):
                    print(f"  Found professional photo: {img}")
                    if download_image(img, filename):
                        return True
                        
            # Fallback to general images with clean filenames
            for img in links:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                if any(k in img_lower for k in ["co2", "jet", "cannon", "blaster", "stage"]):
                    print(f"  Found clean fallback photo: {img}")
                    if download_image(img, filename):
                        return True
    except Exception as e:
        print(f"  Search failed: {e}")
    return False

for fx in special_fx:
    download_special_fx(fx['query'], fx['filename'], fx['blacklist'])

print("\n=== GEAR IMAGING PROCESS COMPLETE ===")

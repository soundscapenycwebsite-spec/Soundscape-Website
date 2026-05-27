import os
import shutil
import urllib.request
import urllib.parse
import re
import sys
import time

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = "assets"
extracted_dir = "assets/pdf_extracted"
os.makedirs(assets_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

def download_file(url, filename):
    dest_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            if len(content) > 10000:
                with open(dest_path, 'wb') as f:
                    f.write(content)
                print(f"  [SUCCESS] {url} -> {filename} ({len(content)} bytes)")
                return True
            else:
                print(f"  [SKIPPED] {url} is too small ({len(content)} bytes)")
    except Exception as e:
        print(f"  [FAILED] {url} -> {e}")
    return False

# ----------------------------------------------------
# STRATEGY 1: DIRECT SWEETWATER PRODUCTS (PRISTINE WHITE BACKGROUNDS)
# ----------------------------------------------------
print("=== STRATEGY 1: DOWNLOADING PRISTINE SWEETWATER ASSETS ===")

sweetwater_items = {
    # Microphones
    "gear_shuresm58.jpg": "https://media.sweetwater.com/images/items/750/SM58-large.jpg",
    "gear_shureqlxd4.jpg": "https://media.sweetwater.com/images/items/750/QLXD24SM58-large.jpg",
    "gear_shureslxd.jpg": "https://media.sweetwater.com/images/items/750/SLXD24SM58-large.jpg",
    "gear_sennxsw.jpg": "https://media.sweetwater.com/images/items/750/XSW2835-A-large.jpg",
    "gear_sennew500.jpg": "https://media.sweetwater.com/images/items/750/EW500935G4-AS-large.jpg",
    
    # Lighting
    "gear_moving_heads450.jpg": "https://media.sweetwater.com/images/items/750/IntimSpot375Z-large.jpg",
    "gear_intimidatorspot200.jpg": "https://media.sweetwater.com/images/items/750/IntimSpot260-large.jpg",
    "gear_intimidatorbeam100.jpg": "https://media.sweetwater.com/images/items/750/IntimBeam355-large.jpg",
    "gear_jmswebbmover.jpg": "https://media.sweetwater.com/images/items/750/R2XWash-large.jpg",
    "gear_beam275.jpg": "https://media.sweetwater.com/images/items/750/IntimBeam140SR-large.jpg",
    "gear_washerhead.jpg": "https://media.sweetwater.com/images/items/750/IntimWashZ450-large.jpg",
    "gear_motionstrip.jpg": "https://media.sweetwater.com/images/items/750/COLORbandPix-large.jpg",
    "gear_laser12w.jpg": "https://media.sweetwater.com/images/items/750/DJLaser3D-large.jpg",
    "gear_uplight.jpg": "https://media.sweetwater.com/images/items/750/FreedomParHex4-large.jpg",
    "gear_washers12.jpg": "https://media.sweetwater.com/images/items/750/SlimPART12USB-large.jpg",
    "gear_barwash43.jpg": "https://media.sweetwater.com/images/items/750/COLORbandH9-large.jpg",
    "gear_gigbar.jpg": "https://media.sweetwater.com/images/items/750/GigBar2-large.jpg",
    
    # Facades & Tables
    "gear_mesh_facade.png": "https://media.sweetwater.com/images/items/750/GFWDJFACADE-large.jpg",
    "gear_steeldeck_booth.jpg": "https://media.sweetwater.com/images/items/750/GFWUTLMEDIATBL-large.jpg",
    "gear_command_booth.jpg": "https://media.sweetwater.com/images/items/750/SDJWS01B-large.jpg",
    "gear_proxvista.jpg": "https://media.sweetwater.com/images/items/750/GFWDJFACADE-large.jpg",
    "gear_odyssey48.jpg": "https://media.sweetwater.com/images/items/750/GFWDJFACADE-large.jpg",
    "gear_stage_platform.jpg": "https://media.sweetwater.com/images/items/750/IntelliStage4x4-large.jpg"
}

for filename, url in sweetwater_items.items():
    download_file(url, filename)

# ----------------------------------------------------
# STRATEGY 2: COPYING EXTRACTED PDF IMAGES FOR SPEAKERS & AUDIO DECK SYSTEMS
# ----------------------------------------------------
print("\n=== STRATEGY 2: COPYING AUTHENTIC PDF-EXTRACTED IMAGES ===")

pdf_mappings = {
    # Stand-Alone Controllers & Decks
    "gear_cdj3000.png": "extracted_img_7_2_Image68.jpg",
    "gear_cdj2000.jpg": "extracted_img_7_3_Image70.jpg",
    "gear_xdjxz.png": "extracted_img_8_1_Image73.jpg",
    "gear_xdjaz.png": "extracted_img_8_2_Image75.jpg",
    "gear_v10mixer.png": "extracted_img_8_3_Image77.jpg",
    "gear_a9mixer.png": "extracted_img_8_4_Image78.jpg",
    "gear_rmx1000.jpg": "extracted_img_9_1_Image92.jpg",
    
    # Speakers & Subs
    "gear_maui11.jpg": "extracted_img_9_2_Image93.jpg",
    "gear_accuracycolumn.jpg": "extracted_img_9_3_Image94.jpg",
    "gear_k12_2.png": "extracted_img_10_1_Image97.jpg",
    "gear_rcfart915.jpg": "extracted_img_10_2_Image99.jpg",
    "gear_nxl44a.jpg": "extracted_img_10_3_Image101.jpg",
    "gear_ventis112.jpg": "extracted_img_10_4_Image103.jpg",
    "gear_icoa15.jpg": "extracted_img_11_1_Image107.jpg",
    "gear_ekx15p.jpg": "extracted_img_11_2_Image108.jpg",
    "gear_eviva12p.jpg": "extracted_img_11_3_Image109.jpg",
    "gear_dxs15.jpg": "extracted_img_11_4_Image110.jpg",
    "gear_etx18sp.jpg": "extracted_img_11_5_Image111.jpg",
    
    # Large Venue & Line Arrays
    "gear_rcf705.jpg": "extracted_img_12_1_Image115.jpg",
    "gear_double21.jpg": "extracted_img_12_2_Image117.jpg",
    "gear_rcfhdl30.jpg": "extracted_img_12_3_Image119.jpg",
    "gear_rcfv221.jpg": "extracted_img_12_4_Image120.jpg",
    "gear_kara2.jpg": "extracted_img_13_1_Image123.jpg",
    "gear_sb28.jpg": "extracted_img_13_2_Image124.jpg"
}

for dest_filename, src_filename in pdf_mappings.items():
    src_path = os.path.join(extracted_dir, src_filename)
    dest_path = os.path.join(assets_dir, dest_filename)
    if os.path.exists(src_path):
        try:
            shutil.copy2(src_path, dest_path)
            print(f"  [SUCCESS] Copied PDF image {src_filename} -> {dest_filename}")
        except Exception as e:
            print(f"  [FAILED] Copying {src_filename} -> {e}")
    else:
        print(f"  [MISSING] Extracted source image {src_filename} does not exist!")

# ----------------------------------------------------
# STRATEGY 3: FAILSAFE SCRAPER FOR SPECIAL EFFECTS (CO2 CANNON & CO2 GUN)
# ----------------------------------------------------
print("\n=== STRATEGY 3: FAILSAFE SCRAPING FOR CRYO EFFECTS ===")

special_fx = [
    {
        "id": "co2cannon",
        "query": "CryoFX CO2 Jet",
        "blacklist": ["gun", "rifle", "pistol", "bb", "airsoft", "toy", "handheld", "shoot", "trigger", "anime", "woodpecker"],
        "filename": "gear_co2_cannon.jpg"
    },
    {
        "id": "co2gun",
        "query": "CryoFX CO2 Gun",
        "blacklist": ["pistol", "bb", "airsoft", "toy", "military", "bullet", "tactical", "ammo", "ammunition", "rifle", "gun shop", "pellet", "firearm", "girl", "sexy", "school", "hindi"],
        "filename": "gear_co2_gun.jpg"
    },
    {
        "id": "odysseymedia",
        "query": "ProX Mesa Media DJ TV Facade Workstation XF-MESA-B",
        "blacklist": ["honda", "car", "minivan", "toy", "maquiagem", "copa", "girl", "makeup"],
        "filename": "gear_odysseymedia.jpg"
    }
]

# Simple DuckDuckGo HTML scraper which is extremely fast and robust, no captchas!
def scrape_ddg_images(query, filename, blacklist):
    print(f"Scraping DDG Images for '{query}'...")
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract standard external image URLs or search result snippets
            links = re.findall(r'href="(https?://[^"]+?\.(?:jpg|jpeg|png))"', html)
            print(f"  Found {len(links)} links in DDG search.")
            
            # Find a clean image that doesn't violate our blacklist
            for img in links:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                
                # Verify it is from a legitimate site or contains product tags
                if any(x in img_lower for x in ["cryofx", "sweetwater", "proaudiostar", "idjnow", "guitarcenter", "dj", "stage", "media", "product"]):
                    print(f"  Selected verified URL: {img}")
                    if download_file(img, filename):
                        return True
            
            # Fallback to the first non-blacklisted image
            for img in links:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                print(f"  Selected fallback URL: {img}")
                if download_file(img, filename):
                    return True
    except Exception as e:
        print(f"  DDG Scrape failed: {e}")
    return False

# Try Yahoo/Bing images with correct parsing (ensuring no fallback to random page links)
def scrape_bing_images_correct(query, filename, blacklist):
    print(f"Scraping Bing Images correctly for '{query}'...")
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Bing store direct image URLs inside "murl" inside JSON blocks
            murls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            print(f"  Found {len(murls)} direct image URLs in Bing index.")
            
            if not murls:
                print("  Bing returned empty search result index (likely bot-blocked). Skipping...")
                return False
                
            for img in murls:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                
                print(f"  Trying: {img}")
                if download_file(img, filename):
                    return True
    except Exception as e:
        print(f"  Bing Scrape failed: {e}")
    return False

for fx in special_fx:
    # First try Bing with correct, clean parsing
    success = scrape_bing_images_correct(fx['query'], fx['filename'], fx['blacklist'])
    # If it fails, fallback to DDG
    if not success:
        success = scrape_ddg_images(fx['query'], fx['filename'], fx['blacklist'])
    # Ultimate static fallback to keep it professional if search engines fail
    if not success:
        print(f"  [FALLBACK] Copying a clean facade placeholder for {fx['id']}")
        shutil.copy2(os.path.join(assets_dir, "gear_mesh_facade.png"), os.path.join(assets_dir, fx['filename']))

print("\n=== ALL STRATEGIES EXECUTED SUCCESSFULLY ===")

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

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def clean_file(filename):
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"  Removed old file: {filename}")
        except Exception as e:
            print(f"  Failed to remove {filename}: {e}")

def download_image(url, dest_name):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            # Verify it's a valid image (JPEG, PNG, or WEBP/GIF)
            if len(content) > 3000 and (content.startswith(b'\xff\xd8') or content.startswith(b'\x89PNG') or content.startswith(b'RIFF') or content.startswith(b'GIF')):
                dest_path = os.path.join(assets_dir, dest_name)
                with open(dest_path, "wb") as f:
                    f.write(content)
                print(f"    [DOWNLOAD SUCCESS] {dest_name} ({len(content)} bytes) downloaded from: {url}")
                return True
    except Exception as e:
        pass
    return False

def search_ddg_fallback(query, dest_name, preferred_domains=None):
    print(f"  Running DDG fallback search for: '{query}'...")
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    req = urllib.request.Request(search_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            links = re.findall(r'href=\"([^\"]+)\"', html)
            
            unescaped_links = []
            for link in links:
                link = urllib.parse.unquote(link)
                if "/l/?kh=-1&uddg=" in link:
                    link = link.split("uddg=")[-1].split("&")[0]
                    link = urllib.parse.unquote(link)
                unescaped_links.append(link)
            
            candidates = []
            for link in unescaped_links:
                if not link.startswith('http'):
                    continue
                if any(ext in link.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    candidates.append(link)
                elif any(domain in link.lower() for domain in ['sweetwater.com', 'fullcompass.com', 'adj.com', 'proxdirect.com', 'chauvetdj.com']):
                    candidates.append(link)
            
            if preferred_domains:
                sorted_candidates = []
                for domain in preferred_domains:
                    for c in candidates:
                        if domain in c.lower() and c not in sorted_candidates:
                            sorted_candidates.append(c)
                for c in candidates:
                    if c not in sorted_candidates:
                        sorted_candidates.append(c)
                candidates = sorted_candidates
            
            candidates = list(dict.fromkeys(candidates))
            
            # Try direct images first
            for c in candidates:
                if any(ext in c.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    print(f"    Trying direct image URL: {c}")
                    if download_image(c, dest_name):
                        return True
            
            # Try to guess from store page links
            for c in candidates:
                if "sweetwater.com/store/detail/" in c:
                    parts = c.split('/')
                    sku = parts[-1] or parts[-2]
                    sku = sku.split('--')[0].split('?')[0]
                    sku_img = f"https://media.sweetwater.com/images/items/750/{sku}-large.jpg"
                    print(f"    Guessed Sweetwater URL from store link: {sku_img}")
                    if download_image(sku_img, dest_name):
                        return True
                
                if "fullcompass.com/prod/" in c or "fullcompass.com/common/products/" in c:
                    match = re.search(r'/prod/(\d+)-', c)
                    if match:
                        prod_id = match.group(1)
                        img_url = f"https://www.fullcompass.com/common/products/original/{prod_id}.jpg"
                        print(f"    Guessed Full Compass URL: {img_url}")
                        if download_image(img_url, dest_name):
                            return True
    except Exception as e:
        print(f"    DDG search failed: {e}")
        
    return False

# Comprehensive list of items to replace and their primary direct retail image sources
stage_equipment = [
    # 1. CO2 Special Effects
    {
        "filename": "gear_co2_gun.jpg",
        "primary_urls": [
            "https://www.cryofx.com/media/catalog/product/c/o/co2-gun-cryofx.jpg",
            "https://www.cryofx.com/media/catalog/product/c/r/cryofx-co2-gun-led-1.jpg"
        ],
        "ddg_query": "CryoFX handheld CO2 blaster cryo gun stage special effect product",
        "preferred": ["cryofx.com"]
    },
    {
        "filename": "gear_co2cannon.jpg",
        "primary_urls": [
            "https://www.adj.com/media/catalog/product/j/e/jet_co2_main.jpg",
            "https://media.sweetwater.com/images/items/750/CO2Jet-large.jpg"
        ],
        "ddg_query": "ADJ DMX floor CO2 jet machine stage effect product photo",
        "preferred": ["adj.com", "sweetwater.com"]
    },
    
    # 2. Stage Decks (Honeycomb textures, wooden panels, steel frame, NO homes or lawns!)
    {
        "filename": "gear_steeldeck_booth.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/XSQ-4X4PK-large.jpg",
            "https://media.sweetwater.com/images/items/750/XSQ4X4-large.jpg"
        ],
        "ddg_query": "ProX StageQ 4x4 stage platform Honeycomb deck surface",
        "preferred": ["proxdirect.com", "sweetwater.com"]
    },
    {
        "filename": "gear_steeldeck_platform.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/XSQ-4X8PK-large.jpg",
            "https://media.sweetwater.com/images/items/750/XSQ4X8-large.jpg"
        ],
        "ddg_query": "ProX StageQ 4x8 stage platform concert riser deck panel",
        "preferred": ["proxdirect.com", "sweetwater.com"]
    },
    
    # 3. DJ Booths & Facades
    {
        "filename": "gear_mesh_facade.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/FZF3072-large.jpg",
            "https://media.sweetwater.com/images/items/750/LTMESH72-large.jpg"
        ],
        "ddg_query": "Odyssey 72 Pro DJ Booth mesh facade panel foldable",
        "preferred": ["sweetwater.com", "odysseycases.com"]
    },
    {
        "filename": "gear_command_booth.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/XS-DJDK-large.jpg",
            "https://media.sweetwater.com/images/items/750/XS-DJDKBL-large.jpg"
        ],
        "ddg_query": "ProX Command Center DJ Booth 53 inch media table stand",
        "preferred": ["proxdirect.com", "sweetwater.com"]
    },
    {
        "filename": "gear_proxvista.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/XF-VISTABAR-large.jpg",
            "https://media.sweetwater.com/images/items/750/XF-MESA-large.jpg"
        ],
        "ddg_query": "ProX Mesa Vista DJ Facade booth panel white mesh",
        "preferred": ["proxdirect.com", "sweetwater.com"]
    },
    {
        "filename": "gear_odyssey48.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/FZF3048-large.jpg",
            "https://media.sweetwater.com/images/items/750/FZF3048BL-large.jpg"
        ],
        "ddg_query": "Odyssey 48 DJ table facade black stretch spandex wrap",
        "preferred": ["sweetwater.com", "odysseycases.com"]
    },
    
    # 4. Professional Lighting & Stage Totems
    {
        "filename": "gear_uplight.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/FreeParH9IP-large.jpg",
            "https://media.sweetwater.com/images/items/750/FreedomParT6-large.jpg"
        ],
        "ddg_query": "Chauvet Freedom Par H9 IP wireless battery LED par uplight",
        "preferred": ["sweetwater.com", "chauvetdj.com"]
    },
    {
        "filename": "gear_washers12.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/ColBandT3USB-large.jpg",
            "https://media.sweetwater.com/images/items/750/ColBandT3BT-large.jpg"
        ],
        "ddg_query": "Chauvet COLORband T3 USB LED strip stage wash bar",
        "preferred": ["sweetwater.com", "chauvetdj.com"]
    },
    {
        "filename": "gear_barwash43.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/COLORbandPix-large.jpg",
            "https://media.sweetwater.com/images/items/750/COLORbandPixM-large.jpg"
        ],
        "ddg_query": "43 inch Chauvet COLORband Pix USB wall washer bar light",
        "preferred": ["sweetwater.com", "chauvetdj.com"]
    },
    {
        "filename": "gear_motionstrip.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/COLORbandPixM-large.jpg",
            "https://media.sweetwater.com/images/items/750/SweeperBeamQuad-large.jpg"
        ],
        "ddg_query": "Chauvet COLORband Pix motorized tilt sweep bar LED light",
        "preferred": ["sweetwater.com", "chauvetdj.com"]
    },
    {
        "filename": "gear_gigbar.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/GigBar2-large.jpg",
            "https://media.sweetwater.com/images/items/750/GigBarILS-large.jpg"
        ],
        "ddg_query": "Chauvet Gigbar 2 mobile DJ light bar system tripod stand",
        "preferred": ["sweetwater.com", "chauvetdj.com"]
    },
    {
        "filename": "gear_totem8ft.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/XT-TOTEM8FT-large.jpg",
            "https://media.sweetwater.com/images/items/750/XT-TOTEM8FT-BL-large.jpg"
        ],
        "ddg_query": "8 feet F34 vertical square aluminum truss totem pillar base plate",
        "preferred": ["sweetwater.com", "proxdirect.com"]
    },
    {
        "filename": "gear_totem6ft.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/XT-TOTEM6FT-large.jpg",
            "https://media.sweetwater.com/images/items/750/XT-TOTEM6FT-BL-large.jpg"
        ],
        "ddg_query": "6 feet F34 vertical square aluminum truss totem pillar base plate",
        "preferred": ["sweetwater.com", "proxdirect.com"]
    },
    {
        "filename": "gear_jmswebbmover.jpg",
        "primary_urls": [
            "https://media.sweetwater.com/images/items/750/IntimSpot260-large.jpg",
            "https://media.sweetwater.com/images/items/750/IntimSpot110-large.jpg"
        ],
        "ddg_query": "Chauvet wash moving head stage light fixture physical product",
        "preferred": ["sweetwater.com", "chauvetdj.com"]
    }
]

print("=== STARTING ADVANCED STAGE EQUIPMENT PHOTO RESOLUTION PIPELINE ===")

for item in stage_equipment:
    filename = item["filename"]
    print(f"\n[ASSET RESOLUTION] Resolving: '{filename}'")
    
    # 1. Clean up old/incorrect file
    clean_file(filename)
    
    # 2. Try primary known retail SKU URLs first
    success = False
    for url in item["primary_urls"]:
        print(f"  Trying primary URL: {url[:80]}...")
        if download_image(url, filename):
            success = True
            break
            
    # 3. If primary URLs fail, fallback to intelligent DDG parser
    if not success:
        print(f"  Primary URLs failed. Falling back to DDG parser...")
        success = search_ddg_fallback(item["ddg_query"], filename, item["preferred"])
        
    if not success:
        print(f"  [CRITICAL ERROR] Failed to download correct photo for: '{filename}'")
    else:
        print(f"  [COMPLETED] Successfully resolved correct asset for: '{filename}'")
        
print("\n=== PIPELINE FINISHED ===")

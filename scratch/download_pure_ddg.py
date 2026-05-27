import urllib.request
import urllib.parse
import re
import os
import shutil
import sys
import time

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = "assets"
os.makedirs(assets_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
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
                print(f"  [SUCCESS] {url} -> {filename} ({len(content)} bytes)")
                return True
            else:
                print(f"  [SKIPPED] Image too small ({len(content)} bytes)")
    except Exception as e:
        print(f"  [FAILED] Downloading {url} -> {e}")
    return False

# DuckDuckGo HTML search images scraper
def search_and_download_gear(query, filename, domain_filters, blacklist):
    print(f"\nSearching DDG for '{query}'...")
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract standard external image URLs or links
            links = re.findall(r'href="(https?://[^"]+?\.(?:jpg|jpeg|png))"', html)
            print(f"  Found {len(links)} links in DDG index.")
            
            # 1st Priority: Match our target domains (e.g. sweetwater, cryofx)
            for img in links:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                
                if any(dom in img_lower for dom in domain_filters):
                    print(f"  Found target-domain match: {img}")
                    if download_image(img, filename):
                        return True
            
            # 2nd Priority: Fallback to any clean image from generic retailers or manufacturers
            for img in links:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                
                # Verify it's a product catalog picture by domain or filename keywords
                if any(x in img_lower for x in ["product", "catalog", "fixture", "guitarcenter", "idjnow", "proaudiostar", "bhphotovideo", "chauvet", "stage", "gear"]):
                    print(f"  Found product catalog match: {img}")
                    if download_image(img, filename):
                        return True
                        
            # Ultimate Fallback: Try the first clean link that isn't blacklisted
            for img in links:
                img_lower = img.lower()
                violates = False
                for black in blacklist:
                    if black in img_lower:
                        violates = True
                        break
                if violates:
                    continue
                print(f"  Using general fallback link: {img}")
                if download_image(img, filename):
                    return True
                    
            print(f"  [FAILED] No suitable image found for query: '{query}'")
            return False
    except Exception as e:
        print(f"  [FAILED] DDG search error: {e}")
        return False

# Master catalog list to retrieve
gear_list = [
    # Special Effects
    {
        "filename": "gear_co2_cannon.jpg",
        "query": "CryoFX CO2 Jet stage special effect",
        "domains": ["cryofx.com", "magicfx.eu", "idjnow.com", "proaudiostar.com"],
        "blacklist": ["gun", "rifle", "pistol", "bb", "airsoft", "toy", "handheld", "shoot", "trigger", "anime", "woodpecker", "mature", "nsfw", "model"]
    },
    {
        "filename": "gear_co2_gun.jpg",
        "query": "CryoFX handheld CO2 blaster gun",
        "domains": ["cryofx.com", "magicfx.eu", "idjnow.com", "proaudiostar.com"],
        "blacklist": ["pistol", "bb", "airsoft", "toy", "military", "bullet", "tactical", "ammo", "ammunition", "rifle", "gun shop", "pellet", "firearm", "girl", "sexy", "school", "hindi", "mature", "nsfw", "model"]
    },
    
    # Lighting
    {
        "filename": "gear_moving_heads450.jpg",
        "query": "Chauvet DJ Intimidator Spot 375Z sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["beam show", "concert light show", "party photos", "kidney", "nephron"]
    },
    {
        "filename": "gear_intimidatorspot200.jpg",
        "query": "Chauvet DJ Intimidator Spot 260 sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["beam show", "concert light show", "party photos", "sailor", "moon"]
    },
    {
        "filename": "gear_intimidatorbeam100.jpg",
        "query": "Chauvet DJ Intimidator Beam 355 sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["beam show", "concert light show", "party photos", "triathlon", "roadcase"]
    },
    {
        "filename": "gear_jmswebbmover.jpg",
        "query": "Chauvet Rogue R2X Wash sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["hay", "foin", "poulailler", "login"]
    },
    {
        "filename": "gear_beam275.jpg",
        "query": "Chauvet DJ Intimidator Beam 140SR sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["beam show", "concert light show", "porn", "xxx"]
    },
    {
        "filename": "gear_washerhead.jpg",
        "query": "Chauvet DJ Intimidator Wash Zoom 450 sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["beam show", "concert light show", "coloring", "sheet", "cup", "ogimg"]
    },
    {
        "filename": "gear_motionstrip.jpg",
        "query": "Chauvet DJ COLORband Pix sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["tumblr"]
    },
    {
        "filename": "gear_laser12w.jpg",
        "query": "professional stage DMX RGB laser light sweetwater",
        "domains": ["sweetwater.com", "guitarcenter.com", "proaudiostar.com"],
        "blacklist": ["beam show", "honda", "civic"]
    },
    {
        "filename": "gear_uplight.jpg",
        "query": "Chauvet DJ Freedom Par Hex 4 sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["oculos", "protecao"]
    },
    {
        "filename": "gear_washers12.jpg",
        "query": "Chauvet DJ SlimPAR T12 USB sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": []
    },
    {
        "filename": "gear_barwash43.jpg",
        "query": "Chauvet DJ COLORband H9 USB sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["fisher", "concert hall"]
    },
    {
        "filename": "gear_gigbar.jpg",
        "query": "Chauvet DJ GigBAR Move sweetwater",
        "domains": ["sweetwater.com", "chauvetdj.com", "guitarcenter.com"],
        "blacklist": ["acidcow", "facts"]
    },
    
    # DJ Booths & Facades
    {
        "filename": "gear_proxvista.jpg",
        "query": "ProX Vista Facade DJ booth sweetwater",
        "domains": ["sweetwater.com", "proaudiostar.com", "idjnow.com"],
        "blacklist": []
    },
    {
        "filename": "gear_odyssey48.jpg",
        "query": "Odyssey 48 DJ table facade sweetwater",
        "domains": ["sweetwater.com", "proaudiostar.com", "idjnow.com"],
        "blacklist": []
    },
    {
        "filename": "gear_steeldeck_booth.jpg",
        "query": "Gator Frameworks Utility DJ table sweetwater",
        "domains": ["sweetwater.com", "proaudiostar.com", "idjnow.com"],
        "blacklist": ["nike", "brasil"]
    },
    {
        "filename": "gear_command_booth.jpg",
        "query": "ProX Command Center DJ booth sweetwater",
        "domains": ["sweetwater.com", "proaudiostar.com", "idjnow.com"],
        "blacklist": ["subligar", "luna"]
    },
    {
        "filename": "gear_odysseymedia.jpg",
        "query": "ProX Mesa Media DJ Facade XF-MESA-B sweetwater",
        "domains": ["sweetwater.com", "proaudiostar.com", "idjnow.com"],
        "blacklist": ["pictoa", "porn", "mature", "nsfw", "model", "gallery"]
    },
    
    # Staging
    {
        "filename": "gear_stage_platform.jpg",
        "query": "IntelliStage 4x4 stage platform panel sweetwater",
        "domains": ["sweetwater.com", "proaudiostar.com", "idjnow.com"],
        "blacklist": []
    }
]

print("=== STARTING BOMBPROOF REDIRECTED DDG DOWNLOADS ===")
for gear in gear_list:
    search_and_download_gear(gear['query'], gear['filename'], gear['domains'], gear['blacklist'])
    time.sleep(1.5) # Throttling

# Copy a premium fallback if any file is missing or still invalid
for gear in gear_list:
    dest_path = os.path.join(assets_dir, gear['filename'])
    if not os.path.exists(dest_path) or os.path.getsize(dest_path) < 5000:
        # Copy a clean facade placeholder to prevent broken image icons on the UI
        shutil.copy2("assets/gear_mesh_facade.png", dest_path)
        print(f"[RECOVERED] Replaced missing or small {gear['filename']} with clean facade placeholder")

print("\n=== GEAR IMAGING PROCESS COMPLETE ===")

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

targets = [
    {
        "id": "co2cannon",
        "query": "CryoFX CO2 Jet",
        "blacklist": ["gun", "rifle", "pistol", "bb", "airsoft", "toy", "handheld", "shoot", "trigger", "amine"],
        "filename": "gear_co2_cannon.jpg"
    },
    {
        "id": "co2gun",
        "query": "CryoFX CO2 Gun blaster",
        "blacklist": ["pistol", "bb", "airsoft", "toy", "military", "bullet", "tactical", "ammo", "ammunition", "rifle", "gun shop", "pellet", "firearm", "girl", "sexy"],
        "filename": "gear_co2_gun.jpg"
    },
    {
        "id": "stageplatforms",
        "query": "stage platform 4x4 panel",
        "blacklist": ["booth", "facade", "honda", "car", "minivan", "toy", "speaker", "corte", "hilo", "ventajas"],
        "filename": "gear_stage_platform.jpg"
    },
    {
        "id": "steeldeckbooth",
        "query": "Steeldeck DJ booth",
        "blacklist": ["honda", "car", "minivan", "toy", "speaker", "mirage", "dassault", "flares", "pakistan"],
        "filename": "gear_steeldeck_booth.jpg"
    },
    {
        "id": "command53",
        "query": "ProX Command Center DJ booth XS-DJDKBL",
        "blacklist": ["honda", "car", "minivan", "toy", "scrim", "martin", "margo"],
        "filename": "gear_command_booth.jpg"
    },
    {
        "id": "odysseymedia",
        "query": "ProX Mesa Media DJ TV Facade Workstation",
        "blacklist": ["honda", "car", "minivan", "toy", "maquiagem", "copa"],
        "filename": "gear_odysseymedia.jpg"
    },
    {
        "id": "movingheads450",
        "query": "Chauvet DJ Intimidator Spot 375Z",
        "blacklist": ["beam show", "club light show", "laser show", "stage design", "kidney", "nephron", "anatomy"],
        "filename": "gear_moving_heads450.jpg"
    },
    {
        "id": "intimidatorspot200",
        "query": "Chauvet DJ Intimidator Spot 260",
        "blacklist": ["beam show", "club light show", "party lights", "stage design"],
        "filename": "gear_intimidatorspot200.jpg"
    },
    {
        "id": "intimidatorbeam100",
        "query": "Chauvet DJ Intimidator Beam 355",
        "blacklist": ["beam show", "club light show", "party lights", "stage design", "triathlon"],
        "filename": "gear_intimidatorbeam100.jpg"
    },
    {
        "id": "jmswebbmover",
        "query": "Chauvet Rogue R2X Wash moving head",
        "blacklist": ["beam show", "club light show", "party lights", "stage design", "hay", "foin", "poulailler"],
        "filename": "gear_jmswebbmover.jpg"
    },
    {
        "id": "beam275",
        "query": "275W beam moving head",
        "blacklist": ["beam show", "club light show", "laser show", "stage design", "ypncdn", "porn", "xxx"],
        "filename": "gear_beam275.jpg"
    },
    {
        "id": "washerhead",
        "query": "LED wash moving head DMX light",
        "blacklist": ["beam show", "club light show", "stage design", "coloring", "sheet", "cup"],
        "filename": "gear_washerhead.jpg"
    },
    {
        "id": "motionstrip",
        "query": "motorized LED strip light bar",
        "blacklist": ["beam show", "club light show", "stage design", "tumblr"],
        "filename": "gear_motionstrip.jpg"
    },
    {
        "id": "laser12w",
        "query": "12W professional RGB DMX laser",
        "blacklist": ["beam show", "club laser show", "stage design"],
        "filename": "gear_laser12w.jpg"
    },
    {
        "id": "uplights",
        "query": "Chauvet DJ Freedom Par hex",
        "blacklist": ["beam show", "stage design"],
        "filename": "gear_uplight.jpg"
    },
    {
        "id": "washers12",
        "query": "Chauvet DJ SlimPAR DMX",
        "blacklist": ["beam show", "stage design"],
        "filename": "gear_washers12.jpg"
    },
    {
        "id": "barwash43",
        "query": "Chauvet DJ COLORband DMX wash bar",
        "blacklist": ["beam show", "stage design", "fisher", "college", "concert hall"],
        "filename": "gear_barwash43.jpg"
    },
    {
        "id": "gigbar2",
        "query": "Chauvet DJ GigBAR 2 System",
        "blacklist": ["beam show", "party photos", "stage design", "acidcow", "facts"],
        "filename": "gear_gigbar.jpg"
    }
]

os.makedirs("assets", exist_ok=True)

# List of trusted domains to prioritize
trusted_domains = ["sweetwater.com", "guitarcenter.com", "idjnow.com", "bhphotovideo.com", "proaudiostar.com", "chauvetdj.com", "cryofx.com", "magicfx.eu", "gear4music", "soundpro.com"]

for target in targets:
    print(f"\n========================================")
    print(f"Processing: {target['id']}")
    print(f"Query: '{target['query']}'")
    
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(target['query'])}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if not img_urls:
                img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            
            print(f"Found {len(img_urls)} raw image URLs in index.")
            
            # Sort URLs to prioritize trusted pro-audio retail sites
            sorted_urls = []
            for img in img_urls:
                img_lower = img.lower()
                is_trusted = any(domain in img_lower for domain in trusted_domains)
                if is_trusted:
                    sorted_urls.insert(0, img) # Put trusted domains at the top!
                else:
                    sorted_urls.append(img)
            
            downloaded = False
            for img in sorted_urls:
                img_lower = img.lower()
                
                # Check blacklist
                violates = False
                for blacklisted in target['blacklist']:
                    if blacklisted in img_lower:
                        violates = True
                        break
                
                if violates:
                    continue
                
                print(f"Trying: {img}")
                try:
                    img_req = urllib.request.Request(img, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                        img_data = img_resp.read()
                        if len(img_data) > 10000:  # Must be a reasonable size
                            dest_path = os.path.join("assets", target['filename'])
                            with open(dest_path, "wb") as f:
                                f.write(img_data)
                            print(f"[SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
                            downloaded = True
                            break
                        else:
                            print("  Too small, skipping...")
                except Exception as e:
                    print(f"  Failed download: {e}")
                    continue
            
            if not downloaded:
                print(f"[FAILED] No clean images found for query.")
    except Exception as e:
        print(f"Search failed: {e}")
    
    time.sleep(1) # Gentle throttling

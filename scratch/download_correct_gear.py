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

# Strict target gear list
target_gear = [
    {
        "id": "co2cannon",
        "query": "CryoFX CO2 Jet stage special effect fixture",
        "blacklist": ["gun", "rifle", "pistol", "bb", "airsoft", "toy", "handheld", "shoot", "trigger"],
        "filename": "gear_co2_cannon.jpg"
    },
    {
        "id": "co2gun",
        "query": "CryoFX handheld CO2 blaster gun special effect",
        "blacklist": ["pistol", "bb", "airsoft", "toy", "military", "bullet", "tactical", "ammo", "ammunition", "rifle", "gun shop", "pellet", "firearm"],
        "filename": "gear_co2_gun.jpg"
    },
    {
        "id": "stageplatforms",
        "query": "Steel Deck stage platform panel 4x4",
        "blacklist": ["booth", "facade", "honda", "car", "minivan", "toy", "speaker"],
        "filename": "gear_stage_platform.jpg"
    },
    {
        "id": "steeldeckbooth",
        "query": "heavy duty steel deck DJ booth performance table",
        "blacklist": ["honda", "car", "minivan", "toy", "speaker"],
        "filename": "gear_steeldeck_booth.jpg"
    },
    {
        "id": "command53",
        "query": "ProX Command Center DJ booth table console XS-DJDKBL",
        "blacklist": ["honda", "car", "minivan", "toy", "scrim"],
        "filename": "gear_command_booth.jpg"
    },
    {
        "id": "odysseymedia",
        "query": "ProX Mesa Media DJ TV Facade Workstation XF-MESA-B",
        "blacklist": ["honda", "car", "minivan", "toy"],
        "filename": "gear_odysseymedia.jpg"
    },
    {
        "id": "movingheads450",
        "query": "450W hybrid moving head beam spot wash DMX light fixture",
        "blacklist": ["beam show", "club light show", "laser show", "stage design"],
        "filename": "gear_moving_heads450.jpg"
    },
    {
        "id": "intimidatorspot200",
        "query": "Chauvet Intimidator Spot 200W LED DMX moving head fixture",
        "blacklist": ["beam show", "club light show", "party lights", "stage design"],
        "filename": "gear_intimidatorspot200.jpg"
    },
    {
        "id": "intimidatorbeam100",
        "query": "Chauvet Intimidator Beam 100W LED DMX moving head fixture",
        "blacklist": ["beam show", "club light show", "party lights", "stage design"],
        "filename": "gear_intimidatorbeam100.jpg"
    },
    {
        "id": "jmswebbmover",
        "query": "LED pixel wash moving head DMX light fixture",
        "blacklist": ["beam show", "club light show", "party lights", "stage design"],
        "filename": "gear_jmswebbmover.jpg"
    },
    {
        "id": "beam275",
        "query": "275W beam moving head light DMX concert fixture",
        "blacklist": ["beam show", "club light show", "laser show", "stage design"],
        "filename": "gear_beam275.jpg"
    },
    {
        "id": "washerhead",
        "query": "LED wash moving head DMX stage light fixture",
        "blacklist": ["beam show", "club light show", "stage design"],
        "filename": "gear_washerhead.jpg"
    },
    {
        "id": "motionstrip",
        "query": "motorized LED strip light bar DMX stage fixture",
        "blacklist": ["beam show", "club light show", "stage design"],
        "filename": "gear_motionstrip.jpg"
    },
    {
        "id": "laser12w",
        "query": "12W RGB DMX professional laser projector light fixture",
        "blacklist": ["beam show", "club laser show", "stage design"],
        "filename": "gear_laser12w.jpg"
    },
    {
        "id": "uplights",
        "query": "battery powered wireless DMX LED uplight hex par fixture",
        "blacklist": ["beam show", "stage design"],
        "filename": "gear_uplight.jpg"
    },
    {
        "id": "washers12",
        "query": "LED DMX wash stage light bar fixture",
        "blacklist": ["beam show", "stage design"],
        "filename": "gear_washers12.jpg"
    },
    {
        "id": "barwash43",
        "query": "43 inch DMX LED wash light bar fixture",
        "blacklist": ["beam show", "stage design"],
        "filename": "gear_barwash43.jpg"
    },
    {
        "id": "gigbar2",
        "query": "Chauvet GIG Bar 2 lighting system stand fixture",
        "blacklist": ["beam show", "party photos", "stage design"],
        "filename": "gear_gigbar.jpg"
    }
]

os.makedirs("assets", exist_ok=True)

for gear in target_gear:
    print(f"\n========================================")
    print(f"Downloading correct photo for {gear['id']}...")
    print(f"Query: {gear['query']}")
    
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(gear['query'])}"
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if not img_urls:
                img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            
            print(f"Found {len(img_urls)} raw image URLs in index.")
            
            # Find a clean image that doesn't violate our blacklist
            downloaded = False
            for img in img_urls:
                img_lower = img.lower()
                # Check blacklist
                violates = False
                for blacklisted in gear['blacklist']:
                    if blacklisted in img_lower:
                        violates = True
                        break
                
                if violates:
                    continue
                
                # Try downloading it!
                print(f"Trying: {img}")
                try:
                    img_req = urllib.request.Request(img, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                        img_data = img_resp.read()
                        if len(img_data) > 10000:  # Must be a reasonable size
                            dest_path = os.path.join("assets", gear['filename'])
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

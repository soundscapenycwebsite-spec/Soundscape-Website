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
        "query": "Chauvet DJ CO2 Jet stage special effect white background",
        "filename": "gear_co2_cannon.jpg"
    },
    {
        "id": "co2gun",
        "query": "MagicFX CO2 Gun stage blaster white background",
        "filename": "gear_co2_gun.jpg"
    },
    {
        "id": "stageplatforms",
        "query": "Steeldeck stage platform 4x4 panel white background",
        "filename": "gear_stage_platform.jpg"
    },
    {
        "id": "steeldeckbooth",
        "query": "Steeldeck DJ booth performance stage table white background",
        "filename": "gear_steeldeck_booth.jpg"
    },
    {
        "id": "command53",
        "query": "ProX Command Center DJ booth XS-DJDKBL white background",
        "filename": "gear_command_booth.jpg"
    },
    {
        "id": "odysseymedia",
        "query": "ProX Mesa Media DJ TV Facade Workstation white background",
        "filename": "gear_odysseymedia.jpg"
    },
    {
        "id": "movingheads450",
        "query": "Chauvet DJ Intimidator Spot 375Z moving head white background",
        "filename": "gear_moving_heads450.jpg"
    },
    {
        "id": "intimidatorspot200",
        "query": "Chauvet DJ Intimidator Spot 260 DMX moving head white background",
        "filename": "gear_intimidatorspot200.jpg"
    },
    {
        "id": "intimidatorbeam100",
        "query": "Chauvet DJ Intimidator Beam 355 DMX moving head white background",
        "filename": "gear_intimidatorbeam100.jpg"
    },
    {
        "id": "jmswebbmover",
        "query": "Chauvet Rogue R2X Wash moving head DMX white background",
        "filename": "gear_jmswebbmover.jpg"
    },
    {
        "id": "beam275",
        "query": "Chauvet DJ Intimidator Beam DMX moving head white background",
        "filename": "gear_beam275.jpg"
    },
    {
        "id": "washerhead",
        "query": "Chauvet DJ wash moving head DMX light white background",
        "filename": "gear_washerhead.jpg"
    },
    {
        "id": "motionstrip",
        "query": "Chauvet DJ COLORband Pix DMX strip bar light white background",
        "filename": "gear_motionstrip.jpg"
    },
    {
        "id": "laser12w",
        "query": "12W professional RGB DMX laser light fixture white background",
        "filename": "gear_laser12w.jpg"
    },
    {
        "id": "uplights",
        "query": "Chauvet DJ Freedom Par hex wireless DMX uplight white background",
        "filename": "gear_uplight.jpg"
    },
    {
        "id": "washers12",
        "query": "Chauvet DJ SlimPAR DMX wash light par white background",
        "filename": "gear_washers12.jpg"
    },
    {
        "id": "barwash43",
        "query": "Chauvet DJ COLORband DMX wash bar light white background",
        "filename": "gear_barwash43.jpg"
    },
    {
        "id": "gigbar2",
        "query": "Chauvet DJ GigBAR Move lighting system stand white background",
        "filename": "gear_gigbar.jpg"
    }
]

os.makedirs("assets", exist_ok=True)

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
            
            # Find a clean retail photo
            downloaded = False
            for img in img_urls:
                img_lower = img.lower()
                
                # Check for trusted retail domains first
                trusted = ["sweetwater", "guitarcenter", "musiciansfriend", "idjnow", "proaudiostar", "bhphotovideo", "chauvet", "cryofx", "magicfx", "static", "media"]
                is_trusted = any(t in img_lower for t in trusted)
                
                # Filter out standard non-product terms
                if "honda" in img_lower or "minivan" in img_lower or "bible" in img_lower or "isaiah" in img_lower or "calendar" in img_lower or "timeline" in img_lower:
                    continue
                
                print(f"Trying: {img} (Trusted: {is_trusted})")
                try:
                    img_req = urllib.request.Request(img, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=8) as img_resp:
                        img_data = img_resp.read()
                        if len(img_data) > 15000:  # Must be a reasonable size
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

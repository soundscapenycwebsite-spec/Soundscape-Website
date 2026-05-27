import urllib.request
import urllib.parse
import json
import os
import time
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Origin': 'https://www.qwant.com',
    'Referer': 'https://www.qwant.com/'
}

def get_qwant_images(query):
    print(f"Searching Qwant for: '{query}'...")
    url = f"https://api.qwant.com/v3/search/images?q={urllib.parse.quote(query)}&count=10&locale=en_US&uiv=4"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('data', {}).get('result', {}).get('items', [])
            return [item.get('media') for item in items if item.get('media')]
    except Exception as e:
        print(f"    [QWANT ERROR]: {e}")
        return []

def download_image(url, output_filename):
    output_path = os.path.join(assets_dir, output_filename)
    img_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=img_headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read()
            with open(output_path, 'wb') as f:
                f.write(content)
        size = os.path.getsize(output_path)
        if size > 5000:  # Must be a decent size
            print(f"    [DOWNLOAD SUCCESS] {url} -> {output_filename} ({size} bytes)")
            return True
        else:
            print(f"    [DOWNLOAD WARNING] Image too small ({size} bytes), ignoring.")
            if os.path.exists(output_path):
                os.remove(output_path)
            return False
    except Exception as e:
        print(f"    [DOWNLOAD FAILED] {url} -> {e}")
        return False

# Specifically target the incorrect images and force override them!
items_to_replace = {
    # 1. CO2 cryo jets (NO weapons, NO BB guns!)
    "gear_co2_gun.jpg": "CryoFX handheld CO2 gun blaster stage special effect product",
    "gear_co2cannon.jpg": "DMX stage floor CO2 jet machine effect nozzle D-Fi",
    
    # 2. Stage Decks (NO houses, NO lawns!)
    "gear_steeldeck_booth.jpg": "ProX StageQ 4x4 stage platform Honeycomb deck surface",
    "gear_steeldeck_platform.jpg": "Steel Deck 8x4 stage platform modular concert riser",
    
    # 3. DJ Booths (NO houses, NO plastic bottles!)
    "gear_mesh_facade.jpg": "Odyssey 72 Pro DJ Booth facade foldable panel",
    "gear_command_booth.jpg": "Odyssey Command Center DJ Booth 53 inch media table stand",
    "gear_proxvista.jpg": "Pro X Vista Facade DJ Booth black mesh panels scrim",
    "gear_odyssey48.jpg": "Odyssey 48 DJ table facade black stretch spandex wrap",
    
    # 4. Lighting (NO sunsets, NO arena warehouse trusses, NO laser light shows!)
    "gear_uplight.jpg": "Chauvet Freedom Par H9 IP wireless battery LED par uplight",
    "gear_washers12.jpg": "Chauvet COLORband T3 USB LED strip stage wash bar",
    "gear_barwash43.jpg": "43 inch linear LED wall washer stage wash bar light",
    "gear_motionstrip.jpg": "Chauvet COLORband Pix motorized tilt sweep bar LED light",
    "gear_gigbar.jpg": "Chauvet Gigbar 2 mobile DJ light bar system tripod stand",
    "gear_totem8ft.jpg": "8 feet F34 vertical square aluminum truss totem pillar base plate",
    "gear_totem6ft.jpg": "6 feet F34 vertical square aluminum truss totem pillar base plate",
    "gear_jmswebbmover.jpg": "LED wash moving head stage light fixture physical product"
}

print("=== STARTING DYNAMIC BINDING AND FORCE OVERWRITING OF STAGE EQUIPMENT ASSETS ===")
for filename, query in items_to_replace.items():
    print(f"\n[PROCESSING] Forcing replacement for '{filename}' with query: '{query}'")
    urls = get_qwant_images(query)
    
    if not urls:
        print(f"  No URLs returned from Qwant search.")
        continue
        
    success = False
    # Try downloading top 5 results
    for url in urls[:5]:
        if url.startswith('http'):
            print(f"  Attempting download: {url[:100]}...")
            if download_image(url, filename):
                success = True
                break
            time.sleep(1)
            
    if not success:
        print(f"  [CRITICAL ERROR] Failed to fetch image for '{filename}'")
    
    time.sleep(2)  # short pause to respect rate limits

print("\n=== FORCE ASSET OVERWRITE COMPLETE ===")

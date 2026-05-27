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
    url = f"https://api.qwant.com/v3/search/images?q={urllib.parse.quote(query)}&count=10&locale=en_US&uiv=4"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            items = data.get('data', {}).get('result', {}).get('items', [])
            return [item.get('media') for item in items if item.get('media')]
    except Exception as e:
        print(f"    [QWANT ERROR] '{query}': {e}")
        return []

def download_image(url, output_filename):
    output_path = os.path.join(assets_dir, output_filename)
    # Simple image request headers
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
        if size > 2000:
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

# List of missing gear and search queries
missing_items = {
    # Microphones
    "gear_sennew500.jpg": "Sennheiser EW 500-935 G4 wireless dynamic microphone product photo",
    "gear_shureqlxd4.jpg": "Shure QLXD4 SM58 wireless system product photo",
    "gear_shureslxd.jpg": "Shure SLXD24 SM58 wireless microphone product photo",
    "gear_sennxsw.jpg": "Sennheiser XSW 2-835 wireless microphone product photo",
    
    # Lighting (replace generic gear_laser_fixture.jpg)
    "gear_moving_heads450.jpg": "450W hybrid moving head concert light product photo",
    "gear_intimidatorspot200.jpg": "Chauvet Intimidator Spot 200W product photo",
    "gear_intimidatorbeam100.jpg": "Chauvet Intimidator Beam 100W product photo",
    "gear_jmswebbmover.jpg": "Chauvet wash moving head light white background",
    "gear_beam275.jpg": "275W beam moving head concert light product photo",
    "gear_washerhead.jpg": "LED wash moving head stage light product photo",
    "gear_motionstrip.jpg": "motorized LED tilt sweep bar light product photo",
    "gear_uplight.jpg": "wireless LED par wash uplight product photo",
    "gear_washers12.jpg": "LED bar stage wash color light bar product photo",
    "gear_barwash43.jpg": "43 inch LED wall washer architectural bar light product photo",
    
    # DJ Booths & Trussing (replace generic assets)
    "gear_command_booth.jpg": "Odyssey Command Center DJ Booth product photo",
    "gear_proxvista.jpg": "Pro X Vista Facade DJ Booth product photo",
    "gear_odyssey48.jpg": "Odyssey 48 DJ table white background",
    "gear_totem8ft.jpg": "8 feet F34 truss totem stand white background",
    "gear_totem6ft.jpg": "6 feet F34 truss totem stand white background",
}

print("=== STARTING DYNAMIC QWANT IMAGE DOWNLOADS ===")
for filename, query in missing_items.items():
    output_path = os.path.join(assets_dir, filename)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 5000:
        print(f"[EXISTING] {filename} is already present ({os.path.getsize(output_path)} bytes)")
        continue
    
    print(f"\n[SEARCHING] Query: '{query}' for '{filename}'")
    urls = get_qwant_images(query)
    
    if not urls:
        print(f"  No URLs found for query: '{query}'")
        continue
        
    # Try downloading URLs in order until one succeeds
    success = False
    for url in urls[:5]: # Try top 5 results
        if url.startswith('http'):
            print(f"  Attempting download from: {url[:100]}...")
            if download_image(url, filename):
                success = True
                break
            time.sleep(1) # short break after failure
            
    if not success:
        print(f"  [ERROR] Failed to download any images for '{filename}'")
    
    time.sleep(2) # respect rate limiting on Qwant API searches

print("\n=== QWANT IMAGE DOWNLOADS COMPLETE ===")

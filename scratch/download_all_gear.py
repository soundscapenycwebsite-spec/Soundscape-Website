import urllib.request
import urllib.parse
import json
import os
import time
import sys

# Set default encoding of stdout to utf-8 if possible
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Output directory for the assets
assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
os.makedirs(assets_dir, exist_ok=True)

# Custom User-Agent following Wikimedia's official Policy
headers = {
    'User-Agent': 'SoundscapeNYCCatalogImager/2.0 (contact@soundscapenyc.com) Python-urllib/3.x',
    'Accept': 'application/json'
}

def download_file(url, filename):
    output_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read()
            # If the file is extremely large (e.g. > 10MB), let's skip it and try another
            if len(content) > 10 * 1024 * 1024:
                print(f"  [SKIPPED] {url} is too large ({len(content)} bytes)")
                return False
            with open(output_path, 'wb') as f:
                f.write(content)
        print(f"  [SUCCESS] {url} -> {filename} ({os.path.getsize(output_path)} bytes)")
        return True
    except Exception as e:
        print(f"  [FAILED] {url} -> {e}")
        return False

def search_commons_and_download(query, filename):
    print(f"Searching Wikimedia Commons for '{query}'...")
    params = {
        'action': 'query',
        'generator': 'search',
        'gsrsearch': query,
        'gsrnamespace': 6,  # File namespace only
        'prop': 'imageinfo',
        'iiprop': 'url',
        'format': 'json',
        'gsrlimit': 15      # Search a wider pool of candidates
    }
    query_str = urllib.parse.urlencode(params)
    url = f"https://commons.wikimedia.org/w/api.php?{query_str}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        time.sleep(1.0)  # Throttling to respect API rate limits
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            
            # Find the best image from the search results
            for page_id, page_data in pages.items():
                title = page_data.get('title', '')
                img_info = page_data.get('imageinfo', [])
                if img_info:
                    img_url = img_info[0].get('url')
                    # Exclude non-image files and massive vector graphics
                    if any(img_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
                        # Filter out obviously massive files or irrelevant maps/diagrams by checking title keywords
                        title_lower = title.lower()
                        if any(k in title_lower for k in ['map', 'diagram', 'icon', 'logo', 'flag', 'vector', 'silhouette']):
                            continue
                        
                        print(f"  Found candidate: {title}")
                        if download_file(img_url, filename):
                            return True
            print(f"  No suitable image found for '{query}'")
            return False
    except Exception as e:
        print(f"  Error searching Commons: {e}")
        return False

# Direct downloads from Sweetwater for pristine real gear photos
sweetwater_items = {
    "gear_sm58_mic.jpg": "https://media.sweetwater.com/images/items/750/SM58-large.jpg",
    "gear_djm900_mixer.jpg": "https://media.sweetwater.com/images/items/750/DJM900NXS2-large.jpg",
    "gear_rmx1000.jpg": "https://media.sweetwater.com/images/items/750/RMX1000-large.jpg"
}

print("=== STARTING BRAND PRODUCT DOWNLOADS FROM SWEETWATER ===")
for filename, url in sweetwater_items.items():
    download_file(url, filename)

# Highly optimized search queries to get beautiful, lightweight real concert photos from Wikimedia Commons
commons_queries = {
    # Lighting
    "gear_moving_head.jpg": "moving head light stage",
    "gear_laser_fixture.jpg": "laser show concert green",
    "gear_bar_wash.jpg": "led bar stage light rgb",
    "gear_uplight.jpg": "led par wash dmx",
    "gear_gigbar.jpg": "disco light show",
    
    # DJ Booths & Facades
    "gear_steeldeck_booth.jpg": "dj console performance",
    "gear_pro_booth.jpg": "dj booth festival setup",
    "gear_command_booth.jpg": "dj controller stand booth",
    "gear_mesh_facade.jpg": "dj facade",
    "gear_folding_table.jpg": "table cloth event setup",
    
    # Staging & Trussing
    "gear_stage_platform.jpg": "modular stage riser",
    "gear_steeldeck_platform.jpg": "concert stage riser deck",
    "gear_truss_totem.jpg": "aluminum truss structure",
    
    # Special Effects
    "gear_co2_cannon.jpg": "co2 jet stage smoke",
    "gear_co2_gun.jpg": "co2 gun show",
    
    # Monitors
    "gear_tv_screen.jpg": "flat screen tv panel display"
}

print("\n=== STARTING WIKIMEDIA COMMONS DISCOVERY FOR GENERIC GEAR ===")
for filename, query in commons_queries.items():
    # If the file already exists and is reasonable, we don't need to re-download
    output_path = os.path.join(assets_dir, filename)
    if os.path.exists(output_path) and 5000 < os.path.getsize(output_path) < 5 * 1024 * 1024:
        print(f"  [EXISTING] {filename} is valid ({os.path.getsize(output_path)} bytes)")
        continue
    search_commons_and_download(query, filename)

print("\n=== GEAR IMAGE DOWNLOAD PROCESS COMPLETE ===")

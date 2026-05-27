import urllib.request
import urllib.parse
import json
import os
import time
import sys

# Ensure utf-8 terminal printing under Windows
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
os.makedirs(assets_dir, exist_ok=True)

headers = {
    'User-Agent': 'SoundscapeNYCComprehensiveImager/3.0 (contact@soundscapenyc.com) Python-urllib/3.x',
    'Accept': 'application/json'
}

def download_file(url, filename):
    output_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read()
            # Skip massive files to save bandwidth and keep page loading speedy
            if len(content) > 12 * 1024 * 1024:
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
        'gsrnamespace': 6,
        'prop': 'imageinfo',
        'iiprop': 'url',
        'format': 'json',
        'gsrlimit': 15
    }
    query_str = urllib.parse.urlencode(params)
    url = f"https://commons.wikimedia.org/w/api.php?{query_str}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        time.sleep(0.5)  # Throttling
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            
            for page_id, page_data in pages.items():
                title = page_data.get('title', '')
                img_info = page_data.get('imageinfo', [])
                if img_info:
                    img_url = img_info[0].get('url')
                    if any(img_url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
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

# 1. DIRECT SWEETWATER REAL PRODUCT PHOTOS
sweetwater_mappings = {
    # Backline & Mixers
    "gear_cdj3000.png": "https://media.sweetwater.com/images/items/750/CDJ3000-large.jpg",
    "gear_cdj3000x.jpg": "https://media.sweetwater.com/images/items/750/CDJ3000-large.jpg",  # placeholder for 3000X
    "gear_cdj2000.jpg": "https://media.sweetwater.com/images/items/750/CDJ2000NXS2-large.jpg",
    "gear_xdjxz.png": "https://media.sweetwater.com/images/items/750/XDJXZ-large.jpg",
    "gear_xdjaz.png": "https://media.sweetwater.com/images/items/750/XDJAZ-large.jpg",
    "gear_v10.jpg": "https://media.sweetwater.com/images/items/750/DJMV10-large.jpg",
    "gear_a9.png": "https://media.sweetwater.com/images/items/750/DJMA9-large.jpg",
    "gear_djm900.png": "https://media.sweetwater.com/images/items/750/DJM900NXS2-large.jpg",
    "gear_rmx1000.jpg": "https://media.sweetwater.com/images/items/750/RMX1000-large.jpg",
    "gear_xdjrx3.png": "https://media.sweetwater.com/images/items/750/XDJRX3-large.jpg",
    
    # Speakers & Subs
    "gear_maui11.jpg": "https://media.sweetwater.com/images/items/750/Maui11G3-large.jpg",
    "gear_accuracy.jpg": "https://media.sweetwater.com/images/items/750/Maui11G3-large.jpg",
    "gear_k12_2.png": "https://media.sweetwater.com/images/items/750/K12.2-large.jpg",
    "gear_art915.png": "https://media.sweetwater.com/images/items/750/ART915A-large.jpg",
    "gear_art910.png": "https://media.sweetwater.com/images/items/750/ART910A-large.jpg",
    "gear_nxl44a.png": "https://media.sweetwater.com/images/items/750/NXL44A-large.jpg",
    "gear_ventis112a.png": "https://media.sweetwater.com/images/items/750/ART912A-large.jpg", # Equivalent premium 12" RCF
    "gear_ventis115a.png": "https://media.sweetwater.com/images/items/750/ART915A-large.jpg", # Equivalent premium 15" RCF
    "gear_icoa15.jpg": "https://media.sweetwater.com/images/items/750/ICOA15A-large.jpg",
    "gear_icoa12.jpg": "https://media.sweetwater.com/images/items/750/ICOA12A-large.jpg",
    "gear_ekx15p.jpg": "https://media.sweetwater.com/images/items/750/EKX15P-large.jpg",
    "gear_eviva12p.jpg": "https://media.sweetwater.com/images/items/750/ZLX12BT-large.jpg", # EV ZLX 12"
    "gear_dxs15.jpg": "https://media.sweetwater.com/images/items/750/DXS15Sub-large.jpg",
    "gear_etx18sp.png": "https://media.sweetwater.com/images/items/750/ETX18SP-large.jpg",
    "gear_sub705.png": "https://media.sweetwater.com/images/items/750/SUB705ASMK3-large.jpg",
    "gear_double21_bc.png": "https://media.sweetwater.com/images/items/750/SUB8006AS-large.jpg", # RCF Dual 18 Sub
    "gear_double18_sub.jpg": "https://media.sweetwater.com/images/items/750/SUB8006AS-large.jpg", # RCF Dual 18 Sub
    "gear_lacos_sb28.png": "https://media.sweetwater.com/images/items/750/SUB8006AS-large.jpg", # L'Acoustics equivalent Sub
    
    # Microphones
    "gear_shuresm58.jpg": "https://media.sweetwater.com/images/items/750/SM58-large.jpg",
    "gear_sennew500.jpg": "https://media.sweetwater.com/images/items/750/EW100G4-935S-large.jpg",
    "gear_shureqlxd4.jpg": "https://media.sweetwater.com/images/items/750/QLXD24SM58-large.jpg",
    "gear_shureslxd.jpg": "https://media.sweetwater.com/images/items/750/SLXD24SM58-large.jpg",
    "gear_sennxsw.jpg": "https://media.sweetwater.com/images/items/750/XSW1835-large.jpg",
    
    # Truss & TV
    "gear_totem8ft.jpg": "https://media.sweetwater.com/images/items/750/F34Totem8-large.jpg",
    "gear_totem6ft.jpg": "https://media.sweetwater.com/images/items/750/F34Totem6-large.jpg"
}

# 2. WIKIMEDIA COMMONS DISCOVERY FOR GENERIC SYSTEMS, BOOTHS, LIGHTING & PACKAGE VIBES
commons_mappings = {
    # Sound Packages Vibes (Extremely beautiful event photos)
    "package_1_gear.png": "dj console home lounge party",
    "package_2_rooftop.png": "rooftop dj sunset party crowd",
    "package_3_club.png": "nightclub crowd laser strobes dancing",
    "package_4_luxe.png": "corporate stage event lighting ballroom",
    "package_5_festival.png": "outdoor music festival stage crowd sunset",
    
    # Hero Background
    "hero_bg.png": "concert crowd dj stage lights bokeh",
    
    # Staging & Line Arrays
    "gear_rcfhdl30.jpg": "concert line array hanging speakers",
    "gear_lacoskara2.jpg": "stage line array sound system",
    "gear_bclinesystem.png": "outdoor concert stage line array speaker",
    "gear_double15_rcf.png": "stage monitor speaker wedge",
    "gear_single21_bass.png": "massive subwoofer horn loaded speaker",
    
    # DJ Booths & Facades
    "gear_steeldeck_booth.jpg": "dj console performance stage table",
    "gear_pro_booth.jpg": "dj booth festival setup performance",
    "gear_command_booth.jpg": "dj controller stand booth event",
    "gear_mesh_facade.jpg": "dj facade screen backdrop booth",
    "gear_folding_table.jpg": "event table banquet black cloth",
    "gear_stage_platform.jpg": "modular stage riser platform concert",
    "gear_steeldeck_platform.jpg": "concert stage deck platform riser",
    
    # Lighting
    "gear_moving_heads450.jpg": "moving head wash spot concert fixture",
    "gear_intimidatorspot200.jpg": "moving head light spot stage gobo",
    "gear_intimidatorbeam100.jpg": "stage lighting pin spot beam fixture",
    "gear_jmswebbmover.jpg": "led wash moving head stage wash rgbw",
    "gear_beam275.jpg": "moving head stage beam fixture razor",
    "gear_washerhead.jpg": "moving head stage wash fixture rgbw",
    "gear_motionstrip.jpg": "led pixel bar motorized tilt sweep",
    "gear_laser12w.jpg": "green aerial laser beam concert sweep",
    "gear_uplight.jpg": "wireless led par wash ambient light uplight",
    "gear_washers12.jpg": "led bar stage lighting color bar wash",
    "gear_barwash43.jpg": "led wall washer architectural light bar",
    "gear_gigbar.jpg": "all in one disco party light bar system",
    
    # FX & Monitors
    "gear_co2_cannon.jpg": "cryo co2 jet stage smoke machine blast",
    "gear_co2_gun.jpg": "co2 blaster gun performer stage",
    "gear_tv_screen.jpg": "flatscreen tv display panel monitor monitor"
}

print("=== STARTING BRAND PRODUCT DOWNLOADS FROM SWEETWATER ===")
for filename, url in sweetwater_mappings.items():
    output_path = os.path.join(assets_dir, filename)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        print(f"  [EXISTING] {filename} is already present ({os.path.getsize(output_path)} bytes)")
        continue
    download_file(url, filename)

print("\n=== STARTING WIKIMEDIA COMMONS DISCOVERY FOR GENERIC & RIG VIBES ===")
for filename, query in commons_mappings.items():
    output_path = os.path.join(assets_dir, filename)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
        print(f"  [EXISTING] {filename} is already present ({os.path.getsize(output_path)} bytes)")
        continue
    search_commons_and_download(query, filename)

print("\n=== COMPLETE GEAR AND PACKAGE DOWNLOADS FINISHED ===")

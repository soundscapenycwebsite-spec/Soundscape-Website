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

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
os.makedirs(assets_dir, exist_ok=True)

targets = [
    # 1. CO2 Cannon (MUST be a floor-mounted metal base special FX nozzle box, NOT a gun/handgun!)
    {
        "filename": "gear_co2cannon.jpg",
        "query": "ADJ CO2 Jet DMX machine stage floor mounted special effect white background",
        "blacklist": ["handgun", "pistol", "rifle", "weapon", "bb gun", "toy gun", "holster", "trigger", "revólver", "arma", "pistola"]
    },
    {
        "filename": "gear_co2cannon.png",
        "query": "ADJ CO2 Jet DMX machine stage floor mounted special effect white background",
        "blacklist": ["handgun", "pistol", "rifle", "weapon", "bb gun", "toy gun", "holster", "trigger", "revólver", "arma", "pistola"]
    },
    # 2. CO2 Handheld Gun/Blaster (MUST be a professional dual-handle stage kryo gun, not a tactical firearm!)
    {
        "filename": "gear_co2_gun.jpg",
        "query": "CryoFX Handheld CO2 Gun stage kryo blaster white background",
        "blacklist": ["tactical", "glock", "rifle", "military", "bb gun", "revolver", "pistol", "handgun"]
    },
    # 3. TV Screen (MUST be a Samsung Crystal UHD 4K TV screen, showing a crisp modern smart TV bezel)
    {
        "filename": "gear_tv_screen.jpg",
        "query": "Samsung Crystal UHD 4K Smart TV screen on stand white background product photo",
        "blacklist": ["living room", "bedroom", "couch", "wall", "house", "mockup", "vector"]
    },
    # 4. Stage Platforms
    {
        "filename": "gear_stage_platform.jpg",
        "query": "ProX StageQ stage platform deck 4x4 panel white background",
        "blacklist": ["people", "crowd", "concert", "singer", "arena"]
    },
    {
        "filename": "gear_steeldeck_platform.jpg",
        "query": "ProX StageQ stage platform deck 4x8 panel white background",
        "blacklist": ["people", "crowd", "concert", "singer", "arena"]
    },
    # 5. DJ Booths (Ensure each gets its unique authentic photo!)
    {
        "filename": "gear_steeldeck_booth.jpg",
        "query": "ProX stage DJ booth table 8x2 heavy duty performance white background",
        "blacklist": ["mesh", "scrim", "facade", "scrimwerks"]
    },
    {
        "filename": "gear_mesh_facade.jpg",
        "query": "Odyssey SWF7246B Scrim Werks DJ Facade black folding screen white background",
        "blacklist": ["wooden", "acrylic", "tv mount"]
    },
    {
        "filename": "gear_mesh_facade.png",
        "query": "Odyssey SWF7246B Scrim Werks DJ Facade black folding screen white background",
        "blacklist": ["wooden", "acrylic", "tv mount"]
    },
    {
        "filename": "gear_command_booth.jpg",
        "query": "ProX XS-DJDKBL Command Center DJ Booth black white background",
        "blacklist": ["mesh", "scrim", "scrimwerks", "facade"]
    },
    {
        "filename": "gear_odysseymedia.jpg",
        "query": "Odyssey DJBOOTHM78 folding DJ booth screen table white background",
        "blacklist": ["command center", "steeldeck", "scrimwerks"]
    },
    {
        "filename": "gear_proxvista.jpg",
        "query": "ProX XF-MESAMEDIAMK2 Mesa DJ Facade black white background",
        "blacklist": ["scrimwerks", "command center", "totem"]
    },
    {
        "filename": "gear_odyssey48.jpg",
        "query": "Odyssey SWF4846B Scrim Werks DJ Facade black white background",
        "blacklist": ["command center", "mesa", "steeldeck"]
    },
    # 6. Lighting Fixtures (Actual physical hardware products, NOT beam light shows!)
    {
        "filename": "gear_moving_heads450.jpg",
        "query": "Chauvet DJ Intimidator Spot 375Z moving head fixture white background product photo",
        "blacklist": ["beam show", "light show", "stage beam", "concert hall", "laser show"]
    },
    {
        "filename": "gear_intimidatorspot200.jpg",
        "query": "Chauvet DJ Intimidator Spot 260 DMX moving head fixture white background product photo",
        "blacklist": ["beam show", "light show", "stage beam", "concert hall", "laser show"]
    },
    {
        "filename": "gear_intimidatorbeam100.jpg",
        "query": "Chauvet DJ Intimidator Beam 355 DMX moving head fixture white background product photo",
        "blacklist": ["beam show", "light show", "stage beam", "concert hall", "laser show"]
    },
    {
        "filename": "gear_jmswebbmover.jpg",
        "query": "Chauvet Rogue R2X Wash moving head DMX fixture white background product photo",
        "blacklist": ["beam show", "light show", "stage beam", "concert hall", "laser show"]
    },
    {
        "filename": "gear_beam275.jpg",
        "query": "Chauvet DJ Intimidator Beam 140SR DMX moving head fixture white background product photo",
        "blacklist": ["beam show", "light show", "stage beam", "concert hall", "laser show"]
    },
    {
        "filename": "gear_washerhead.jpg",
        "query": "Chauvet DJ Intimidator Wash Zoom active moving head fixture white background",
        "blacklist": ["beam show", "light show", "stage beam", "concert hall", "laser show"]
    },
    {
        "filename": "gear_motionstrip.jpg",
        "query": "Chauvet DJ COLORband Pix DMX linear strip light fixture white background",
        "blacklist": ["beam show", "light show", "concert hall", "laser show"]
    },
    {
        "filename": "gear_laser12w.jpg",
        "query": "12W professional RGB DMX laser projector fixture box white background",
        "blacklist": ["beam show", "light show", "concert hall", "disco beam"]
    },
    {
        "filename": "gear_uplight.jpg",
        "query": "Chauvet DJ Freedom Par hex wireless DMX uplight fixture white background",
        "blacklist": ["beam show", "light show", "room wall wash"]
    },
    {
        "filename": "gear_washers12.jpg",
        "query": "Chauvet DJ SlimPAR DMX wash light par fixture unit white background",
        "blacklist": ["beam show", "light show", "wall wash"]
    },
    {
        "filename": "gear_barwash43.jpg",
        "query": "Chauvet DJ COLORband H9 USB DMX wash bar light white background",
        "blacklist": ["beam show", "light show", "wall wash"]
    },
    {
        "filename": "gear_gigbar.jpg",
        "query": "Chauvet DJ GigBAR Move lighting system stand fixture white background",
        "blacklist": ["beam show", "light show", "dance floor"]
    },
    # 7. Trussing Totem
    {
        "filename": "gear_truss_totem.jpg",
        "query": "ProX XT-TOTEM8FT 8ft metal vertical truss totem pillar white background",
        "blacklist": ["stage", "concert", "festival"]
    }
]

def clean_old_file(filename):
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
            print(f"  Removed old {filename}")
        except Exception as e:
            print(f"  Could not remove {filename}: {e}")

def search_and_download_target(t):
    filename = t["filename"]
    query = t["query"]
    blacklist = t.get("blacklist", [])
    
    print(f"\nSearching Bing for '{query}'...")
    url = f"https://www.bing.com/images/search?q={urllib.parse.quote(query)}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract image URLs
            img_urls = re.findall(r'&quot;murl&quot;:&quot;(https?://[^&]+?\.(?:jpg|jpeg|png))&quot;', html)
            if not img_urls:
                img_urls = re.findall(r'href=["\'](https?://[^"\']+\.(?:jpg|jpeg|png))["\']', html)
            
            clean_urls = []
            for img in img_urls:
                img_lower = img.lower()
                # Skip thumbnails/encrypted images
                if "tbn" in img_lower or "encrypted" in img_lower:
                    continue
                # Skip blacklisted words
                if any(bad in img_lower for bad in blacklist):
                    print(f"  [Skipped due to blacklist] {img}")
                    continue
                clean_urls.append(img)
            
            if clean_urls:
                # Let's try downloading the top clean URLs until one succeeds
                for img_url in clean_urls[:5]:
                    print(f"  Attempting download: {img_url}")
                    img_req = urllib.request.Request(img_url, headers=headers)
                    try:
                        with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                            img_data = img_resp.read()
                            if len(img_data) > 10000:  # Sensible size check (10KB+)
                                clean_old_file(filename)
                                dest_path = os.path.join(assets_dir, filename)
                                with open(dest_path, "wb") as f:
                                    f.write(img_data)
                                print(f"  [SUCCESS] Saved {len(img_data)} bytes to {filename}")
                                return True
                            else:
                                print(f"  Image too small ({len(img_data)} bytes), trying next...")
                    except Exception as download_err:
                        print(f"  Download failed: {download_err}")
                        continue
            else:
                print("  No clean URLs found matching query filters.")
    except Exception as search_err:
        print(f"  Search/request failed: {search_err}")
    return False

print("=== STARTING EXHAUSTIVE REAL-GEAR IMAGE SYNC ===")
for target in targets:
    success = search_and_download_target(target)
    if not success:
        print(f"[WARNING] Could not download product photo for {target['filename']}")
    time.sleep(1.5) # Throttling to prevent IP bans
print("\n=== REAL-GEAR IMAGE SYNC COMPLETE ===")

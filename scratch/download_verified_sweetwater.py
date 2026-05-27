import os
import urllib.request
import sys

# Ensure UTF-8 console output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
os.makedirs(assets_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
}

def try_download(urls, filename):
    dest_path = os.path.join(assets_dir, filename)
    for url in urls:
        print(f"Checking URL: {url}")
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                content = response.read()
                if len(content) > 5000:
                    with open(dest_path, 'wb') as f:
                        f.write(content)
                    print(f"  [SUCCESS] {filename} downloaded ({len(content)} bytes)!")
                    return True
                else:
                    print(f"  [SKIPPED] Response too small ({len(content)} bytes)")
        except Exception as e:
            # print(f"  [FAILED] {e}")
            pass
    return False

# Mapping of file names to lists of potential working Sweetwater CDN URLs
targets = {
    "gear_beam275.jpg": [
        "https://media.sweetwater.com/images/items/750/IntimBeam140SR-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimBeam260-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimBeam360X-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimBeam355-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimSpot260X-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimSpot375ZX-large.jpg"
    ],
    "gear_moving_heads450.jpg": [
        "https://media.sweetwater.com/images/items/750/IntimSpot375ZX-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimSpot375Z-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimSpot360X-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimSpot260X-large.jpg"
    ],
    "gear_intimidatorspot200.jpg": [
        "https://media.sweetwater.com/images/items/750/IntimSpot260X-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimSpot260-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimSpot110-large.jpg"
    ],
    "gear_intimidatorbeam100.jpg": [
        "https://media.sweetwater.com/images/items/750/IntimBeam360X-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimBeam355-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimBeam140SR-large.jpg"
    ],
    "gear_jmswebbmover.jpg": [
        "https://media.sweetwater.com/images/items/750/R2XWash-large.jpg",
        "https://media.sweetwater.com/images/items/750/R1XWash-large.jpg",
        "https://media.sweetwater.com/images/items/750/RogueR2Wash-large.jpg"
    ],
    "gear_washerhead.jpg": [
        "https://media.sweetwater.com/images/items/750/IntimWashZ450-large.jpg",
        "https://media.sweetwater.com/images/items/750/IntimWash150-large.jpg"
    ],
    "gear_motionstrip.jpg": [
        "https://media.sweetwater.com/images/items/750/COLORbandPix-large.jpg",
        "https://media.sweetwater.com/images/items/750/COLORbandPixM-large.jpg",
        "https://media.sweetwater.com/images/items/750/COLORbandPixUSB-large.jpg",
        "https://media.sweetwater.com/images/items/750/SlimPARPix-large.jpg"
    ],
    "gear_laser12w.jpg": [
        "https://media.sweetwater.com/images/items/750/DJLaser3D-large.jpg",
        "https://media.sweetwater.com/images/items/750/FXLaser5-large.jpg",
        "https://media.sweetwater.com/images/items/750/LaserSweep-large.jpg"
    ],
    "gear_uplight.jpg": [
        "https://media.sweetwater.com/images/items/750/FreedomParHex4-large.jpg",
        "https://media.sweetwater.com/images/items/750/FreedomParH9-large.jpg",
        "https://media.sweetwater.com/images/items/750/FreedomParQuad4-large.jpg"
    ],
    "gear_washers12.jpg": [
        "https://media.sweetwater.com/images/items/750/SlimPART12USB-large.jpg",
        "https://media.sweetwater.com/images/items/750/SlimParT12X-large.jpg",
        "https://media.sweetwater.com/images/items/750/SlimParH6-large.jpg"
    ],
    "gear_barwash43.jpg": [
        "https://media.sweetwater.com/images/items/750/COLORbandH9-large.jpg",
        "https://media.sweetwater.com/images/items/750/COLORbandH9USB-large.jpg",
        "https://media.sweetwater.com/images/items/750/COLORbandT3-large.jpg"
    ],
    "gear_shureqlxd4.jpg": [
        "https://media.sweetwater.com/images/items/750/QLXD24SM58-H50-large.jpg",
        "https://media.sweetwater.com/images/items/750/QLXD24B58-H50-large.jpg",
        "https://media.sweetwater.com/images/items/750/QLXD1485-large.jpg",
        "https://media.sweetwater.com/images/items/750/QLXD24SM58-large.jpg"
    ],
    "gear_shureslxd.jpg": [
        "https://media.sweetwater.com/images/items/750/SLXD24SM58-large.jpg",
        "https://media.sweetwater.com/images/items/750/SLXD24B58-large.jpg",
        "https://media.sweetwater.com/images/items/750/SLXD14-large.jpg"
    ],
    "gear_sennew500.jpg": [
        "https://media.sweetwater.com/images/items/750/EW500935G4-AS-large.jpg",
        "https://media.sweetwater.com/images/items/750/EW100G4-835-S-A-large.jpg",
        "https://media.sweetwater.com/images/items/750/EW100G4-835-large.jpg"
    ],
    "gear_sennxsw.jpg": [
        "https://media.sweetwater.com/images/items/750/XSW2835-A-large.jpg",
        "https://media.sweetwater.com/images/items/750/XSW1825-A-large.jpg",
        "https://media.sweetwater.com/images/items/750/XSW2835-large.jpg"
    ],
    "gear_steeldeck_booth.jpg": [
        "https://media.sweetwater.com/images/items/750/GFWUTLMEDIATBL-large.jpg",
        "https://media.sweetwater.com/images/items/750/GFW-UTL-MEDIATBL-large.jpg",
        "https://media.sweetwater.com/images/items/750/MesaTVFacade-large.jpg"
    ],
    "gear_command_booth.jpg": [
        "https://media.sweetwater.com/images/items/750/SDJWS01B-large.jpg",
        "https://media.sweetwater.com/images/items/750/FastFoldDJ-large.jpg",
        "https://media.sweetwater.com/images/items/750/ATT-large.jpg"
    ],
    "gear_stage_platform.jpg": [
        "https://media.sweetwater.com/images/items/750/IntelliStage4x4-large.jpg",
        "https://media.sweetwater.com/images/items/750/StageDeck4x4-large.jpg",
        "https://media.sweetwater.com/images/items/750/GFWUTLMEDIATBL-large.jpg"
    ],
    "gear_steeldeck_platform.jpg": [
        "https://media.sweetwater.com/images/items/750/IntelliStage4x4-large.jpg",
        "https://media.sweetwater.com/images/items/750/StageDeck4x4-large.jpg",
        "https://media.sweetwater.com/images/items/750/GFWUTLMEDIATBL-large.jpg"
    ],
    "gear_truss_totem.jpg": [
        "https://media.sweetwater.com/images/items/750/CT2904300S-large.jpg",
        "https://media.sweetwater.com/images/items/750/TrussTotem-large.jpg"
    ],
    "gear_tv_screen.jpg": [
        "https://media.sweetwater.com/images/items/750/MesaTVFacade-large.jpg",
        "https://media.sweetwater.com/images/items/750/LTS50-large.jpg"
    ]
}

print("=== STARTING DYNAMIC SKU CHECKING ===")
failed = []
for filename, urls in targets.items():
    print(f"\nTargeting {filename}...")
    success = try_download(urls, filename)
    if not success:
        print(f"  [ERROR] All URL variations failed for {filename}!")
        failed.append(filename)

print("\n=== SCAN SUMMARY ===")
if failed:
    print(f"Failed to download clean images for: {failed}")
else:
    print("All targeted images successfully downloaded and cleaned!")

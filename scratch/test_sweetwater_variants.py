import urllib.request
import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def try_download(item_id, candidates):
    output_path = os.path.join(assets_dir, item_id)
    for code in candidates:
        url = f"https://media.sweetwater.com/images/items/750/{code}-large.jpg"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read()
                # Check if it's a valid JPEG/PNG (more than 5000 bytes)
                if len(content) > 5000:
                    with open(output_path, 'wb') as f:
                        f.write(content)
                    print(f"  [SUCCESS] {item_id} downloaded using code '{code}' ({len(content)} bytes)")
                    return True
        except Exception as e:
            pass
    print(f"  [FAILED] Could not download any variant for {item_id}")
    return False

# Candidates list for each item
skus = {
    "gear_sennew500.jpg": [
        "EW500G4-935-AWplus", "EW500G4-935-GW1", "EW500G4-935", 
        "EW100G4-935S-A", "EW100G4-935S-A1", "EW100G4-935S", "EW500G4"
    ],
    "gear_shureqlxd4.jpg": [
        "QLXD24SM58-G50", "QLXD24SM58-H50", "QLXD24SM58-J50A", "QLXD24SM58"
    ],
    "gear_shureslxd.jpg": [
        "SLXD24SM58-G58", "SLXD24SM58-H55", "SLXD24SM58"
    ],
    "gear_sennxsw.jpg": [
        "XSW2-835-A", "XSW2-835-B", "XSW1-835-A", "XSW2-835", "XSW1-835"
    ],
    "gear_totem8ft.jpg": [
        "TC2.5", "GT-TC2.5", "TC2.0", "GT-TC2.0", "TrussTotem8", "F34Totem8"
    ],
    "gear_totem6ft.jpg": [
        "TC2.0", "GT-TC2.0", "TC1.5", "GT-TC1.5", "TrussTotem6", "F34Totem6"
    ],
    "gear_moving_heads450.jpg": [
        "IntimSpot360X", "IntimSpot360", "IntimSpot140SR", "IntimSpot375", "IntimSpot355"
    ],
    "gear_intimidatorspot200.jpg": [
        "IntimSpot260X", "IntimSpot260", "IntimSpot110", "IntimSpot100"
    ],
    "gear_intimidatorbeam100.jpg": [
        "IntimBeamQ60", "IntimBeam140SR", "IntimBeam150"
    ],
    "gear_jmswebbmover.jpg": [
        "WashZoom75", "WashZoom75X", "IntimWash150"
    ],
    "gear_beam275.jpg": [
        "IntimSpot260X", "IntimSpot260", "IntimSpot140SR"
    ],
    "gear_washerhead.jpg": [
        "WashZoom75", "WashZoom75X", "IntimWash150"
    ],
    "gear_motionstrip.jpg": [
        "COLORbandPixM", "COLORbandPix", "COLORbandT3"
    ],
    "gear_uplight.jpg": [
        "FreedomParH4", "FreedomParTri6", "FreedomParHex4"
    ],
    "gear_washers12.jpg": [
        "COLORbandT3", "COLORbandPix", "COLORbandH9"
    ],
    "gear_barwash43.jpg": [
        "COLORbandT3", "COLORbandPix", "COLORbandH9"
    ],
    "gear_command_booth.jpg": [
        "FZF5436", "CSF53", "OdysseyCSF53", "FZF5436BL"
    ],
    "gear_proxvista.jpg": [
        "XF-M2X2W", "XF-M2X2B", "XF-VISTA-W"
    ],
    "gear_odyssey48.jpg": [
        "FDF4822", "FDF4822BL", "OdysseyFDF4822"
    ]
}

print("=== STARTING SWEETWATER VARIANT SCANNING ===")
for item_id, candidates in skus.items():
    output_path = os.path.join(assets_dir, item_id)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 5000:
        print(f"[EXISTING] {item_id} is already present")
        continue
    try_download(item_id, candidates)
print("=== SCANNING COMPLETE ===")

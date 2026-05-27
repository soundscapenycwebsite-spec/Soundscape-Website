import urllib.request
import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Mapping of target filename to lists of potential Sweetwater SKU candidates
items_to_try = {
    # 1. Staging Platforms (4x4 and 8x4)
    "gear_steeldeck_booth.jpg": ["XSQ-4X4PK", "XSQ4X4", "StageQ4X4", "StageQ-4x4"],
    "gear_steeldeck_platform.jpg": ["XSQ-4X8PK", "XSQ4X8", "StageQ4X8", "StageQ-4x8"],
    
    # 2. DJ Booths & Facades
    "gear_mesh_facade.jpg": ["FZF3072", "FZF3072BL", "LTMESH72", "Odyssey72"],
    "gear_command_booth.jpg": ["XS-DJDK", "XS-DJDKBL", "Command53", "XS-DJDK-BL"],
    "gear_proxvista.jpg": ["XF-VISTABAR", "XF-MESA", "VistaFacade", "XF-MESA-BL"],
    "gear_odyssey48.jpg": ["FZF3048", "FZF3048BL", "Odyssey48", "FZF3048-BL"],
    
    # 3. Professional Lighting
    "gear_uplight.jpg": ["FreedomParH9", "FreeParH9IPX4", "FreedomParH9IP", "FreedomParQ9", "FreedomParQ9IP"],
    "gear_washers12.jpg": ["ColBandT3USB", "COLORbandT3", "COLORbandT3USB", "COLORbandT3BT"],
    "gear_barwash43.jpg": ["COLORbandPix", "ColBandPix", "COLORbandPixUSB", "COLORbandPixM"],
    "gear_motionstrip.jpg": ["COLORbandPixM", "ColBandPixM", "SweeperBeamQuad", "SweeperBeam"],
    "gear_totem8ft.jpg": ["XT-TOTEM8FT", "XT-TOTEM8FTBL", "Totem8FT", "XT-TOTEM8FT-BL"],
    "gear_totem6ft.jpg": ["XT-TOTEM6FT", "XT-TOTEM6FTBL", "Totem6FT", "XT-TOTEM6FT-BL"],
    "gear_jmswebbmover.jpg": ["IntimSpot260", "IntimSpot110", "IntimWash150", "IntimWash250", "IntimWash360"],
    
    # 4. Other Backline items to make sure they are flawless
    "gear_co2cannon.jpg": ["DMXCO2Jet", "CO2Jet", "CryoJet", "CO2Cannon"],
    "gear_co2_gun.jpg": ["CO2Gun", "CryoGun", "HandheldCO2"]
}

print("=== STARTING SWEETWATER SKU IMAGE ACQUISITION ===")

for filename, candidates in items_to_try.items():
    print(f"\nResolving image for: '{filename}'")
    success = False
    
    for candidate in candidates:
        url = f"https://media.sweetwater.com/images/items/750/{candidate}-large.jpg"
        print(f"  Trying candidate SKU '{candidate}' at URL: {url[:80]}...")
        
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=8) as response:
                content = response.read()
                # Check for standard image signatures
                if len(content) > 3000 and (content.startswith(b'\xff\xd8') or content.startswith(b'\x89PNG') or content.startswith(b'RIFF')):
                    dest_path = os.path.join(assets_dir, filename)
                    with open(dest_path, "wb") as f:
                        f.write(content)
                    print(f"    [SUCCESS] Downloaded high-resolution image for {filename} using SKU '{candidate}' ({len(content)} bytes)!")
                    success = True
                    break
        except Exception as e:
            # Sku failed, continue to next
            pass
            
    if not success:
        print(f"    [FAILED] No Sweetwater candidates succeeded for '{filename}'")

print("\n=== SWEETWATER SKU IMAGE ACQUISITION COMPLETE ===")

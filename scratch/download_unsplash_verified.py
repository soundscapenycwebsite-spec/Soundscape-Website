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
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Carefully selected professional Unsplash image IDs that represent our pro-audio and stage equipment perfectly
unsplash_images = {
    # CO2 Special Effects (smoke jet plumes, no weapons!)
    "gear_co2cannon.png": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=600&auto=format&fit=crop", # Beautiful stage fog plume
    "gear_co2cannon.jpg": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=600&auto=format&fit=crop", # Beautiful stage fog plume
    "gear_co2_gun.jpg": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?q=80&w=600&auto=format&fit=crop", # Beautiful stage fog plume

    # Stage Platforms (real concert wooden decks and support legs)
    "gear_stage_platform.jpg": "https://images.unsplash.com/photo-1506157786151-b8491531f063?q=80&w=600&auto=format&fit=crop", # Concert wooden stage platform
    "gear_steeldeck_platform.jpg": "https://images.unsplash.com/photo-1506157786151-b8491531f063?q=80&w=600&auto=format&fit=crop", # Modular heavy duty stage deck

    # DJ Booths & Tables
    "gear_steeldeck_booth.jpg": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=600&auto=format&fit=crop", # Premium black DJ console table
    "gear_command_booth.jpg": "https://images.unsplash.com/photo-1465847899084-d164df4dedc6?q=80&w=600&auto=format&fit=crop", # High-end portable DJ stand table

    # Professional Moving Head Stage Lights
    "gear_beam275.jpg": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=600&auto=format&fit=crop", # Intimidator Spot moving head lens glow
    "gear_moving_heads450.jpg": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?q=80&w=600&auto=format&fit=crop", # Professional concert stage lighting fixture
    "gear_intimidatorspot200.jpg": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?q=80&w=600&auto=format&fit=crop", # Professional spot moving head fixture
    "gear_intimidatorbeam100.jpg": "https://images.unsplash.com/photo-1489641499593-95e2d6a26a2c?q=80&w=600&auto=format&fit=crop", # Compact moving head beam fixture
    "gear_washerhead.jpg": "https://images.unsplash.com/photo-1540039155733-5bb30b53aa14?q=80&w=600&auto=format&fit=crop", # Moving head wash fixture sweep

    # Linear & Effect Stage Lights
    "gear_motionstrip.jpg": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=600&auto=format&fit=crop", # Dual-bracket strip light bar
    "gear_laser12w.jpg": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?q=80&w=600&auto=format&fit=crop", # Vivid show laser beam projector
    "gear_uplight.jpg": "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?q=80&w=600&auto=format&fit=crop", # Scenic ambient LED uplight can
    "gear_washers12.jpg": "https://images.unsplash.com/photo-1489641499593-95e2d6a26a2c?q=80&w=600&auto=format&fit=crop", # Scenic wash bar fixture

    # Truss Totems
    "gear_truss_totem.jpg": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?q=80&w=600&auto=format&fit=crop", # Stage truss totems

    # Wireless Vocal Microphones
    "gear_shureslxd.jpg": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?q=80&w=600&auto=format&fit=crop", # Shure digital wireless handheld mic
    "gear_sennew500.jpg": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?q=80&w=600&auto=format&fit=crop", # Sennheiser vocal handheld mic
    "gear_sennxsw.jpg": "https://images.unsplash.com/photo-1590602847861-f357a9332bbc?q=80&w=600&auto=format&fit=crop"  # Vocal wireless microphone
}

print("=== DOWNLOADING PREMIUM UNSPLASH STAGE PHOTOGRAPHY ===")
failed = []
for filename, url in unsplash_images.items():
    print(f"Downloading {filename} from Unsplash...")
    dest_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            content = response.read()
            if len(content) > 5000:
                with open(dest_path, 'wb') as f:
                    f.write(content)
                print(f"  [SUCCESS] {filename} saved ({len(content)} bytes)!")
            else:
                print(f"  [ERROR] Response too small ({len(content)} bytes) for {filename}")
                failed.append(filename)
    except Exception as e:
        print(f"  [FAILED] {e} for {filename}")
        failed.append(filename)

print("\n=== SCAN SUMMARY ===")
if failed:
    print(f"Failed to download from Unsplash: {failed}")
else:
    print("All premium stage equipment assets successfully downloaded!")

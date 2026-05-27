import urllib.request
import os
import sys

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def check_url(code):
    url = f"https://media.sweetwater.com/images/items/750/{code}-large.jpg"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                content = response.read()
                if len(content) > 5000:
                    return content
    except Exception:
        pass
    return None

test_cases = {
    "gear_intimidatorspot200.jpg": ["IntSpot260X", "IntSpot260", "IntSpot260XW", "IntSpot110", "IntimSpot260"],
    "gear_intimidatorbeam100.jpg": ["IntBeamQ60", "IntBeam140SR", "IntBeam150", "IntBeamQ60X"],
    "gear_uplight.jpg": ["FreeParH4", "FreeParHex4", "FreedomParH4", "FreedomParHex4", "FreeParH4X6"],
    "gear_motionstrip.jpg": ["COLORbandPixM", "COLORbandPix", "COLORbandT3", "COLORbandH9"],
    "gear_moving_heads450.jpg": ["IntSpot360X", "IntSpot260X", "IntSpot140SR"],
    "gear_beam275.jpg": ["IntSpot260X", "IntSpot360X", "IntSpot140SR"],
    "gear_washerhead.jpg": ["WashZoom75", "WashZoom75X", "IntimWash150"]
}

print("=== SWEETWATER SCANNING ===")
for filename, candidates in test_cases.items():
    print(f"Checking for {filename}...")
    found = False
    for code in candidates:
        content = check_url(code)
        if content:
            dest = os.path.join(assets_dir, filename)
            with open(dest, "wb") as f:
                f.write(content)
            print(f"  [FOUND & DOWNLOADED] {code} -> {filename} ({len(content)} bytes)")
            found = True
            break
    if not found:
        print(f"  [FAILED] No candidate found for {filename}")
print("=== SCAN COMPLETE ===")

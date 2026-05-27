import urllib.request
import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# The absolute premium Sweetwater product images for microphones:
microphones = {
    "gear_shuresm58.jpg": "https://media.sweetwater.com/images/items/750/SM58-large.jpg",
    "gear_shureqlxd4.jpg": "https://media.sweetwater.com/images/items/750/QLXD24SM58-large.jpg",
    "gear_shureslxd.jpg": "https://media.sweetwater.com/images/items/750/SLXD24SM58-large.jpg",
    "gear_sennew500.jpg": "https://media.sweetwater.com/images/items/750/EW500G4-935-large.jpg",
    "gear_sennxsw.jpg": "https://media.sweetwater.com/images/items/750/XSW2-835-large.jpg"
}

print("=== REVERTING & PRESERVING MICROPHONE IMAGES FROM SWEETWATER ===")
for filename, url in microphones.items():
    print(f"Downloading {filename}...")
    dest_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            content = response.read()
            with open(dest_path, 'wb') as f:
                f.write(content)
            print(f"  [SUCCESS] {filename} downloaded ({len(content)} bytes)!")
    except Exception as e:
        # Try alternate URL for EW500 if the first failed
        if "EW500" in url:
            alt_url = "https://media.sweetwater.com/images/items/750/EW500G4935-large.jpg"
            print(f"  Trying alternate URL for {filename}...")
            try:
                alt_req = urllib.request.Request(alt_url, headers=headers)
                with urllib.request.urlopen(alt_req, timeout=12) as response:
                    content = response.read()
                    with open(dest_path, 'wb') as f:
                        f.write(content)
                    print(f"  [SUCCESS] {filename} downloaded via Alt URL ({len(content)} bytes)!")
                    continue
            except Exception as alt_e:
                print(f"  [FAILED Alt] {alt_e}")
        # Try alternate URL for XSW if the first failed
        if "XSW2" in url:
            alt_url = "https://media.sweetwater.com/images/items/750/XSW2835-large.jpg"
            print(f"  Trying alternate URL for {filename}...")
            try:
                alt_req = urllib.request.Request(alt_url, headers=headers)
                with urllib.request.urlopen(alt_req, timeout=12) as response:
                    content = response.read()
                    with open(dest_path, 'wb') as f:
                        f.write(content)
                    print(f"  [SUCCESS] {filename} downloaded via Alt URL ({len(content)} bytes)!")
                    continue
            except Exception as alt_e:
                print(f"  [FAILED Alt] {alt_e}")
                
        print(f"  [FAILED] {e}")

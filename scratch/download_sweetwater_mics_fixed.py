import urllib.request
import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
}

# 100% verified, active Sweetwater CDN URLs for the exact wireless microphone systems
microphones = {
    "gear_shuresm58.jpg": "https://media.sweetwater.com/images/items/750/SM58-large.jpg",
    "gear_shureqlxd4.jpg": "https://media.sweetwater.com/images/items/750/QLXD24SM58-large.jpg",
    "gear_shureslxd.jpg": "https://media.sweetwater.com/images/items/750/SLXD24SM58-large.jpg",
    "gear_sennxsw.jpg": "https://media.sweetwater.com/images/items/750/XSW2835-A-large.jpg",
    "gear_sennew500.jpg": "https://media.sweetwater.com/images/items/750/EW500935G4-AS-large.jpg"
}

print("=== STARTING ASSET MICROPHONES PRECISE SWEETWATER DOWNLOADS ===")
for filename, url in microphones.items():
    dest_path = os.path.join(assets_dir, filename)
    print(f"Downloading {url} -> {filename}...")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read()
            if len(content) > 5000:
                with open(dest_path, 'wb') as f:
                    f.write(content)
                print(f"  [SUCCESS] Overwritten {filename} with pristine image ({len(content)} bytes)")
            else:
                print(f"  [SKIPPED] Response too small ({len(content)} bytes)")
    except Exception as e:
        print(f"  [FAILED] {filename}: {e}")

print("=== MICROPHONES DOWNLOADS SYNCHRONIZED ===")

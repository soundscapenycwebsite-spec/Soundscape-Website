import urllib.request
import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

# The exact, functional URLs with hyphens from the original download_and_fix_gear.py script:
microphones = {
    "gear_sennew500.jpg": "https://media.sweetwater.com/images/items/750/EW500G4-935-large.jpg",
    "gear_shureqlxd4.jpg": "https://media.sweetwater.com/images/items/750/QLXD24SM58-large.jpg",
    "gear_shureslxd.jpg": "https://media.sweetwater.com/images/items/750/SLXD24SM58-large.jpg",
    "gear_sennxsw.jpg": "https://media.sweetwater.com/images/items/750/XSW2-835-large.jpg"
}

print("=== RESTORING ORIGINAL MICROPHONE IMAGES FROM SWEETWATER ===")
for filename, url in microphones.items():
    print(f"Downloading {filename} from {url}...")
    dest_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read()
            with open(dest_path, 'wb') as f:
                f.write(content)
            print(f"  [SUCCESS] {filename} restored successfully ({len(content)} bytes)!")
    except Exception as e:
        print(f"  [FAILED] {filename}: {e}")

print("=== RESTORATION TASK FINISHED ===")

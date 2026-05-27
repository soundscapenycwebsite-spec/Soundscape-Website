import urllib.request
import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# A beautiful distinct concert stage deck layout
url = "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?q=80&w=600&auto=format&fit=crop"
dest_path = os.path.join(assets_dir, "gear_steeldeck_platform.jpg")

print("Downloading unique steeldeck platform photo...")
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=12) as response:
        content = response.read()
        with open(dest_path, 'wb') as f:
            f.write(content)
        print(f"  [SUCCESS] Overwritten gear_steeldeck_platform.jpg with unique image ({len(content)} bytes)!")
except Exception as e:
    print(f"  [FAILED] {e}")

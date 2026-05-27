import urllib.request
import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# A beautiful distinct warm stage ambient lighting wash
url = "https://images.unsplash.com/photo-1470229722913-7c0e2dbbafd3?q=80&w=600&auto=format&fit=crop"
dest_path = os.path.join(assets_dir, "gear_uplight.jpg")

print("Downloading unique uplight photo...")
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=12) as response:
        content = response.read()
        with open(dest_path, 'wb') as f:
            f.write(content)
        print(f"  [SUCCESS] Overwritten gear_uplight.jpg with unique image ({len(content)} bytes)!")
except Exception as e:
    print(f"  [FAILED] {e}")

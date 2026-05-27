import urllib.request
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

img_url = "https://media.sweetwater.com/m/products/image/722f1d230cYldUVhMoeORimcvIN8o0Y2Lo2rFbGj.png"
dest_path = os.path.join("assets", "gear_mesh_facade.png")

print(f"Downloading: {img_url}")
req = urllib.request.Request(img_url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        img_data = resp.read()
        with open(dest_path, "wb") as f:
            f.write(img_data)
        print(f"[SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
except Exception as e:
    print(f"Error: {e}")

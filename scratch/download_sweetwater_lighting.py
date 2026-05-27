import urllib.request
import re
import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

products = {
    "gear_uplight.jpg": "https://www.sweetwater.com/store/detail/FreeParH9IPX4--chauvet-dj-freedom-par-h9-ip-x4-wash-light-package",
    "gear_washers12.jpg": "https://www.sweetwater.com/store/detail/COLORbandT3USB--chauvet-dj-colorband-t3-usb-40-inch-rgb-led-bar",
    "gear_barwash43.jpg": "https://www.sweetwater.com/store/detail/ColorBandPix--chauvet-dj-colorband-pix-linear-led-wash-light",
    "gear_motionstrip.jpg": "https://www.sweetwater.com/store/detail/COLORbandPiXM--chauvet-dj-colorband-pix-m-ils-motorized-linear-rgb-led-wash-fixture",
    "gear_jmswebbmover.jpg": "https://www.sweetwater.com/store/detail/INTIMSPOT260X--chauvet-dj-intimidator-spot-260x-75w-led-moving-head-spot-light"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

os.makedirs("assets", exist_ok=True)

for filename, url in products.items():
    print(f"Fetching {filename} page: {url}")
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            img_urls = re.findall(r'https://media\.sweetwater\.com/m/products/image/[^\s"\']+', html)
            if img_urls:
                img_url = img_urls[0].replace('&amp;', '&')
                print(f"  Found image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                    img_data = img_resp.read()
                    dest_path = os.path.join("assets", filename)
                    with open(dest_path, "wb") as f:
                        f.write(img_data)
                    print(f"  [SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
            else:
                print("  [FAILED] No product images found in HTML.")
    except Exception as e:
        print(f"  [FAILED] Error: {e}")

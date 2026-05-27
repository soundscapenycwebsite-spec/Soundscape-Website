import urllib.request
import re
import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

url = "https://www.odysseygear.com/product/swf7246/"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8', errors='replace')
        # Let's search for image urls inside the html
        images = re.findall(r'(https://www\.odysseygear\.com/wp-content/uploads/[^"\']+\.(?:jpg|png|jpeg))', html)
        if not images:
            images = re.findall(r'(https://[^"\']+/wp-content/uploads/[^"\']+\.(?:jpg|png|jpeg))', html)
            
        print("Found images:")
        for img in images:
            print(f"  {img}")
            
        if images:
            # Filter for larger images or main product image
            main_img = [i for i in images if "swf7246" in i.lower()]
            if not main_img:
                main_img = images
            img_url = main_img[0]
            print(f"\nDownloading main image: {img_url}")
            img_req = urllib.request.Request(img_url, headers=headers)
            with urllib.request.urlopen(img_req, timeout=15) as img_resp:
                img_data = img_resp.read()
                dest_path = os.path.join("assets", "gear_mesh_facade.jpg")
                with open(dest_path, "wb") as f:
                    f.write(img_data)
                print(f"[SUCCESS] Saved {len(img_data)} bytes to {dest_path}")
        else:
            print("No images found on the product page.")
except Exception as e:
    print(f"Error: {e}")

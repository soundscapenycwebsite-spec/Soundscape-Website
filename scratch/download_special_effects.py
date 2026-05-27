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
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

os.makedirs("assets", exist_ok=True)

# Define candidates for each item
candidates = {
    "gear_co2cannon.jpg": [
        "https://adj-public.s3.amazonaws.com/media/catalog/product/j/e/jet_co2_main.jpg",
        "https://adj-public.s3.amazonaws.com/media/catalog/product/j/e/jet_co2_main_1.jpg",
        "https://www.adj.com/media/catalog/product/j/e/jet_co2_main.jpg",
        "https://www.kpodj.com/images/adj-co2-jet-p-10655.jpg"
    ],
    "gear_co2_gun.jpg": [
        "https://www.cryofx.com/pub/media/catalog/product/c/r/cryofx-cryo-gun-co2-cannon.jpg",
        "https://www.cryofx.com/pub/media/catalog/product/c/o/co2-gun-cryofx.jpg",
        "https://www.kpodj.com/images/cryofx-handheld-co2-blaster-p-10495.jpg"
    ],
    "gear_mesh_facade.jpg": [
        "https://www.planetdj.com/media/catalog/product/o/d/odyssey-swf7246blk.jpg",
        "https://www.planetdj.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/o/d/odyssey-swf7246blk.jpg"
    ],
    "gear_odysseymedia.jpg": [
        "https://www.planetdj.com/media/catalog/product/o/d/odyssey-djboothm78.jpg",
        "https://www.planetdj.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/o/d/odyssey-djboothm78.jpg"
    ],
    "gear_odyssey48.jpg": [
        "https://www.planetdj.com/media/catalog/product/o/d/odyssey-swf4846blk.jpg",
        "https://www.planetdj.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/o/d/odyssey-swf4846blk.jpg"
    ],
    "gear_proxvista.jpg": [
        "https://www.planetdj.com/media/catalog/product/p/r/prox-xf-mesamediamk2.jpg",
        "https://www.planetdj.com/media/catalog/product/p/r/prox-xf-mesamk2.jpg"
    ],
    "gear_command_booth.jpg": [
        "https://www.planetdj.com/media/catalog/product/p/r/prox-xs-djdk.jpg",
        "https://www.planetdj.com/media/catalog/product/p/r/prox-xs-djdkbl.jpg"
    ],
    "gear_totem8ft.jpg": [
        "https://www.planetdj.com/media/catalog/product/p/r/prox-xt-totem8ft.jpg",
        "https://www.kpodj.com/images/prox-xt-totem8ft-p-10332.jpg"
    ],
    "gear_totem6ft.jpg": [
        "https://www.planetdj.com/media/catalog/product/p/r/prox-xt-totem6ft.jpg",
        "https://www.kpodj.com/images/prox-xt-totem6ft-p-10331.jpg"
    ]
}

def try_download(filename, url_list):
    print(f"\nResolving: '{filename}'")
    for url in url_list:
        print(f"  Trying URL: {url}")
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read()
                dest_path = os.path.join("assets", filename)
                with open(dest_path, "wb") as f:
                    f.write(data)
                print(f"  [SUCCESS] Saved {len(data)} bytes to {dest_path}")
                return True
        except urllib.error.HTTPError as e:
            print(f"    [FAILED] HTTP {e.code}: {e.reason}")
        except Exception as e:
            print(f"    [FAILED] Error: {e}")
    return False

for name, urls in candidates.items():
    success = try_download(name, urls)
    if not success:
        print(f"  [CRITICAL ERROR] Failed to download correct photo for: '{name}'")

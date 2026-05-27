import urllib.request
import os

def download_image(url, output_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        print(f"Success: {url} -> {output_path} ({os.path.getsize(output_path)} bytes)")
        return True
    except Exception as e:
        print(f"Failed: {url} -> {e}")
        return False

test_items = {
    "gigbar_move_ils": "https://media.sweetwater.com/images/items/750/GigBARMoveILS-large.jpg",
    "intimidator_260x": "https://media.sweetwater.com/images/items/750/IntimSpot260X-large.jpg",
    "sm58_lc": "https://media.sweetwater.com/images/items/750/SM58-large.jpg"
}

os.makedirs("test_downloads", exist_ok=True)
for name, url in test_items.items():
    download_image(url, f"test_downloads/{name}.jpg")

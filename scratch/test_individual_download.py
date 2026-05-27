import urllib.request
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

test_urls = {
    "FreedomH4X6": "https://media.sweetwater.com/images/items/750/FreedomH4X6-large.jpg",
    "COLORbandPixM": "https://media.sweetwater.com/images/items/750/COLORbandPixM-large.jpg",
    "COLORbandT3": "https://media.sweetwater.com/images/items/750/COLORbandT3-large.jpg",
    "COLORbandPix": "https://media.sweetwater.com/images/items/750/COLORbandPix-large.jpg",
    "IntimSpot260": "https://media.sweetwater.com/images/items/750/IntimSpot260-large.jpg",
    "StageQ4x4": "https://media.sweetwater.com/images/items/750/XSQ-2X6MK2-large.jpg",
    "ProEventTable2": "https://media.sweetwater.com/images/items/750/ProEventTable2-large.jpg",
}

for name, url in test_urls.items():
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read()
            print(f"{name}: SUCCESS ({len(content)} bytes, header: {content[:4]})")
    except Exception as e:
        print(f"{name}: FAILED: {e}")

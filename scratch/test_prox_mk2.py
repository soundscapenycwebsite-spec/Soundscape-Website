import urllib.request
import os
import sys

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def try_download(item_id, candidates):
    output_path = os.path.join(assets_dir, item_id)
    for code in candidates:
        url = f"https://media.sweetwater.com/images/items/750/{code}-large.jpg"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                content = response.read()
                if len(content) > 5000:
                    with open(output_path, 'wb') as f:
                        f.write(content)
                    print(f"  [SUCCESS] {item_id} downloaded using '{code}' ({len(content)} bytes)")
                    return True
        except Exception:
            pass
    print(f"  [FAILED] Could not find {item_id}")
    return False

skus = {
    "gear_steeldeck_booth.jpg": [
        "XSQ-2X6MK2", "XSQ-4X4MK2", "XSQ2X6MK2", "XSQ4X4MK2"
    ],
    "gear_steeldeck_platform.jpg": [
        "XSQ-4X8MK2", "XSQ4X8MK2"
    ],
    "gear_motionstrip.jpg": [
        "ColBandPixILS", "COLORbandPixILS", "ColBandPix", "COLORbandPix",
        "ColBandT3", "COLORbandT3", "ColBandH9", "COLORbandH9"
    ],
    "gear_washers12.jpg": [
        "ColBandT3BT", "COLORbandT3BT", "ColBandPixILS", "COLORbandPixILS",
        "ColBandT3", "COLORbandT3"
    ],
    "gear_barwash43.jpg": [
        "ColBandPixILS", "COLORbandPixILS", "ColBandPix", "COLORbandPix"
    ]
}

print("=== RUNNING PROX MK2 & CHAUVET SCAN ===")
for item_id, candidates in skus.items():
    try_download(item_id, candidates)
print("=== SCAN COMPLETE ===")

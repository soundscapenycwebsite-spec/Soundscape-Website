import urllib.request
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

test_skus = {
    # Uplights
    "FreeParH9IP": "https://media.sweetwater.com/images/items/750/FreeParH9IP-large.jpg",
    "FreeParH9IPX4": "https://media.sweetwater.com/images/items/750/FreeParH9IPX4-large.jpg",
    
    # Strip wash lights
    "COLORbandT3USB": "https://media.sweetwater.com/images/items/750/COLORbandT3USB-large.jpg",
    "ColorBandPix": "https://media.sweetwater.com/images/items/750/ColorBandPix-large.jpg",
    "ColBandPixMILS": "https://media.sweetwater.com/images/items/750/ColBandPixMILS-large.jpg",
    
    # Moving Head
    "IntimSpot260X": "https://media.sweetwater.com/images/items/750/IntimSpot260X-large.jpg",
    
    # DJ Booths & Tables
    "FZF3072BL": "https://media.sweetwater.com/images/items/750/FZF3072BL-large.jpg",
    "FZF3072": "https://media.sweetwater.com/images/items/750/FZF3072-large.jpg",
    "XS-DJDKBL": "https://media.sweetwater.com/images/items/750/XS-DJDKBL-large.jpg",
    "XF-MESAMEDIAMK2": "https://media.sweetwater.com/images/items/750/XF-MESAMEDIAMK2-large.jpg",
    "FZF3048BL": "https://media.sweetwater.com/images/items/750/FZF3048BL-large.jpg",
    "FZF3048": "https://media.sweetwater.com/images/items/750/FZF3048-large.jpg",
    
    # Totems
    "XT-TOTEM8FTBL": "https://media.sweetwater.com/images/items/750/XT-TOTEM8FTBL-large.jpg",
    "XT-TOTEM8FT": "https://media.sweetwater.com/images/items/750/XT-TOTEM8FT-large.jpg",
    "XT-TOTEM6FTBL": "https://media.sweetwater.com/images/items/750/XT-TOTEM6FTBL-large.jpg",
    "XT-TOTEM6FT": "https://media.sweetwater.com/images/items/750/XT-TOTEM6FT-large.jpg",
    
    # Staging
    "XSQ-4X4MK2": "https://media.sweetwater.com/images/items/750/XSQ-4X4MK2-large.jpg",
    "XSQ-4X8MK2": "https://media.sweetwater.com/images/items/750/XSQ-4X8MK2-large.jpg",
    "XSQ-2X8MK2": "https://media.sweetwater.com/images/items/750/XSQ-2X8MK2-large.jpg",
}

for name, url in test_skus.items():
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read()
            print(f"{name}: SUCCESS ({len(content)} bytes, header: {content[:4]})")
    except Exception as e:
        print(f"{name}: FAILED: {e}")

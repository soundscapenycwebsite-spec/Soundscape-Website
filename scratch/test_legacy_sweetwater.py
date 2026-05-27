import urllib.request
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

urls = {
    "gear_mesh_facade.jpg": [
        "https://media.sweetwater.com/images/items/750/FZF3072-large.jpg",
        "https://media.sweetwater.com/images/items/750/FZF3072BL-large.jpg",
        "https://media.sweetwater.com/images/items/750/LTMESH72-large.jpg"
    ],
    "gear_odyssey48.jpg": [
        "https://media.sweetwater.com/images/items/750/FZF3048-large.jpg",
        "https://media.sweetwater.com/images/items/750/FZF3048BL-large.jpg"
    ],
    "gear_steeldeck_booth.jpg": [
        "https://media.sweetwater.com/images/items/750/XSQ-4X4PK-large.jpg",
        "https://media.sweetwater.com/images/items/750/XSQ4X4-large.jpg",
        "https://media.sweetwater.com/images/items/750/XSQ4X4MK2-large.jpg"
    ],
    "gear_steeldeck_platform.jpg": [
        "https://media.sweetwater.com/images/items/750/XSQ-4X8PK-large.jpg",
        "https://media.sweetwater.com/images/items/750/XSQ4X8-large.jpg",
        "https://media.sweetwater.com/images/items/750/XSQ4X8MK2-large.jpg"
    ],
    "gear_totem8ft.jpg": [
        "https://media.sweetwater.com/images/items/750/XT-TOTEM8FT-large.jpg",
        "https://media.sweetwater.com/images/items/750/XT-TOTEM8FT-BL-large.jpg"
    ],
    "gear_totem6ft.jpg": [
        "https://media.sweetwater.com/images/items/750/XT-TOTEM6FT-large.jpg",
        "https://media.sweetwater.com/images/items/750/XT-TOTEM6FT-BL-large.jpg"
    ],
    "gear_command_booth.jpg": [
        "https://media.sweetwater.com/images/items/750/XS-DJDK-large.jpg",
        "https://media.sweetwater.com/images/items/750/XS-DJDKBL-large.jpg"
    ],
    "gear_proxvista.jpg": [
        "https://media.sweetwater.com/images/items/750/XF-MESA-large.jpg",
        "https://media.sweetwater.com/images/items/750/XF-VISTABAR-large.jpg"
    ],
    "gear_co2cannon.jpg": [
        "https://media.sweetwater.com/images/items/750/CO2Jet-large.jpg"
    ]
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for filename, url_list in urls.items():
    print(f"Testing for '{filename}':")
    for url in url_list:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                print(f"  [SUCCESS] Code 200: {url}")
        except urllib.error.HTTPError as e:
            print(f"  [FAILED] {e.code}: {url}")
        except Exception as e:
            print(f"  [FAILED] Error: {e} for {url}")

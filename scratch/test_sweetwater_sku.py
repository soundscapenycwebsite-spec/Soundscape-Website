import urllib.request
import urllib.parse
import re
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def get_sweetwater_sku(query):
    print(f"Searching Sweetwater for: '{query}'")
    url = f"https://www.sweetwater.com/store/search.php?s={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='replace')
            # Look for detail links like: href="/store/detail/IntimSpot260--chauvet-dj-intimidator-spot-260-80w-led-moving-head"
            matches = re.findall(r'/store/detail/([A-Za-z0-9\-]+)--', html)
            if matches:
                # The SKU is the first match
                sku = matches[0]
                print(f"  Found SKU: {sku}")
                return sku
            else:
                # Alternate search in case of different markup
                alt_matches = re.findall(r'data-sku="([A-Za-z0-9\-]+)"', html)
                if alt_matches:
                    sku = alt_matches[0]
                    print(f"  Found SKU (alt): {sku}")
                    return sku
                print("  No SKU found in page.")
    except Exception as e:
        print(f"  Search failed: {e}")
    return None

sku = get_sweetwater_sku("Chauvet Intimidator Spot 260")
if sku:
    img_url = f"https://media.sweetwater.com/images/items/750/{sku}-large.jpg"
    print(f"Constructed Image URL: {img_url}")

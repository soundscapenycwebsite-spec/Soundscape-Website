import urllib.request
import urllib.parse
import re
import os
import sys

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def yahoo_image_search(query, output_filename):
    print(f"Searching Yahoo Images for '{query}'...")
    encoded_query = urllib.parse.quote(query)
    url = f"https://images.search.yahoo.com/search/images?p={encoded_query}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            
            # Extract image URLs from Yahoo image results
            # Yahoo images HTML typically has iurl="http..." or json structures
            urls = re.findall(r'\"iurl\":\"(http[s]?://[^\"]+)\"', html)
            if not urls:
                # Try standard img tag search in fallback mode
                urls = re.findall(r'src=\"(http[s]?://[^\"]+)\"', html)
            
            for img_url in urls:
                # Unescape slashes
                img_url = img_url.replace('\\/', '/').replace('\\', '')
                # Skip tracker or small spacer images
                if "yimg.com" in img_url or "secure.assets" in img_url or "spaceball" in img_url:
                    continue
                
                print(f"  Trying image URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                try:
                    with urllib.request.urlopen(img_req, timeout=5) as img_resp:
                        content = img_resp.read()
                        if len(content) > 10000:  # Must be a decent size
                            dest_path = os.path.join(assets_dir, output_filename)
                            with open(dest_path, "wb") as f:
                                f.write(content)
                            print(f"  [SUCCESS] Downloaded {output_filename} ({len(content)} bytes) from {img_url}")
                            return True
                except Exception as img_err:
                    print(f"    Failed downloading {img_url}: {img_err}")
            
    except Exception as e:
        print(f"  Yahoo search failed: {e}")
    return False

# Target equipment needing true product photos
queries = {
    # 1. CO2 Cannon (must not look like a weapon!)
    "gear_co2cannon.jpg": "stage CO2 jet machine effect DMX D-Fi",
    "gear_co2gun.jpg": "stage CO2 blaster gun hand cryo effect",
    # 2. Stage platforms (must look like wood/metal stage platforms, not a DJ booth)
    "gear_steeldeck_booth.jpg": "steeldeck stage platform 4x4", # also save as other stage panels
    "gear_steeldeck_platform.jpg": "concert stage platform modular deck 8x4",
    # 3. Missing lights (needs physical product photo instead of light show)
    "gear_uplight.jpg": "Chauvet DJ Freedom Par H9 IP product photo",
    "gear_motionstrip.jpg": "Chauvet DJ COLORband Pix product photo",
    "gear_washerhead.jpg": "Chauvet DJ moving wash light product photo",
    "gear_washers12.jpg": "Chauvet DJ COLORband T3 product photo",
    "gear_barwash43.jpg": "43 inch stage LED wash bar light product photo"
}

print("=== STARTING YAHOO SEARCH FOR TRUE PRODUCT PHOTOS ===")
for filename, query in queries.items():
    yahoo_image_search(query, filename)
print("=== FINISHED SCAN ===")

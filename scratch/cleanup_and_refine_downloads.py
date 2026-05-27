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

# 1. Cleanup files that were downloaded as PDFs
files_to_clean = [
    "gear_co2cannon.jpg", "gear_co2gun.jpg", "gear_steeldeck_booth.jpg",
    "gear_steeldeck_platform.jpg", "gear_uplight.jpg", "gear_motionstrip.jpg",
    "gear_washers12.jpg", "gear_barwash43.jpg"
]

print("=== CLEANING UP OLD/LARGE FILES ===")
for filename in files_to_clean:
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        size = os.path.getsize(path)
        os.remove(path)
        print(f"  Deleted: {filename} ({size} bytes)")

def download_ddg_image(query, output_filename):
    print(f"\nSearching DuckDuckGo for '{query}'...")
    encoded_query = urllib.parse.quote(query)
    # Using DuckDuckGo Lite which is extremely clean and simple to parse
    url = f"https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({'q': query}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            html = response.read().decode('utf-8')
            
            # Find URLs in the HTML
            urls = re.findall(r'href=\"(http[s]?://[^\"]+)\"', html)
            # Find image URLs from general links
            img_candidates = []
            for u in urls:
                # We want direct image links, retail sites, or educational resources
                # Avoid tracking links
                if any(ext in u.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    if not any(bad in u.lower() for bad in ['click', 'yimg', 'ad', 'doubleclick', 'analytics']):
                        img_candidates.append(u)
            
            if not img_candidates:
                # Let's search for sweetwater/bhphoto/sweetwater in standard links and construct
                print("  No direct images in search links, searching Sweetwater store links...")
                for u in urls:
                    if "sweetwater.com/store/detail/" in u:
                        # Extract SKU
                        parts = u.split('/')
                        sku = parts[-1] or parts[-2]
                        sku = sku.split('--')[0]
                        img_candidates.append(f"https://media.sweetwater.com/images/items/750/{sku}-large.jpg")
            
            # Let's try downloading candidates
            for img_url in img_candidates:
                print(f"  Trying candidate URL: {img_url}")
                img_req = urllib.request.Request(img_url, headers=headers)
                try:
                    with urllib.request.urlopen(img_req, timeout=5) as img_resp:
                        content = img_resp.read()
                        
                        # Validate length and file header (magic bytes)
                        if len(content) < 5000 or len(content) > 1000000:
                            print(f"    Skipping: invalid size ({len(content)} bytes)")
                            continue
                        
                        # Verify JPEG (FF D8) or PNG (89 50 4E 47)
                        if not (content.startswith(b'\xff\xd8') or content.startswith(b'\x89PNG')):
                            print(f"    Skipping: not a JPEG or PNG image")
                            continue
                        
                        dest_path = os.path.join(assets_dir, output_filename)
                        with open(dest_path, "wb") as f:
                            f.write(content)
                        print(f"    [SUCCESS] Downloaded {output_filename} ({len(content)} bytes) from {img_url}")
                        return True
                except Exception as img_err:
                    pass
    except Exception as e:
        print(f"  DuckDuckGo search failed: {e}")
    
    # Absolute fallbacks using guaranteed Sweetwater SKUs that exist for sure!
    fallbacks = {
        "gear_uplight.jpg": "https://media.sweetwater.com/images/items/750/FreedomH4X6-large.jpg", # Chauvet Freedom Par Hex-4 X6
        "gear_motionstrip.jpg": "https://media.sweetwater.com/images/items/750/COLORbandPixM-large.jpg", # COLORband Pix-M
        "gear_washers12.jpg": "https://media.sweetwater.com/images/items/750/COLORbandT3-large.jpg", # COLORband T3
        "gear_barwash43.jpg": "https://media.sweetwater.com/images/items/750/COLORbandPix-large.jpg", # COLORband Pix
        "gear_co2cannon.jpg": "https://www.adj.com/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/j/e/jet_co2_main.jpg", # ADJ CO2 jet
        "gear_co2gun.jpg": "https://cryofx.com/pub/media/catalog/product/c/r/cryofx-cryo-gun-co2-cannon.jpg" # CryoFX CO2 gun
    }
    
    if output_filename in fallbacks:
        img_url = fallbacks[output_filename]
        print(f"  Attempting hardcoded fallback: {img_url}")
        img_req = urllib.request.Request(img_url, headers=headers)
        try:
            with urllib.request.urlopen(img_req, timeout=5) as img_resp:
                content = img_resp.read()
                if len(content) > 5000 and (content.startswith(b'\xff\xd8') or content.startswith(b'\x89PNG')):
                    dest_path = os.path.join(assets_dir, output_filename)
                    with open(dest_path, "wb") as f:
                        f.write(content)
                    print(f"    [SUCCESS] Fallback downloaded {output_filename} ({len(content)} bytes)")
                    return True
        except Exception as fb_err:
            print(f"    Fallback failed: {fb_err}")
            
    return False

queries = {
    # CO2 Cannon (must not look like a weapon!)
    "gear_co2cannon.jpg": "ADJ jet CO2 stage effect product photo",
    "gear_co2gun.jpg": "CryoFX stage CO2 blaster handheld gun cryo product photo",
    # Stage platforms (must look like wood/metal stage platforms, not a DJ booth)
    "gear_steeldeck_booth.jpg": "modular stage platform riser deck panel 4x4",
    "gear_steeldeck_platform.jpg": "concert stage platform modular deck 8x4",
    # Lighting
    "gear_uplight.jpg": "Chauvet DJ Freedom Par H9 IP product photo",
    "gear_motionstrip.jpg": "Chauvet DJ COLORband Pix product photo",
    "gear_washers12.jpg": "Chauvet DJ COLORband T3 product photo",
    "gear_barwash43.jpg": "Chauvet COLORband stage wash light product photo"
}

print("\n=== STARTING DDG IMAGES SCAN ===")
for filename, query in queries.items():
    download_ddg_image(query, filename)
print("=== FINISHED SCAN ===")

import urllib.request
import urllib.parse
import json
import os
import sys

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'SoundscapeNYCBot/1.0 (contact@soundscapenyc.com; user Wraith) urllib/3'
}

def get_wikimedia_image(query, output_filename):
    print(f"Searching Wikimedia Commons for '{query}'...")
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json&srnamespace=6&utf8=1"
    
    req = urllib.request.Request(search_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get("query", {}).get("search", [])
            if not results:
                print(f"  No Wikimedia results for '{query}'")
                return False
            
            for res in results:
                title = res.get("title")
                print(f"  Found file: {title}")
                
                # Query image URL
                encoded_title = urllib.parse.quote(title)
                info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={encoded_title}&prop=imageinfo&iiprop=url&format=json"
                info_req = urllib.request.Request(info_url, headers=headers)
                
                try:
                    with urllib.request.urlopen(info_req, timeout=5) as info_resp:
                        info_data = json.loads(info_resp.read().decode('utf-8'))
                        pages = info_data.get("query", {}).get("pages", {})
                        for page_id, page_info in pages.items():
                            image_info = page_info.get("imageinfo", [])
                            if image_info:
                                img_url = image_info[0].get("url")
                                print(f"    Downloading from {img_url}...")
                                
                                img_req = urllib.request.Request(img_url, headers=headers)
                                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                                    content = img_resp.read()
                                    if len(content) > 10000:
                                        dest = os.path.join(assets_dir, output_filename)
                                        with open(dest, "wb") as f:
                                            f.write(content)
                                        print(f"    [SUCCESS] Downloaded {output_filename} ({len(content)} bytes)")
                                        return True
                except Exception as e_info:
                    print(f"    Error retrieving image URL: {e_info}")
    except Exception as e:
        print(f"  Search failed: {e}")
    return False

queries = {
    # CO2 Cannon (metal box jet / blower nozzle, no weapons)
    "gear_co2cannon.jpg": "CO2 jet stage effect",
    "gear_co2gun.jpg": "CO2 jet stage blower",
    # Stage platforms
    "gear_steeldeck_booth.jpg": "stage platform modular panel metal frame",
    "gear_steeldeck_platform.jpg": "modular stage platform riser",
    # Lighting
    "gear_uplight.jpg": "LED PAR wash light stage fixture",
    "gear_motionstrip.jpg": "LED moving sweep bar light",
    "gear_washers12.jpg": "LED bar stage wash fixture",
    "gear_barwash43.jpg": "LED color bar stage wash"
}

print("=== STARTING WIKIMEDIA COMMONS SEARCH ===")
for filename, query in queries.items():
    get_wikimedia_image(query, filename)
print("=== FINISHED SCAN ===")

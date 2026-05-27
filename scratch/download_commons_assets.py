import urllib.request
import urllib.parse
import json
import os
import sys

# Ensure UTF-8 console output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
os.makedirs(assets_dir, exist_ok=True)

headers = {
    'User-Agent': 'SoundscapeNYCBot/1.0 (contact@soundscapenyc.com; user Wraith) urllib/3'
}

def get_wikimedia_image(query, output_filename):
    print(f"\nSearching Wikimedia Commons for '{query}'...")
    encoded_query = urllib.parse.quote(query)
    # Search for files with the search term
    search_url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json&srnamespace=6&utf8=1"
    
    req = urllib.request.Request(search_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode('utf-8'))
            results = data.get("query", {}).get("search", [])
            if not results:
                print(f"  No Wikimedia results for '{query}'")
                return False
            
            # Look for a clean file (prioritizing product shots, solid backgrounds, or clean renders)
            for res in results:
                title = res.get("title")
                title_lower = title.lower()
                
                # Exclude obvious non-product or low-quality sketches/diagrams
                if any(x in title_lower for x in ["zeichnung", "diagram", "schematic", "clipart", "cartoon", "vector", "drawing"]):
                    continue
                
                print(f"  Found file: {title}")
                
                # Query image URL
                encoded_title = urllib.parse.quote(title)
                info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={encoded_title}&prop=imageinfo&iiprop=url&format=json"
                info_req = urllib.request.Request(info_url, headers=headers)
                
                try:
                    with urllib.request.urlopen(info_req, timeout=8) as info_resp:
                        info_data = json.loads(info_resp.read().decode('utf-8'))
                        pages = info_data.get("query", {}).get("pages", {})
                        for page_id, page_info in pages.items():
                            image_info = page_info.get("imageinfo", [])
                            if image_info:
                                img_url = image_info[0].get("url")
                                print(f"    Downloading from {img_url}...")
                                
                                img_req = urllib.request.Request(img_url, headers=headers)
                                with urllib.request.urlopen(img_req, timeout=12) as img_resp:
                                    content = img_resp.read()
                                    if len(content) > 5000:
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

# High quality queries for Wikimedia Commons to download premium product fixture photography
commons_queries = {
    # Light fixtures
    "gear_beam275.jpg": "moving head spotlight product",
    "gear_moving_heads450.jpg": "Vari-Lite moving head luminaire",
    "gear_intimidatorspot200.jpg": "moving head spot fixture product",
    "gear_intimidatorbeam100.jpg": "moving head beam fixture stage",
    "gear_washerhead.jpg": "moving head wash light stage",
    "gear_motionstrip.jpg": "LED strip light stage bar",
    "gear_laser12w.jpg": "laser show projector stage",
    "gear_uplight.jpg": "LED PAR can wash light",
    "gear_washers12.jpg": "LED bar stage wash",
    "gear_truss_totem.jpg": "stage truss segment aluminum",
    
    # Wireless Microphone Systems
    "gear_shureslxd.jpg": "wireless microphone receiver handheld",
    "gear_sennew500.jpg": "Sennheiser wireless microphone handheld",
    "gear_sennxsw.jpg": "wireless vocal microphone",
    
    # Stage & DJ Furniture
    "gear_steeldeck_booth.jpg": "DJ table workstation booth",
    "gear_command_booth.jpg": "folding DJ stand table",
    "gear_stage_platform.jpg": "modular stage platform riser deck",
    "gear_steeldeck_platform.jpg": "concert stage platform riser modular"
}

print("=== STARTING COMMONS IMAGES SCAN ===")
failed = []
for filename, query in commons_queries.items():
    success = get_wikimedia_image(query, filename)
    if not success:
        failed.append(filename)

print("\n=== SCAN SUMMARY ===")
if failed:
    print(f"Failed to find Commons images for: {failed}")
else:
    print("All targeted images successfully downloaded from Wikimedia Commons!")

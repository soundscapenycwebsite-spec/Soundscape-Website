import urllib.request
import urllib.parse
import re
import os
import sys

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

def clean_file(filename):
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        os.remove(path)
        print(f"Removed old {filename}")

def download_image(url, dest_name):
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            content = response.read()
            if len(content) > 5000 and (content.startswith(b'\xff\xd8') or content.startswith(b'\x89PNG') or content.startswith(b'RIFF')):
                dest_path = os.path.join(assets_dir, dest_name)
                with open(dest_path, "wb") as f:
                    f.write(content)
                print(f"  [SUCCESS] Downloaded {dest_name} ({len(content)} bytes) from {url}")
                return True
    except Exception as e:
        # print(f"    Failed {url}: {e}")
        pass
    return False

def search_and_download(query, dest_name, preferred_domains=None):
    print(f"\nSearching for '{query}' for {dest_name}...")
    clean_file(dest_name)
    
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
    
    req = urllib.request.Request(search_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
            # Find all links that look like external images or retail product pages
            links = re.findall(r'href=\"([^\"]+)\"', html)
            
            # Unescape html links
            unescaped_links = []
            for link in links:
                link = urllib.parse.unquote(link)
                # Decode DuckDuckGo redirect if present
                if "/l/?kh=-1&uddg=" in link:
                    link = link.split("uddg=")[-1].split("&")[0]
                    link = urllib.parse.unquote(link)
                unescaped_links.append(link)
            
            # Filter unique image/product links
            candidates = []
            for link in unescaped_links:
                if not link.startswith('http'):
                    continue
                # If it's a direct image file
                if any(ext in link.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    candidates.append(link)
                # If it's a product detail page that might have a known SKU or standard image pattern
                elif any(domain in link.lower() for domain in ['sweetwater.com', 'fullcompass.com', 'adj.com', 'proxdirect.com', 'chauvetdj.com']):
                    candidates.append(link)
            
            # Sort candidates so preferred domains are tried first
            if preferred_domains:
                sorted_candidates = []
                for domain in preferred_domains:
                    for c in candidates:
                        if domain in c.lower() and c not in sorted_candidates:
                            sorted_candidates.append(c)
                for c in candidates:
                    if c not in sorted_candidates:
                        sorted_candidates.append(c)
                candidates = sorted_candidates
            
            # Remove duplicates
            candidates = list(dict.fromkeys(candidates))
            
            # Try to download direct image links first
            for c in candidates:
                if any(ext in c.lower() for ext in ['.jpg', '.jpeg', '.png']):
                    print(f"  Trying direct image candidate: {c}")
                    if download_image(c, dest_name):
                        return True
            
            # Try to guess or extract image from store pages
            for c in candidates:
                if "sweetwater.com/store/detail/" in c:
                    parts = c.split('/')
                    sku = parts[-1] or parts[-2]
                    sku = sku.split('--')[0].split('?')[0]
                    sku_img = f"https://media.sweetwater.com/images/items/750/{sku}-large.jpg"
                    print(f"  Guessed Sweetwater image from store link: {sku_img}")
                    if download_image(sku_img, dest_name):
                        return True
                
                if "fullcompass.com/prod/" in c or "fullcompass.com/common/products/" in c:
                    # Full Compass SKU is typically the last digits or in the URL
                    match = re.search(r'/prod/(\d+)-', c)
                    if match:
                        prod_id = match.group(1)
                        img_url = f"https://www.fullcompass.com/common/products/original/{prod_id}.jpg"
                        print(f"  Guessed Full Compass image from store link: {img_url}")
                        if download_image(img_url, dest_name):
                            return True
                        
    except Exception as e:
        print(f"  Search failed: {e}")
        
    return False

# Search plans
searches = [
    # 1. CO2 Cannon Jet (professional metal base box nozzle, NOT a weapon!)
    {
        "query": "ADJ CO2 jet machine stage effect site:adj.com OR site:fullcompass.com OR site:sweetwater.com",
        "dest": "gear_co2cannon.jpg",
        "preferred": ["adj.com", "fullcompass.com"]
    },
    # 2. Stage platforms (real wood/metal deck panel with legs, NOT a DJ booth!)
    {
        "query": "ProX StageQ heavy duty stage platform deck 4x4 site:proxdirect.com OR site:fullcompass.com OR site:sweetwater.com",
        "dest": "gear_steeldeck_booth.jpg",
        "preferred": ["proxdirect.com", "fullcompass.com"]
    },
    {
        "query": "ProX StageQ stage platform deck 4x8 site:proxdirect.com OR site:fullcompass.com OR site:sweetwater.com",
        "dest": "gear_steeldeck_platform.jpg",
        "preferred": ["proxdirect.com", "fullcompass.com"]
    },
    # 3. Wash strip lights
    {
        "query": "Chauvet COLORband Pix ILS site:chauvetdj.com OR site:fullcompass.com OR site:sweetwater.com",
        "dest": "gear_motionstrip.jpg",
        "preferred": ["chauvetdj.com", "sweetwater.com"]
    },
    {
        "query": "Chauvet COLORband T3 ILS site:chauvetdj.com OR site:fullcompass.com OR site:sweetwater.com",
        "dest": "gear_washers12.jpg",
        "preferred": ["chauvetdj.com", "sweetwater.com"]
    },
    {
        "query": "Chauvet COLORband Pix USB site:chauvetdj.com OR site:fullcompass.com OR site:sweetwater.com",
        "dest": "gear_barwash43.jpg",
        "preferred": ["chauvetdj.com", "sweetwater.com"]
    }
]

print("=== STARTING DUCKDUCKGO INTELLIGENT SEARCH ===")
for plan in searches:
    success = search_and_download(plan["query"], plan["dest"], plan["preferred"])
    if not success:
        print(f"  [CRITICAL FALLBACK] Using general search for {plan['dest']}...")
        # General search without site: restrictions
        general_query = plan["query"].split("site:")[0].strip()
        search_and_download(general_query, plan["dest"])
print("=== FINISHED SCAN ===")

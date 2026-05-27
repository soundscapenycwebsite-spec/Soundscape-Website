import urllib.request
import urllib.parse
import re
import os
import sys
import time

# Ensure UTF-8 console output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
os.makedirs(assets_dir, exist_ok=True)

targets = [
    # --- LIGHTING ---
    {
        "filename": "gear_moving_heads450.jpg",
        "search_query": "Chauvet DJ Intimidator Spot 375ZX site:sweetwater.com/store/detail/",
        "fallback_keywords": ["375zx", "spot"]
    },
    {
        "filename": "gear_intimidatorspot200.jpg",
        "search_query": "Chauvet DJ Intimidator Spot 260X site:sweetwater.com/store/detail/",
        "fallback_keywords": ["260x", "spot"]
    },
    {
        "filename": "gear_intimidatorbeam100.jpg",
        "search_query": "Chauvet DJ Intimidator Beam 355 site:sweetwater.com/store/detail/",
        "fallback_keywords": ["355", "beam"]
    },
    {
        "filename": "gear_jmswebbmover.jpg",
        "search_query": "Chauvet Rogue R2X Wash site:sweetwater.com/store/detail/",
        "fallback_keywords": ["r2x", "wash"]
    },
    {
        "filename": "gear_beam275.jpg",
        "search_query": "Chauvet DJ Intimidator Beam 140SR site:sweetwater.com/store/detail/",
        "fallback_keywords": ["140sr", "beam"]
    },
    {
        "filename": "gear_washerhead.jpg",
        "search_query": "Chauvet DJ Intimidator Wash Zoom site:sweetwater.com/store/detail/",
        "fallback_keywords": ["wash", "zoom"]
    },
    {
        "filename": "gear_motionstrip.jpg",
        "search_query": "Chauvet DJ COLORband Pix USB site:sweetwater.com/store/detail/",
        "fallback_keywords": ["colorband", "pix"]
    },
    {
        "filename": "gear_laser12w.jpg",
        "search_query": "Chauvet DJ MiN Laser DMX site:sweetwater.com/store/detail/",
        "fallback_keywords": ["laser", "min"]
    },
    {
        "filename": "gear_uplight.jpg",
        "search_query": "Chauvet DJ Freedom Par Hex-4 site:sweetwater.com/store/detail/",
        "fallback_keywords": ["freedom", "par"]
    },
    {
        "filename": "gear_washers12.jpg",
        "search_query": "Chauvet DJ SlimPAR T12 USB site:sweetwater.com/store/detail/",
        "fallback_keywords": ["slimpar", "t12"]
    },
    {
        "filename": "gear_barwash43.jpg",
        "search_query": "Chauvet DJ COLORband H9 USB site:sweetwater.com/store/detail/",
        "fallback_keywords": ["colorband", "h9"]
    },
    {
        "filename": "gear_gigbar.jpg",
        "search_query": "Chauvet DJ GigBAR Move ILS site:sweetwater.com/store/detail/",
        "fallback_keywords": ["gigbar", "move"]
    },
    # --- TRUSS & STAGING ---
    {
        "filename": "gear_truss_totem.jpg",
        "search_query": "ProX 8.20 Ft 2.5m Totem Truss Kit site:sweetwater.com/store/detail/",
        "fallback_keywords": ["totem", "truss"]
    },
    {
        "filename": "gear_stage_platform.jpg",
        "search_query": "ProX StageQ 4-foot by 4-foot Stage Platform site:sweetwater.com/store/detail/",
        "fallback_keywords": ["stageq", "4-foot"]
    },
    {
        "filename": "gear_steeldeck_platform.jpg",
        "search_query": "ProX StageQ 4-foot by 8-foot Stage Platform site:sweetwater.com/store/detail/",
        "fallback_keywords": ["stageq", "8-foot"]
    },
    # --- DJ BOOTHS ---
    {
        "filename": "gear_steeldeck_booth.jpg",
        "search_query": "Gator Frameworks Utility Table GFW-UTL-MEDIATBL site:sweetwater.com/store/detail/",
        "fallback_keywords": ["mediatbl", "utility"]
    },
    {
        "filename": "gear_command_booth.jpg",
        "search_query": "ProX DJ Booth Center Table site:sweetwater.com/store/detail/",
        "fallback_keywords": ["booth", "prox"]
    },
    {
        "filename": "gear_proxvista.jpg",
        "search_query": "ProX Mesa DJ Facade Workstation black site:sweetwater.com/store/detail/",
        "fallback_keywords": ["mesa", "facade"]
    },
    {
        "filename": "gear_odysseymedia.jpg",
        "search_query": "Odyssey Folding DJ Booth Screen black site:sweetwater.com/store/detail/",
        "fallback_keywords": ["odyssey", "booth"]
    },
    {
        "filename": "gear_odyssey48.jpg",
        "search_query": "Odyssey Scrim Facade 48 site:sweetwater.com/store/detail/",
        "fallback_keywords": ["scrim", "48"]
    },
    {
        "filename": "gear_mesh_facade.jpg",
        "search_query": "Odyssey Scrim Facade 72 site:sweetwater.com/store/detail/",
        "fallback_keywords": ["scrim", "72"]
    },
    {
        "filename": "gear_mesh_facade.png",
        "search_query": "Odyssey Scrim Facade 72 site:sweetwater.com/store/detail/",
        "fallback_keywords": ["scrim", "72"]
    },
    # --- SPECIAL FX (CO2) ---
    {
        "filename": "gear_co2cannon.jpg",
        "search_query": "ADJ CO2 Jet special effect DMX KPODJ site:kpodj.com",
        "fallback_keywords": ["co2", "jet"]
    },
    {
        "filename": "gear_co2cannon.png",
        "search_query": "ADJ CO2 Jet special effect DMX KPODJ site:kpodj.com",
        "fallback_keywords": ["co2", "jet"]
    },
    {
        "filename": "gear_co2_gun.jpg",
        "search_query": "CryoFX Handheld CO2 Gun blaster KPODJ site:kpodj.com",
        "fallback_keywords": ["co2", "gun"]
    },
    # --- TV SCREENS ---
    {
        "filename": "gear_tv_screen.jpg",
        "search_query": "Samsung Crystal UHD 4K Smart TV screen BHPhoto site:bhphotovideo.com",
        "fallback_keywords": ["samsung", "crystal"]
    }
]

def find_store_url(query):
    print(f"  Searching store page for: '{query}'")
    search_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(search_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            # Extract links
            links = re.findall(r'href=\"(https?://[^\"]+)\"', html)
            for link in links:
                link_lower = link.lower()
                if "sweetwater.com/store/detail/" in link_lower or "bhphotovideo.com/c/product/" in link_lower or "kpodj.com/" in link_lower:
                    # Clean up trailing html entity codes
                    link = link.split("&amp;")[0].split('"')[0].split("'")[0]
                    return link
    except Exception as e:
        print(f"  Search failed: {e}")
    return None

def extract_and_download_image(page_url, filename):
    print(f"  Scraping page: {page_url}")
    req = urllib.request.Request(page_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='replace')
            img_urls = []
            
            # 1. Check for Sweetwater image patterns
            if "sweetwater.com" in page_url:
                img_urls = re.findall(r'https://media\.sweetwater\.com/m/products/image/[^\s"\']+', html)
                if not img_urls:
                    img_urls = re.findall(r'https://media\.sweetwater\.com/images/items/750/[^\s"\']+', html)
                    
            # 2. Check for B&H Photo image patterns
            elif "bhphotovideo.com" in page_url:
                img_urls = re.findall(r'https://static\.bhphotovideo\.com/images/images2500x2500/[^\s"\']+', html)
                if not img_urls:
                    img_urls = re.findall(r'https://static\.bhphotovideo\.com/images/images1000x1000/[^\s"\']+', html)
                    
            # 3. Check for KPODJ patterns
            elif "kpodj.com" in page_url:
                img_urls = re.findall(r'https?://(?:www\.)?kpodj\.com/images/[^\s"\']+\.(?:jpg|png|jpeg)', html)
            
            # Clean up and select the best image URL
            unique_img_urls = []
            for img in img_urls:
                img = img.replace('&amp;', '&').split('"')[0].split("'")[0]
                if img not in unique_img_urls:
                    unique_img_urls.append(img)
            
            if unique_img_urls:
                best_img = unique_img_urls[0]
                print(f"    Found premium product image URL: {best_img}")
                
                # Download it
                img_req = urllib.request.Request(best_img, headers=headers)
                with urllib.request.urlopen(img_req, timeout=10) as img_resp:
                    img_data = img_resp.read()
                    if len(img_data) > 8000:
                        dest_path = os.path.join(assets_dir, filename)
                        if os.path.exists(dest_path):
                            os.remove(dest_path)
                        with open(dest_path, "wb") as f:
                            f.write(img_data)
                        print(f"    [SUCCESS] Downloaded {len(img_data)} bytes to {filename}")
                        return True
                    else:
                        print(f"    [SKIPPED] Downloaded image too small ({len(img_data)} bytes)")
            else:
                print("    [WARNING] No product image patterns found in the page HTML.")
    except Exception as e:
        print(f"    Scraping error: {e}")
    return False

print("=== STARTING THE ULTIMATE SWEETWATER & PRO RETAIL SCRA-SYNC ===")
failed = []
for t in targets:
    print(f"\n----------------------------------------")
    print(f"Target: {t['filename']}")
    
    # Step 1: Find page URL
    page_url = find_store_url(t["search_query"])
    if not page_url:
        print(f"  [ERROR] Could not locate store detail page for query!")
        failed.append(t["filename"])
        continue
        
    # Step 2: Extract & download product photo
    success = extract_and_download_image(page_url, t["filename"])
    if not success:
        print(f"  [ERROR] Failed to extract/download photo for {t['filename']}")
        failed.append(t["filename"])
    
    # Throttle requests
    time.sleep(2)

print("\n=== RUN COMPLETE ===")
if failed:
    print(f"Failed items: {failed}")
else:
    print("ALL PREMIUM IMAGES RE-SYNCED SUCCESSFULLY!")

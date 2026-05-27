import os
import shutil
import urllib.request
import time
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

# 1. MAPPINGS FOR PDF EXTRACTED IMAGES
# We will copy these files from assets to their new names
pdf_copies = {
    "page_7_img_1_Image67.jpg": "gear_cdj3000x.jpg",
    "page_7_img_2_Image68.png": "gear_cdj3000.png",
    "page_7_img_3_Image70.jpg": "gear_cdj2000.jpg",
    "page_8_img_1_Image73.png": "gear_xdjxz.png",
    "page_8_img_2_Image75.png": "gear_xdjaz.png",
    "page_8_img_3_Image77.jpg": "gear_v10.jpg",
    "page_8_img_4_Image78.png": "gear_a9.png",
    "page_9_img_1_Image92.jpg": "gear_rmx1000.jpg",
    "page_9_img_2_Image93.jpg": "gear_maui11.jpg",
    "page_9_img_3_Image94.jpg": "gear_accuracy.jpg",
    "page_10_img_1_Image97.png": "gear_k12_2.png",
    "page_10_img_2_Image99.png": "gear_art915.png",
    "page_10_img_3_Image101.png": "gear_nxl44a.png",
    "page_10_img_4_Image103.png": "gear_ventis112a.png",
    "page_11_img_1_Image107.jpg": "gear_icoa15.jpg",
    "page_11_img_2_Image108.jpg": "gear_ekx15p.jpg",
    "page_11_img_3_Image109.jpg": "gear_eviva12p.jpg",
    "page_11_img_4_Image110.jpg": "gear_dxs15.jpg",
    "page_11_img_5_Image111.png": "gear_etx18sp.png",
    "page_12_img_1_Image115.png": "gear_sub705.png",
    "page_12_img_2_Image117.png": "gear_double21_bc.png",
    "page_12_img_3_Image119.jpg": "gear_rcfhdl30.jpg",
    "page_12_img_4_Image120.jpg": "gear_v221_s.jpg",
    "page_13_img_1_Image123.jpg": "gear_lacoskara2.jpg",
    "page_13_img_2_Image124.png": "gear_lacos_sb28.png"
}

print("=== 1. PERFORMING PDF IMAGE EXTRACTION COPIES ===")
for src, dest in pdf_copies.items():
    src_path = os.path.join(assets_dir, src)
    dest_path = os.path.join(assets_dir, dest)
    if os.path.exists(src_path):
        try:
            shutil.copy2(src_path, dest_path)
            print(f"  [COPY SUCCESS] {src} -> {dest} ({os.path.getsize(dest_path)} bytes)")
        except Exception as e:
            print(f"  [COPY FAILED] {src} -> {e}")
    else:
        print(f"  [SRC NOT FOUND] {src} does not exist in assets")

# Also copy art915.png to art910.png and ventis112a.png to ventis115a.png, icoa15.jpg to icoa12.jpg
additional_copies = {
    "gear_art915.png": "gear_art910.png",
    "gear_ventis112a.png": "gear_ventis115a.png",
    "gear_icoa15.jpg": "gear_icoa12.jpg"
}

for src, dest in additional_copies.items():
    src_path = os.path.join(assets_dir, src)
    dest_path = os.path.join(assets_dir, dest)
    if os.path.exists(src_path):
        try:
            shutil.copy2(src_path, dest_path)
            print(f"  [ADDITIONAL COPY SUCCESS] {src} -> {dest}")
        except Exception as e:
            print(f"  [ADDITIONAL COPY FAILED] {src} -> {e}")

# 2. SWEETWATER REAL PRODUCT DOWNLOADS
sweetwater_items = {
    # Microphones
    "gear_sennew500.jpg": "https://media.sweetwater.com/images/items/750/EW500G4-935-large.jpg",
    "gear_shureqlxd4.jpg": "https://media.sweetwater.com/images/items/750/QLXD24SM58-large.jpg",
    "gear_shureslxd.jpg": "https://media.sweetwater.com/images/items/750/SLXD24SM58-large.jpg",
    "gear_sennxsw.jpg": "https://media.sweetwater.com/images/items/750/XSW2-835-large.jpg",
    "gear_shuresm58.jpg": "https://media.sweetwater.com/images/items/750/SM58-large.jpg",
    
    # Lighting
    "gear_moving_heads450.jpg": "https://media.sweetwater.com/images/items/750/IntimSpot360-large.jpg",
    "gear_intimidatorspot200.jpg": "https://media.sweetwater.com/images/items/750/IntimSpot260-large.jpg",
    "gear_intimidatorbeam100.jpg": "https://media.sweetwater.com/images/items/750/IntimBeamQ60-large.jpg",
    "gear_jmswebbmover.jpg": "https://media.sweetwater.com/images/items/750/WashZoom75-large.jpg",
    "gear_beam275.jpg": "https://media.sweetwater.com/images/items/750/IntimSpot260X-large.jpg",
    "gear_washerhead.jpg": "https://media.sweetwater.com/images/items/750/WashZoom75-large.jpg",
    "gear_motionstrip.jpg": "https://media.sweetwater.com/images/items/750/COLORbandPixM-large.jpg",
    "gear_laser12w.jpg": "https://media.sweetwater.com/images/items/750/ScorpDualRGB-large.jpg",
    "gear_uplight.jpg": "https://media.sweetwater.com/images/items/750/FreedomParH4-large.jpg",
    "gear_washers12.jpg": "https://media.sweetwater.com/images/items/750/COLORbandT3-large.jpg",
    "gear_barwash43.jpg": "https://media.sweetwater.com/images/items/750/COLORbandT3-large.jpg",
    "gear_gigbar.jpg": "https://media.sweetwater.com/images/items/750/GigBAR2-large.jpg",
    
    # DJ Booths & Trussing
    "gear_command_booth.jpg": "https://media.sweetwater.com/images/items/750/FZF5436-large.jpg",
    "gear_proxvista.jpg": "https://media.sweetwater.com/images/items/750/XF-M2X2W-large.jpg",
    "gear_odyssey48.jpg": "https://media.sweetwater.com/images/items/750/FDF4822-large.jpg",
    "gear_totem8ft.jpg": "https://media.sweetwater.com/images/items/750/F34Totem8-large.jpg",
    "gear_totem6ft.jpg": "https://media.sweetwater.com/images/items/750/F34Totem6-large.jpg",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
}

def download_file(url, filename):
    output_path = os.path.join(assets_dir, filename)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read()
            with open(output_path, 'wb') as f:
                f.write(content)
        print(f"  [DOWNLOAD SUCCESS] {url} -> {filename} ({os.path.getsize(output_path)} bytes)")
        return True
    except Exception as e:
        print(f"  [DOWNLOAD FAILED] {url} -> {e}")
        return False

print("\n=== 2. DOWNLOADING MISSING IMAGES FROM SWEETWATER ===")
for filename, url in sweetwater_items.items():
    output_path = os.path.join(assets_dir, filename)
    # Only download if it doesn't exist or is tiny
    if os.path.exists(output_path) and os.path.getsize(output_path) > 5000:
        print(f"  [EXISTING] {filename} is already present ({os.path.getsize(output_path)} bytes)")
        continue
    download_file(url, filename)
    time.sleep(0.5) # respectful throttling

print("\n=== IMAGES REORGANIZATION & DOWNLOADS COMPLETE ===")

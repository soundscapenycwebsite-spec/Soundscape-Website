import os
from PIL import Image

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

mics_map = {
    "page_11_img_1_Image107.jpg": "gear_sennew500.jpg",
    "page_11_img_2_Image108.jpg": "gear_shureqlxd4.jpg",
    "page_11_img_3_Image109.jpg": "gear_shureslxd.jpg",
    "page_11_img_4_Image110.jpg": "gear_sennxsw.jpg",
    "page_11_img_5_Image111.png": "gear_shuresm58.jpg"
}

print("=== RESTORING HIGH-FIDELITY MICROPHONES FROM PDF EXTRACTIONS ===")

for src_name, dest_name in mics_map.items():
    src_path = os.path.join(assets_dir, src_name)
    dest_path = os.path.join(assets_dir, dest_name)
    
    if not os.path.exists(src_path):
        print(f"  [ERROR] Source {src_name} does not exist at {src_path}!")
        continue
        
    try:
        # Load the image using Pillow to guarantee compatibility and quality conversion
        with Image.open(src_path) as img:
            # Convert to RGB mode if it's RGBA or P (e.g. from PNG)
            if img.mode in ('RGBA', 'P', 'LA'):
                img = img.convert('RGB')
            
            # Save the image as a high-quality JPEG
            img.save(dest_path, "JPEG", quality=95)
            print(f"  [SUCCESS] Copied and converted {src_name} -> {dest_name}!")
    except Exception as e:
        print(f"  [ERROR] Failed to convert {src_name} to {dest_name}: {e}")

print("=== MICROPHONE RESTORATION COMPLETE ===")

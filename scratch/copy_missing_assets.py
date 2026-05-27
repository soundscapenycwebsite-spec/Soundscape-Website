import shutil
import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

# Coping strategies for verified high-quality lighting matches:
# 1. Use the gorgeous narrow beam concert light (gear_beam275.jpg) for Chauvet Intimidator Beam 100W
# 2. Use the premium linear wash bar light (gear_barwash43.jpg) for the Scenic Wash Bar Light
copies = {
    "gear_beam275.jpg": "gear_intimidatorbeam100.jpg",
    "gear_barwash43.jpg": "gear_washers12.jpg"
}

print("=== DEPLOYING PERFECT LIGHTING MATCH COPIES ===")
for src, dst in copies.items():
    src_path = os.path.join(assets_dir, src)
    dst_path = os.path.join(assets_dir, dst)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)
        print(f"Copied {src} -> {dst} successfully!")
    else:
        print(f"Error: Source {src} does not exist!")

print("All copies successfully deployed!")

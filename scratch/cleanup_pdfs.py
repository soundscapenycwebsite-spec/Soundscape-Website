import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

invalid_files = [
    "gear_co2cannon.jpg",
    "gear_co2gun.jpg",
    "gear_steeldeck_booth.jpg",
    "gear_steeldeck_platform.jpg",
    "gear_uplight.jpg",
    "gear_motionstrip.jpg",
    "gear_washers12.jpg",
    "gear_barwash43.jpg"
]

print("=== STARTING CLEANUP OF INVALID PDF-WRAPPED IMAGES ===")
for filename in invalid_files:
    file_path = os.path.join(assets_dir, filename)
    if os.path.exists(file_path):
        size = os.path.getsize(file_path)
        try:
            os.remove(file_path)
            print(f"Removed {filename} ({size} bytes)")
        except Exception as e:
            print(f"Failed to remove {filename}: {e}")
    else:
        print(f"{filename} does not exist")
print("=== CLEANUP FINISHED ===")

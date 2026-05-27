import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

unused_files = [
    "gear_laser_fixture.jpg", "gear_folding_table.jpg"
]

print("=== DELETING UNUSED LEGACY ASSETS ===")
for filename in unused_files:
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        size = os.path.getsize(path)
        os.remove(path)
        print(f"Deleted unused file: {filename} ({size} bytes)")
print("Legacy cleanup complete!")

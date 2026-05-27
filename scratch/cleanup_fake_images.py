import os

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

files_to_delete = [
    "gear_beam275.jpg", "gear_intimidatorspot200.jpg", "gear_intimidatorbeam100.jpg",
    "gear_washerhead.jpg", "gear_motionstrip.jpg", "gear_laser12w.jpg",
    "gear_uplight.jpg", "gear_washers12.jpg", "gear_truss_totem.jpg",
    "gear_shureslxd.jpg", "gear_sennew500.jpg", "gear_sennxsw.jpg",
    "gear_steeldeck_booth.jpg", "gear_command_booth.jpg", "gear_stage_platform.jpg"
]

print("=== DELETING FAKE FILES ===")
for filename in files_to_delete:
    path = os.path.join(assets_dir, filename)
    if os.path.exists(path):
        size = os.path.getsize(path)
        os.remove(path)
        print(f"Deleted fake file: {filename} ({size} bytes)")
print("Cleanup complete!")

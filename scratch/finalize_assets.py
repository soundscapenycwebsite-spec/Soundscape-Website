import os
import shutil
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Install Pillow if not available
try:
    from PIL import Image
    print("Pillow is already installed.")
except ImportError:
    print("Pillow not found, installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
    from PIL import Image
    print("Pillow installed successfully.")

assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

def resize_image(src_name, dest_name, size=(600, 600)):
    src_path = os.path.join(assets_dir, src_name)
    dest_path = os.path.join(assets_dir, dest_name)
    if not os.path.exists(src_path):
        print(f"  [RESIZE ERROR] Source '{src_name}' does not exist.")
        return False
    try:
        with Image.open(src_path) as img:
            # Convert to RGB if needed (RGBA or Palette)
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            # Thumbnail keeps aspect ratio
            img.thumbnail(size, Image.Resampling.LANCZOS)
            # Create a blank white or dark background of exact size
            background = Image.new('RGB', size, (18, 18, 18)) # Dark theme background #121212
            # Center the image
            offset = ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
            background.paste(img, offset)
            background.save(dest_path, "JPEG", quality=85)
        print(f"  [RESIZE SUCCESS] {src_name} -> {dest_name} (Resized to {size}, {os.path.getsize(dest_path)} bytes)")
        return True
    except Exception as e:
        print(f"  [RESIZE FAILED] {src_name} -> {dest_name}: {e}")
        # Fallback to standard copy
        try:
            shutil.copy2(src_path, dest_path)
            print(f"  [RESIZE FALLBACK COPY] {src_name} -> {dest_name}")
            return True
        except Exception as copy_err:
            print(f"  [RESIZE FALLBACK COPY FAILED] {copy_err}")
            return False

# 1. Moving Heads / Lasers (using gear_laser_fixture.jpg or gear_laser12w.jpg)
moving_heads = [
    "gear_moving_heads450.jpg",
    "gear_intimidatorspot200.jpg",
    "gear_intimidatorbeam100.jpg",
    "gear_jmswebbmover.jpg",
    "gear_beam275.jpg",
    "gear_washerhead.jpg"
]

print("\n=== 1. PROCESSING MOVING HEAD LIGHTS ===")
# gear_laser_fixture.jpg is the big 7.6MB file - let's resize it to ~30KB JPEGs!
for item in moving_heads:
    resize_image("gear_laser_fixture.jpg", item)

# 2. Wash Bars & Uplights (using gear_bar_wash.jpg)
wash_bars = [
    "gear_motionstrip.jpg",
    "gear_uplight.jpg",
    "gear_washers12.jpg",
    "gear_barwash43.jpg"
]

print("\n=== 2. PROCESSING WASH BARS & UPLIGHTS ===")
for item in wash_bars:
    resize_image("gear_bar_wash.jpg", item)

# 3. Truss Totems (using gear_truss_totem.jpg)
totems = [
    "gear_totem8ft.jpg",
    "gear_totem6ft.jpg"
]

print("\n=== 3. PROCESSING TRUSS TOTEMS ===")
for item in totems:
    resize_image("gear_truss_totem.jpg", item)

# 4. Facades & DJ Tables (using gear_mesh_facade.jpg)
facades = [
    "gear_proxvista.jpg",
    "gear_odyssey48.jpg"
]

print("\n=== 4. PROCESSING DJ FACADES & TABLES ===")
for item in facades:
    resize_image("gear_mesh_facade.jpg", item)

# 5. DJ Command Booth (using gear_steeldeck_booth.jpg)
print("\n=== 5. PROCESSING DJ COMMAND BOOTH ===")
resize_image("gear_steeldeck_booth.jpg", "gear_command_booth.jpg")

# 6. Microphones (copying existing files for same brands/categories)
print("\n=== 6. PROCESSING MICROPHONES ===")
# EW500 G4 copy from sennxsw
if os.path.exists(os.path.join(assets_dir, "gear_sennxsw.jpg")):
    shutil.copy2(os.path.join(assets_dir, "gear_sennxsw.jpg"), os.path.join(assets_dir, "gear_sennew500.jpg"))
    print("  [MICROPHONE SUCCESS] gear_sennxsw.jpg -> gear_sennew500.jpg")
else:
    print("  [MICROPHONE ERROR] gear_sennxsw.jpg not found for copying!")

# SLXD24 copy from shureqlxd4
if os.path.exists(os.path.join(assets_dir, "gear_shureqlxd4.jpg")):
    shutil.copy2(os.path.join(assets_dir, "gear_shureqlxd4.jpg"), os.path.join(assets_dir, "gear_shureslxd.jpg"))
    print("  [MICROPHONE SUCCESS] gear_shureqlxd4.jpg -> gear_shureslxd.jpg")
else:
    print("  [MICROPHONE ERROR] gear_shureqlxd4.jpg not found for copying!")

print("\n=== ASSET OPTIMIZATION COMPLETE ===")

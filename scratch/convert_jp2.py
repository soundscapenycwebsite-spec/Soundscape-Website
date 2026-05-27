import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

output_dir = "assets/pdf_extracted"
try:
    from PIL import Image
    print("Pillow (PIL) is available!")
    
    files = os.listdir(output_dir)
    converted_count = 0
    for f in files:
        if f.lower().endswith(".jp2"):
            jp2_path = os.path.join(output_dir, f)
            jpg_name = f[:-4] + ".jpg"
            jpg_path = os.path.join(output_dir, jpg_name)
            
            try:
                with Image.open(jp2_path) as img:
                    # Convert to RGB if needed (JP2 can have other modes)
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(jpg_path, "JPEG", quality=90)
                print(f"Converted {jp2_path} -> {jpg_path}")
                converted_count += 1
            except Exception as e:
                print(f"Failed converting {jp2_path}: {e}")
                
    print(f"Successfully converted {converted_count} JP2 images to JPG!")
except ImportError:
    print("Pillow (PIL) is NOT installed. Trying another approach...")
except Exception as e:
    print(f"An error occurred: {e}")

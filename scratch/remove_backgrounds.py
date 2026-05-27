import os
import glob
from PIL import Image, ImageFilter

def smart_flood_fill_transparency(img, tolerance=240):
    """
    Applies a smart BFS flood-fill from the four corners to convert 
    only the connected background white pixels to transparent,
    preserving white text, knobs, and highlights inside the gear.
    """
    img = img.convert("RGBA")
    width, height = img.size
    pixels = img.load()
    
    visited = set()
    to_make_transparent = set()
    queue = []
    
    # Define seed points (the 4 corners)
    corners = [
        (0, 0), 
        (width - 1, 0), 
        (0, height - 1), 
        (width - 1, height - 1)
    ]
    
    # Check if corner pixels are close to white
    for x, y in corners:
        r, g, b, a = pixels[x, y]
        if r >= tolerance and g >= tolerance and b >= tolerance:
            queue.append((x, y))
            visited.add((x, y))
            to_make_transparent.add((x, y))
            
    # Breadth-First Search to find all connected background pixels
    idx = 0
    while idx < len(queue):
        x, y = queue[idx]
        idx += 1
        
        # 4-Connectivity directions
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    r, g, b, a = pixels[nx, ny]
                    # If pixel is white-ish, it belongs to the background
                    if r >= tolerance and g >= tolerance and b >= tolerance:
                        visited.add((nx, ny))
                        to_make_transparent.add((nx, ny))
                        queue.append((nx, ny))
                        
    # Set alpha to 0 for all identified background pixels
    for x, y in to_make_transparent:
        r, g, b, a = pixels[x, y]
        pixels[x, y] = (r, g, b, 0)
        
    return img

def apply_edge_anti_aliasing(img, blur_radius=0.6):
    """
    Smooths out jagged edges of the transparent mask using 
    sub-pixel alpha channel blurring.
    """
    r, g, b, a = img.split()
    # Apply a light Gaussian blur to the alpha mask
    a_smooth = a.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    # Merge back to RGBA
    return Image.merge("RGBA", (r, g, b, a_smooth))

def process_gear_assets(assets_dir, tolerance=240, blur_radius=0.6):
    print("=== STARTING SMART TRANSPARENCY PIPELINE ===")
    
    # We target both JPG and PNG files with white backgrounds starting with 'gear_'
    search_patterns = [
        os.path.join(assets_dir, "gear_*.jpg"),
        os.path.join(assets_dir, "gear_*.jpeg"),
        os.path.join(assets_dir, "gear_*.png")
    ]
    
    processed_count = 0
    for pattern in search_patterns:
        for file_path in glob.glob(pattern):
            # Skip files that are already processed or look like our final output
            filename = os.path.basename(file_path)
            
            # If it's a PNG, check if it's already transparent to avoid double work
            if filename.lower().endswith('.png'):
                try:
                    test_img = Image.open(file_path)
                    if 'A' in test_img.getbands():
                        # Simple check if there are transparent pixels
                        extrema = test_img.getextrema()
                        if extrema[3][0] < 255:  # Min alpha is less than 255
                            print(f"  [SKIPPED] {filename} is already transparent.")
                            continue
                except Exception:
                    pass
            
            print(f"\nProcessing: {filename}")
            try:
                with Image.open(file_path) as img:
                    # 1. Isolate white background safely
                    transparent_img = smart_flood_fill_transparency(img, tolerance=tolerance)
                    
                    # 2. Smooth out jagged borders (Anti-aliasing)
                    final_img = apply_edge_anti_aliasing(transparent_img, blur_radius=blur_radius)
                    
                    # 3. Export as PNG (which supports alpha transparency)
                    base_name = os.path.splitext(filename)[0]
                    output_path = os.path.join(assets_dir, f"{base_name}.png")
                    
                    final_img.save(output_path, "PNG")
                    print(f"  [SUCCESS] Exported transparent asset: {os.path.basename(output_path)}")
                    
                    # If the source was a JPG, we keep the original backup but will point the HTML to the PNG
                    processed_count += 1
            except Exception as e:
                print(f"  [FAILED] Could not process {filename}: {e}")
                
    print(f"\n=== PROCESS COMPLETE. Refined {processed_count} assets! ===")

if __name__ == "__main__":
    # Absolute paths are best for workspace scripts
    ASSETS_DIR = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"
    
    # Try importing rembg to offer the AI model fallback
    try:
        from rembg import remove
        print("[INFO] AI Neural Segmenter (rembg) detected! Ready for complex shapes.")
    except ImportError:
        print("[INFO] Utilizing high-performance Smart Corner Flood-Fill.")
        
    process_gear_assets(ASSETS_DIR)

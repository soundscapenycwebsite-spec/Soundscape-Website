import os
import re

html_path = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\index.html"
assets_dir = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\assets"

def update_html_references():
    print("=== SYNCHRONIZING HTML CATALOG IMAGE REFERENCES ===")
    
    if not os.path.exists(html_path):
        print(f"[ERROR] HTML file not found at: {html_path}")
        return
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # Find all references like "assets/gear_some_name.jpg" or 'assets/gear_some_name.jpg'
    matches = re.findall(r'["\'](assets/gear_[^"\']+\.jpg)["\']', html_content)
    
    if not matches:
        print("No JPEG gear references found in HTML! They may already be synchronized.")
        return
        
    updated_content = html_content
    updates_made = 0
    
    for match in set(matches):
        base_name = os.path.splitext(os.path.basename(match))[0]
        png_filename = f"{base_name}.png"
        png_path = os.path.join(assets_dir, png_filename)
        
        # Check if we have created a transparent PNG version of this asset
        if os.path.exists(png_path):
            old_ref = match
            new_ref = f"assets/{png_filename}"
            
            # Replace in HTML content
            updated_content = updated_content.replace(old_ref, new_ref)
            print(f"  Updated: {old_ref} -> {new_ref}")
            updates_made += 1
        else:
            print(f"  [WARNING] No transparent PNG found for: {match} (skipped replacement)")
            
    if updates_made > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"\n[SUCCESS] Successfully updated {updates_made} references in index.html to pristine PNGs!")
    else:
        print("\nNo references needed updates.")

if __name__ == "__main__":
    update_html_references()

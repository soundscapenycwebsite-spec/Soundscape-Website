import os

html_path = r"c:\Users\Wraith\Desktop\Desktop\Blacklist Development\Projects\Jahn Sanchez Projects\05_Web_Apps\Soundscape NYC\index.html"

# Precise mappings of GEAR_CATALOG ids to their actual dedicated transparent PNG assets
mappings = {
    'ventis112a': 'assets/gear_ventis112a.png',
    'ventis115a': 'assets/gear_ventis115a.png',
    'icoa12': 'assets/gear_icoa12.png',
    'double18_sub': 'assets/gear_double18_sub.png',
    'single21_bass': 'assets/gear_v221_s.png',
    'accuracy': 'assets/gear_accuracy.png',
    'lacoskara2': 'assets/gear_lacoskara2.png',
    'djm900': 'assets/gear_djm900.png',
    'v10': 'assets/gear_v10.png',
    'sub705': 'assets/gear_sub705.png',
    'double21_bc': 'assets/gear_double21_bc.png',
    'lacos_sb28': 'assets/gear_lacos_sb28.png',
    'odysseymedia': 'assets/gear_odysseymedia.png',
    'co2cannon': 'assets/gear_co2_cannon.png' # Optimized 721KB version instead of 5.1MB!
}

def fix_catalog_mismatches():
    print("=== RESOLVING GEAR IMAGE REFERENCE MISMATCHES ===")
    
    if not os.path.exists(html_path):
        print(f"[ERROR] HTML file not found at: {html_path}")
        return
        
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    updated_content = html_content
    replacements_made = 0
    
    for item_id, correct_image in mappings.items():
        # Look for the block containing the id and replace its image reference
        # Example target block: { id: "ventis115a", ..., image: "assets/gear_ventis112.png", ... }
        # We can locate the item's line containing the id and replace the image on or near it.
        
        # To be extremely precise, we use regex or direct string replacement of the specific lines
        # Let's check which lines contain the item IDs in index.html
        pass

    # Direct approach: search for the catalog block and replace the specific lines
    # We will locate the line for each item ID and swap the image path inside it
    lines = html_content.split('\n')
    for i, line in enumerate(lines):
        for item_id, correct_image in mappings.items():
            if f'id: "{item_id}"' in line or f"id: '{item_id}'" in line:
                # Found the line! Replace the image attribute in this line
                # Example: image: "assets/gear_ventis112.png" -> image: "assets/gear_ventis115a.png"
                if 'image: ' in line:
                    # Extract current image path in the line
                    start_idx = line.find('image: "')
                    if start_idx != -1:
                        end_idx = line.find('"', start_idx + 8)
                        old_img = line[start_idx + 8 : end_idx]
                        if old_img != correct_image:
                            lines[i] = line.replace(f'image: "{old_img}"', f'image: "{correct_image}"')
                            print(f"  Fixed {item_id}: image changed from '{old_img}' to '{correct_image}'")
                            replacements_made += 1
                    else:
                        start_idx = line.find("image: '")
                        if start_idx != -1:
                            end_idx = line.find("'", start_idx + 8)
                            old_img = line[start_idx + 8 : end_idx]
                            if old_img != correct_image:
                                lines[i] = line.replace(f"image: '{old_img}'", f"image: '{correct_image}'")
                                print(f"  Fixed {item_id}: image changed from '{old_img}' to '{correct_image}'")
                                replacements_made += 1
                                
    if replacements_made > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print(f"\n[SUCCESS] Successfully corrected {replacements_made} gear catalog image references in index.html!")
    else:
        print("\nNo mismatches needed correction (already up-to-date).")

if __name__ == "__main__":
    fix_catalog_mismatches()

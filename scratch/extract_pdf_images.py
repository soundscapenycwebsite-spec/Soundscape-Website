import os
import sys

# Ensure utf-8 output
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pdf_path = "Sound Scape Equipment May 2026.pdf"
output_dir = "assets/pdf_extracted"
os.makedirs(output_dir, exist_ok=True)

try:
    import fitz # PyMuPDF
    print("PyMuPDF (fitz) is available!")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    img_count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        print(f"Page {page_num+1} has {len(image_list)} images")
        
        for img_idx, img_info in enumerate(image_list):
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            img_count += 1
            img_name = f"extracted_img_{page_num+1}_{img_idx+1}.{image_ext}"
            img_path = os.path.join(output_dir, img_name)
            
            with open(img_path, "wb") as img_file:
                img_file.write(image_bytes)
                
            print(f"Saved {img_path} ({len(image_bytes)} bytes)")
            
    print(f"Successfully extracted {img_count} images!")
except ImportError:
    print("PyMuPDF (fitz) is NOT installed. Trying another library...")
    try:
        from pypdf import PdfReader
        print("pypdf is available!")
        reader = PdfReader(pdf_path)
        img_count = 0
        for page_num, page in enumerate(reader.pages):
            for count, image_file_object in enumerate(page.images):
                img_count += 1
                img_name = f"extracted_img_{page_num+1}_{count+1}_{image_file_object.name}"
                img_path = os.path.join(output_dir, img_name)
                with open(img_path, "wb") as fp:
                    fp.write(image_file_object.data)
                print(f"Saved {img_path} ({len(image_file_object.data)} bytes)")
        print(f"Successfully extracted {img_count} images!")
    except Exception as e:
        print(f"Failed using pypdf: {e}")
except Exception as e:
    print(f"An error occurred: {e}")

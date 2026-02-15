import os
import sys
import pyfiglet
import shutil
import re
from datetime import datetime
from icrawler.builtin import BingImageCrawler
from PIL import Image

def main():
    # 1. Display 3D Text
    ascii_banner = pyfiglet.figlet_format("PintSSv1tt", font="slant")
    print(ascii_banner)
    print("      [ Chrome-Style Search (via Bing) ]\n")

    # 2. Get User Input
    try:
        if sys.stdin.isatty():
            print("What do you want to find? ", end="", flush=True)
            query = sys.stdin.readline().strip()
        else:
            query = sys.stdin.readline().strip()
    except EOFError:
        query = ""
        
    if not query:
        print("\nEmpty search query. Exiting.")
        return

    # 3. Setup Folders
    temp_folder = "temp_dl"
    output_folder = "downloads"
    
    if os.path.exists(temp_folder):
        shutil.rmtree(temp_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    os.makedirs(temp_folder)

    # 4. Search and Download using icrawler (Bing is more stable)
    print(f"Searching for '{query}' and downloading top 5 images...")
    
    bing_crawler = BingImageCrawler(storage={'root_dir': temp_folder})
    bing_crawler.crawl(keyword=query, max_num=5)

    # 5. Convert to PNG and Move to Downloads with Unique Naming
    downloaded_files = os.listdir(temp_folder)
    if not downloaded_files:
        print("No images found or downloaded.")
        shutil.rmtree(temp_folder)
        return

    print(f"Processing and converting {len(downloaded_files)} images...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_query = re.sub(r'[^\w\-_]', '_', query)[:15]
    
    count = 0
    # Sort files to maintain some order
    for filename in sorted(downloaded_files):
        if count >= 5: break
            
        file_path = os.path.join(temp_folder, filename)
        if os.path.isfile(file_path):
            try:
                with Image.open(file_path) as img:
                    # UNIQUE FILENAME: Query + Timestamp + Index
                    png_name = f"{safe_query}_{timestamp}_{count+1}.png"
                    png_path = os.path.join(output_folder, png_name)
                    
                    # Ensure RGB for saving as PNG if needed (though PNG supports RGBA)
                    if img.mode == "P": # Palette images often need conversion
                        img = img.convert("RGBA")
                    elif img.mode not in ("RGB", "RGBA"):
                        img = img.convert("RGB")
                    
                    img.save(png_path, "PNG")
                    print(f"  [+] Saved: {png_name}")
                    count += 1
            except Exception as e:
                # print(f"  [-] Failed to convert {filename}: {e}")
                pass

    # 6. Cleanup
    shutil.rmtree(temp_folder)
    if count > 0:
        print(f"\nSuccess! {count} unique PNG images saved in '{output_folder}/'.")
    else:
        print("\nFailed to process any images. Maybe try a different search term.")

if __name__ == "__main__":
    main()

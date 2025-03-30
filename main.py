import os
import shutil
import imagehash
from PIL import Image
from collections import defaultdict

def get_image_hash(image_path):
    """Generate a perceptual hash (pHash) for an image."""
    try:
        with Image.open(image_path) as img:
            img_hash = imagehash.phash(img)
            print(f"✔ Processed {image_path} | Hash: {img_hash}")  # Debugging line
            return img_hash
    except Exception as e:
        print(f"❌ Error processing {image_path}: {e}")
        return None

def find_duplicates(source_folder, destination_folder):
    """Find duplicate images in a folder and move them to another folder."""
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    hash_dict = defaultdict(list)

    # Scan all images in the source folder
    print(f"📂 Scanning folder: {source_folder}")
    files_found = 0

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)
        if os.path.isfile(file_path) and file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            files_found += 1
            image_hash = get_image_hash(file_path)
            if image_hash:
                hash_dict[image_hash].append(file_path)

    if files_found == 0:
        print("⚠ No images found in the source folder.")
        return

    # Move duplicates to the destination folder
    duplicates_moved = 0
    for image_list in hash_dict.values():
        if len(image_list) > 1:
            print(f"🔍 Found duplicates: {image_list}")
            for duplicate in image_list[1:]:  # Keep the first one, move the rest
                shutil.move(duplicate, os.path.join(destination_folder, os.path.basename(duplicate)))
                print(f"📦 Moved duplicate: {duplicate}")
                duplicates_moved += 1

    if duplicates_moved == 0:
        print("✅ No duplicates found.")
    else:
        print(f"✅ Total duplicates moved: {duplicates_moved}")

if __name__ == "__main__":
    source_folder = "./images"  # Change to your folder path
    destination_folder = "./duplicates"  # Folder where duplicates will be moved
    
    if not os.path.exists(source_folder):
        print(f"❌ Error: Source folder '{source_folder}' does not exist!")
    else:
        find_duplicates(source_folder, destination_folder)
        print("🎯 Duplicate detection and moving completed.")

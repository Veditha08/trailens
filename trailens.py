import os
from datetime import datetime
from PIL import Image, ExifTags
import ollama

PHOTOS_DIR = "./hike_photos"
OUTPUT_FILE = "TRAIL_JOURNAL.md"

def get_exif_data(image_path):
    """Extracts timestamp and GPS data if available."""
    metadata = {"timestamp": "Unknown Date", "gps": None}
    try:
        with Image.open(image_path) as img:
            exif = img._getexif()
            if not exif:
                return metadata
            
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id, tag_id)
                if tag == "DateTimeOriginal":
                    metadata["timestamp"] = value
                elif tag == "GPSInfo":
                    # Flag that GPS metadata exists
                    metadata["gps"] = "GPS coordinates recorded in EXIF"
    except Exception:
        pass
    return metadata

def analyze_photo(image_path):
    """Sends image to local Moondream model via Ollama."""
    prompt = (
        "You are an expert field naturalist and botanist. "
        "Examine this photo taken on a trail. "
        "1. Identify the primary plant, tree, fungus, animal, or rock/terrain visible. "
        "2. Give its common name (and scientific name if identifiable). "
        "3. Write a 1-2 sentence ecological observation about it."
    )
    
    response = ollama.chat(
        model="moondream",
        messages=[{
            "role": "user",
            "content": prompt,
            "images": [image_path]
        }]
    )
    return response["message"]["content"].strip()

def build_journal():
    valid_exts = (".jpg", ".jpeg", ".png", ".webp")
    photo_files = [
        f for f in os.listdir(PHOTOS_DIR) 
        if f.lower().endswith(valid_exts)
    ]
    
    if not photo_files:
        print(f"[!] No photos found in {PHOTOS_DIR}. Add some images first!")
        return

    print(f"[*] Found {len(photo_files)} photos. Generating journal...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# 🌲 TraiLens: Automated Field Journal\n\n")
        out.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} entirely offline using open-weight vision model (Moondream via Ollama).*\n\n")
        out.write("---\n\n")
        
        for idx, filename in enumerate(sorted(photo_files), 1):
            filepath = os.path.join(PHOTOS_DIR, filename)
            print(f"[{idx}/{len(photo_files)}] Analyzing {filename}...")
            
            metadata = get_exif_data(filepath)
            notes = analyze_photo(filepath)
            
            out.write(f"## Entry #{idx}: `{filename}`\n\n")
            out.write(f"![{filename}]({filepath})\n\n")
            out.write(f"- **Captured At:** {metadata['timestamp']}\n")
            if metadata["gps"]:
                out.write(f"- **Location Data:** {metadata['gps']}\n")
            out.write("\n### Field Naturalist Notes\n")
            out.write(f"> {notes}\n\n")
            out.write("---\n\n")

    print(f"Success! Trail journal saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    build_journal()
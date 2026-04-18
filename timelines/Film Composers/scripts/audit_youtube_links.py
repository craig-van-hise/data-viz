import json
import os
import re
import yt_dlp
import time

def normalize_text(text):
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Strip special characters and punctuation (keep only alphanumeric and spaces)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def audit_links():
    data_dir = 'data/filmographies/'
    files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'extract_flat': True,
        'no_warnings': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for filename in files:
            filepath = os.path.join(data_dir, filename)
            print(f"Auditing {filename}...")
            
            # Extract composer's last name from filename
            composer_name_parts = filename.replace('.json', '').split('_')
            composer_last_name = normalize_text(composer_name_parts[-1])
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue

            updated = False
            for item in data:
                youtube_link = item.get('youtube_link')
                if not youtube_link:
                    continue

                film_title = item.get('title', '')
                normalized_film_title = normalize_text(film_title)

                try:
                    # Added a small delay to respect YouTube's rate limits
                    time.sleep(1.5)
                    
                    info = ydl.extract_info(youtube_link, download=False)
                    yt_title = info.get('title', '')
                    yt_description = info.get('description', '') or ""
                    
                    normalized_yt_title = normalize_text(yt_title)
                    normalized_yt_description = normalize_text(yt_description)

                    # Check A: Does normalized film title exist in normalized YouTube title?
                    check_a = False
                    if normalized_film_title:
                        pattern = rf'\b{re.escape(normalized_film_title)}\b'
                        if re.search(pattern, normalized_yt_title):
                            check_a = True

                    # Check B: Film title AND Composer's last name in description?
                    check_b = False
                    if not check_a:
                        if normalized_film_title and composer_last_name:
                            if (normalized_film_title in normalized_yt_description) and (composer_last_name in normalized_yt_description):
                                check_b = True

                    if not check_a and not check_b:
                        print(f"  FAILED validation for '{film_title}': {youtube_link}")
                        item['youtube_link'] = None
                        updated = True
                    else:
                        print(f"  Passed: '{film_title}'")

                except Exception as e:
                    error_msg = str(e)
                    # Critical: If rate limited, we MUST stop and NOT set the link to null
                    if "rate-limited" in error_msg.lower():
                        print("\nCRITICAL: Rate limit hit. Saving current progress and stopping script.")
                        if updated:
                            with open(filepath, 'w', encoding='utf-8') as f:
                                json.dump(data, f, indent=4)
                        return # Exit the entire script

                    print(f"  ERROR for '{film_title}' ({youtube_link}): Video unavailable or private.")
                    item['youtube_link'] = None
                    updated = True

            if updated:
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    print(f"  Updated {filename}")
                except Exception as e:
                    print(f"  Error writing to {filename}: {e}")

if __name__ == "__main__":
    audit_links()

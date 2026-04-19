import json
import os
import re
import yt_dlp
import time
import random
import sys

# Setup paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
FILMOGRAPHIES_DIR = os.path.join(PROJECT_ROOT, "data/filmographies")
CHECKPOINT_FILE = os.path.join(SCRIPT_DIR, ".verify_checkpoint")


def normalize_text(text):
    if not text:
        return ""
    # Convert to lowercase
    text = text.lower()
    # Strip special characters and punctuation (keep only alphanumeric and spaces)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text.strip()

def get_films_to_process(films, threshold=12):
    """
    Returns a list of indices representing which films need scraping.
    
    1. State 1 & 2 (Total Blank/Failure):
       If the array has 0 valid youtube_links (missing or every link is null), return ALL indices.
    
    2. State 3 (Cascades & Blocks):
       Find contiguous blocks of missing or null links. If a block's length >= threshold, 
       add the indices of THAT block to the return list.
    """
    valid_links_count = sum(1 for film in films if film.get('youtube_link'))
    
    if valid_links_count == 0:
        return list(range(len(films)))
    
    target_indices = []
    current_block = []
    
    for i, film in enumerate(films):
        if not film.get('youtube_link'):
            current_block.append(i)
        else:
            if len(current_block) >= threshold:
                target_indices.extend(current_block)
            current_block = []
            
    # Don't forget the last block
    if len(current_block) >= threshold:
        target_indices.extend(current_block)
        
    return target_indices

def verify_film_link(film_title, composer_last_name, yt_title, yt_description):
    normalized_film_title = normalize_text(film_title)
    normalized_yt_title = normalize_text(yt_title)
    normalized_yt_description = normalize_text(yt_description or "")
    
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
                
    return check_a or check_b

def main():
    if not os.path.exists(FILMOGRAPHIES_DIR):
        print(f"Error: Directory not found: {FILMOGRAPHIES_DIR}")
        return

    files = sorted([f for f in os.listdir(FILMOGRAPHIES_DIR) if f.endswith('.json')])
    
    # Load already processed files
    processed_files = set()
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, 'r') as f:
            processed_files = set(line.strip() for line in f if line.strip())

    
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'no_warnings': True,
        'cookiesfrombrowser': ('chrome',),
        'skip_download': True,
        'extract_flat': True, # Only want metadata, avoid format resolution errors
        'ignoreerrors': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
    }


    print("\n[!] Attempting to use Google Chrome cookies for authentication.")
    print("[!] IF YOU ARE ON A MAC: You will see a prompt for your keychain password.")
    print("[!] You MUST enter your password and click 'Always Allow' for the script to continue.\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for filename in files:
            if filename in processed_files:
                continue

            filepath = os.path.join(FILMOGRAPHIES_DIR, filename)

            
            # Composer info
            composer_name = filename.replace('.json', '').replace('_', ' ')
            composer_parts = filename.replace('.json', '').split('_')
            composer_last_name = normalize_text(composer_parts[-1])
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                continue
                
            films = data if isinstance(data, list) else data.get('filmography', [])
            if not films:
                continue
                
            indices_to_process = get_films_to_process(films)
            if not indices_to_process:
                print(f"Skipping {filename} (no large missing blocks found).")
                continue
                
            print(f"\nProcessing {filename} ({len(indices_to_process)} films need scraping)...")
            
            for idx in indices_to_process:
                film = films[idx]
                film_title = film.get('title', 'Unknown Title')
                search_query = f"ytsearch1:{film_title} {composer_name} main theme suite"
                
                max_retries = 4
                retry_delay = 300 # 5 minutes

                passed = False
                found_url = None
                
                for attempt in range(max_retries):
                    try:
                        # Jitter
                        time.sleep(random.uniform(2.0, 5.0))
                        
                        print(f"  Searching: '{film_title}' (Attempt {attempt + 1}/{max_retries})...")
                        result = ydl.extract_info(search_query, download=False)
                        
                        if not result:
                            print(f"    ⚠️ Warning: yt-dlp returned None for {film_title}")
                            found_url = None
                            passed = False
                            break

                        # ytsearch1 returns a playlist structure
                        entries = result.get('entries', [])
                        if not entries or not entries[0]:
                            print(f"    ⚠️ Warning: No search results found for {film_title}")
                            found_url = None
                            passed = True # Mark as processed (failed)
                            break
                            
                        first_entry = entries[0]
                        if not first_entry:
                            print(f"    ⚠️ Warning: First entry in search result is None")
                            found_url = None
                            passed = True
                            break

                        yt_title = first_entry.get('title', '')
                        yt_description = first_entry.get('description', '') or ""
                        yt_url = first_entry.get('url') or first_entry.get('webpage_url')
                        
                        if yt_url and not yt_url.startswith('http'):
                            yt_url = f"https://www.youtube.com/watch?v={yt_url}"
                        
                        if not yt_url and first_entry.get('id'):
                            yt_url = f"https://www.youtube.com/watch?v={first_entry.get('id')}"

                        
                        if verify_film_link(film_title, composer_last_name, yt_title, yt_description):
                            print(f"    ✅ MATCH FOUND: {yt_url}")
                            found_url = yt_url
                            passed = True
                        else:
                            print(f"    ❌ VERIFICATION FAILED: {yt_title}")
                            found_url = None
                            passed = True # We consider it "processed" even if it failed verification
                        
                        # Exit retry loop
                        break
                        
                    except Exception as e:
                        error_msg = str(e).lower()
                        if "rate-limited" in error_msg or "try again later" in error_msg or "429" in error_msg:
                            if attempt < max_retries - 1:
                                print(f"    ⚠️ Rate limit hit! Waiting {retry_delay // 60} minutes...")
                                time.sleep(retry_delay)
                                retry_delay *= 2
                                continue
                            else:
                                print("    🛑 CRITICAL: Max retries reached on rate limit. Exiting.")
                                sys.exit(1)
                        else:
                            print(f"    ⚠️ Error: {e}")
                            break # Move to next film on other errors
                
                # Update film and save file immediately
                if passed:
                    film['youtube_link'] = found_url
                else:
                    # If we exhausted retries or failed completely, we don't necessarily want to mark it null 
                    # but the task says "If it fails, set film['youtube_link'] = None"
                    # However, if it's a rate limit exit, we already exited. 
                    # If it's a search failure, set to None.
                    film['youtube_link'] = None
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)

            # Mark file as processed in checkpoint
            with open(CHECKPOINT_FILE, 'a') as f:
                f.write(f"{filename}\n")
                f.flush()
                os.fsync(f.fileno())
            print(f"  [Checkpoint Locked: {filename}]")


if __name__ == "__main__":
    main()

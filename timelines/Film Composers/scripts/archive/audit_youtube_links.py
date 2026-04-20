import json
import os
import re
import yt_dlp
import time
import random
import sys

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
    checkpoint_file = 'scripts/.audit_checkpoint'
    
    # Load already processed files
    processed_files = set()
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            processed_files = set(line.strip() for line in f if line.strip())

    files = sorted([f for f in os.listdir(data_dir) if f.endswith('.json')])

    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'no_warnings': True,
        'cookiesfrombrowser': ('chrome',),
        'skip_download': True,
        'extract_flat': True,
        'ignoreerrors': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
        'sleep_interval_requests': 3,
        'sleep_interval': 4,
        'max_sleep_interval': 7,
    }

    print("\n[!] Attempting to authenticate using Google Chrome cookies.")
    print("[!] IF YOU ARE ON A MAC: You will see a prompt for your keychain password.")
    print("[!] You MUST enter your password and click 'Always Allow' for the script to continue.\n")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for filename in files:
            if filename in processed_files:
                continue

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

                max_retries = 4
                retry_delay = 300 # Start with a 5-minute pause for rate limits

                for attempt in range(max_retries):
                    try:
                        # Jitter for the initial request
                        time.sleep(random.uniform(2.0, 4.0))
                        
                        info = ydl.extract_info(youtube_link, download=False, process=False)
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
                            
                        # Break out of retry loop on success or clean text failure
                        break 

                    except Exception as e:
                        error_msg = str(e).lower()
                        
                        # CRITICAL: Catch the exact yt-dlp rate limit strings
                        if "rate-limited" in error_msg or "try again later" in error_msg or "429" in error_msg:
                            if attempt < max_retries - 1:
                                print(f"\n[!] Rate limit hit! YouTube is blocking us.")
                                print(f"[!] Auto-pausing for {retry_delay // 60} minutes before retrying (Attempt {attempt + 1}/{max_retries})...")
                                time.sleep(retry_delay)
                                retry_delay *= 2 # Exponential backoff (5m -> 10m -> 20m)
                                continue # Retry the exact same URL
                            else:
                                print("\nCRITICAL: Max retries reached. YouTube is completely blocking this IP.")
                                print("Saving progress and shutting down to protect data.")
                                if updated:
                                    with open(filepath, 'w', encoding='utf-8') as f:
                                        json.dump(data, f, indent=4)
                                sys.exit(1)

                        # If we reach here, it is a genuine dead/private link, NOT a rate limit
                        print(f"  ERROR for '{film_title}': Video unavailable or private.")
                        item['youtube_link'] = None
                        updated = True
                        break # Break loop, move to next video

            # Save data and update checkpoint
            if updated:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4)
                print(f"  Updated {filename}")
            
            # Mark file as processed and FORCE flush to hard drive immediately
            with open(checkpoint_file, 'a') as f:
                f.write(f"{filename}\n")
                f.flush()
                os.fsync(f.fileno())
            print(f"  [Checkpoint Locked: {filename}]")

if __name__ == "__main__":
    audit_links()

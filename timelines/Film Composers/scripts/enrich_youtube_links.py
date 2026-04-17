import json
import os
import requests
import re
import time
import random
import urllib.parse

# Setup paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
FILMOGRAPHIES_DIR = os.path.join(PROJECT_ROOT, "data/filmographies")

# Realistic headers to avoid immediate blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

def get_youtube_link(title, composer):
    """
    Scrapes YouTube search results for a film's main theme.
    """
    # Search query optimize for scores/suites
    query = f"{title} {composer} main theme suite"
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        # Regex to find the first video ID in the YouTube internal JSON response
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', res.text)
        
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
                
    except Exception as e:
        print(f"    ⚠️ Error searching {title}: {e}")
        
    return None

def main():
    if not os.path.exists(FILMOGRAPHIES_DIR):
        print(f"Error: Directory not found: {FILMOGRAPHIES_DIR}")
        return

    json_files = [f for f in os.listdir(FILMOGRAPHIES_DIR) if f.endswith('.json')]
    json_files.sort() # Process alphabetically
    
    print(f"🚀 Starting YouTube enrichment for {len(json_files)} filmography files...")
    
    for i, json_file in enumerate(json_files):
        composer_name = json_file.replace(".json", "").replace("_", " ")
        json_path = os.path.join(FILMOGRAPHIES_DIR, json_file)
        
        print(f"[{i+1}/{len(json_files)}] Processing {composer_name}...")
        
        try:
            with open(json_path, 'r') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ❌ Failed to load {json_file}: {e}")
            continue
            
        # Handle different JSON structures (list vs. dict with 'filmography' key)
        films = data if isinstance(data, list) else data.get('filmography', [])
        
        if not films:
            print(f"  ⚠️ No films found in {json_file}")
            continue

        updated_count = 0
        total_films = len(films)
        
        for j, film in enumerate(films):
            # Skip if already has a link
            if 'youtube_link' in film and film['youtube_link']:
                continue
                
            title = film.get('title')
            if not title:
                continue
                
            link = get_youtube_link(title, composer_name)
            
            if link:
                film['youtube_link'] = link
                updated_count += 1
                print(f"  ({j+1}/{total_films}) Found: {title}")
                # Respectful delay between searches
                time.sleep(random.uniform(0.5, 1.2))
            else:
                # Still sleep a bit if not found
                time.sleep(0.2)
        
        if updated_count > 0:
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"  ✅ Saved {updated_count} new links to {json_file}")
        else:
            print(f"  ℹ️ No new links needed/found for {composer_name}")

    print("\n🎉 Enrichment complete!")

if __name__ == "__main__":
    main()

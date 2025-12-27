import json
import os
import requests
import re
import time
import random
import urllib.parse

# Setup paths
base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
json_path = os.path.join(base_dir, "data/Most important films.json")

# Realistic headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

def get_youtube_link(title, composer):
    # Search query: "{Title}" {Composer} main theme suite
    query = f"{title} {composer} main theme suite"
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        
        # Regex for video ID
        # "videoId":"VIDEO_ID"
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', res.text)
        
        if video_ids:
            # Return first one
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
                
    except Exception as e:
        print(f"Error searching {title}: {e}")
        
    return None

def main():
    with open(json_path, 'r') as f:
        data = json.load(f)
        
    updated_count = 0
    total_count = 0
    
    print("Starting YouTube enrichment...")
    
    try:
        for entry in data:
            composer = entry['composer']
            for film in entry['films']:
                total_count += 1
                
                # Update progress
                # if total_count % 10 == 0:
                #    print(f"Processed {total_count} films...")

                # Skip if already has link
                if 'youtube_link' in film and film['youtube_link']:
                    continue
                    
                title = film['title']
                
                link = get_youtube_link(title, composer)
                
                if link:
                    print(f"[{updated_count+1}] Found: {title} -> {link}")
                    film['youtube_link'] = link
                    updated_count += 1
                else:
                    print(f"[{updated_count+1}] Not Found: {title}")
                
                # Sleep to avoid rate limits
                # Youtube is sensitive. 1s is bare minimum. 2-4s is safer.
                time.sleep(random.uniform(0.5, 1.5))
                
                # Save periodically (every 5 updates)
                if updated_count % 5 == 0 and updated_count > 0:
                    with open(json_path, 'w') as f:
                        json.dump(data, f, indent=4)

    except KeyboardInterrupt:
        print("\nStopping...")
        
    # Final save
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Done. Updated {updated_count} films.")

if __name__ == "__main__":
    main()

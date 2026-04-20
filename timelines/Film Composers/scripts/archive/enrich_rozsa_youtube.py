import json
import os
import requests
import re
import urllib.parse
import time
import random

# CONFIG
base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
input_json = os.path.join(base_dir, "data/filmographies/Miklós_Rózsa.json")
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def get_youtube_link(title, composer="Miklós Rózsa"):
    # Search for "Title Composer suite" or "Title Composer theme"
    query = f"{title} {composer} suite"
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        # Extract video ID
        # Pattern: "videoId":"(VIDEO_ID)"
        video_ids = re.findall(r'\"videoId\":\"([a-zA-Z0-9_-]{11})\"', res.text)
        
        if video_ids:
            return f"https://www.youtube.com/watch?v={video_ids[0]}"
    except Exception as e:
        print(f"    Error: {e}")
        
    return None

def process():
    with open(input_json, 'r') as f:
        data = json.load(f)
        
    films = data.get('filmography', [])
    updated = False
    
    print(f"Enriching YouTube links for {len(films)} entries...")
    
    for film in films:
        title = film.get('title', '')
        if not title: continue
        
        # Skip if already has link
        if 'youtube_link' in film and film['youtube_link']:
            continue
            
        # Skip concert pieces
        is_concert_music = any(x in title for x in ["Op.", "Concerto", "Sonata", "Symphony", "Quartet", "Trio", "Quintet", "Variations", "Motet"])
        if is_concert_music:
            # Maybe we DO want youtube links for concert music? 
            # The prompt said "filmography", but the file has concert music.
            # Let's try to get them anyway, it adds value.
            pass

        print(f"Searching: {title}")
        link = get_youtube_link(title)
        
        if link:
            print(f"    Found: {link}")
            film['youtube_link'] = link
            updated = True
        else:
            print(f"    Not found.")
            
        time.sleep(random.uniform(1.0, 2.0))
        
        # Save periodically
        if updated and random.random() < 0.1:
             with open(input_json, 'w') as f:
                json.dump(data, f, indent=2)
             print("    (Saved progress)")
             updated = False

    # Final save
    with open(input_json, 'w') as f:
        json.dump(data, f, indent=2)
    print("Done.")

if __name__ == "__main__":
    process()

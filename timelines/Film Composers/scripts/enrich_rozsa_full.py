import json
import os
import re
import requests
from bs4 import BeautifulSoup
import time
import random

# CONFIG
base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
input_json = os.path.join(base_dir, "data/filmographies/Miklós_Rózsa.json")
thumb_base = os.path.join(base_dir, "thumbnails/Miklós Rózsa")

if not os.path.exists(thumb_base):
    os.makedirs(thumb_base)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def sanitize_filename(title):
    s = re.sub(r"['\".\-:!?]", "", title)
    return s.strip()

def scrape_imdb_poster(url):
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        meta = soup.find('meta', property='og:image')
        # Check if it's the generic imdb logo
        if meta and "nopicture" not in meta['content'] and "imdb_logo" not in meta['content']:
            return meta['content']
    except:
        pass
    return None

def find_imdb_via_wiki(title, year):
    # Search for wiki page first
    candidates = [
        title,
        f"{title} ({year} film)",
        f"{title} (film)",
        f"{title} ({year})"
    ]
    
    for c in candidates:
        slug = c.replace(" ", "_")
        wiki_url = f"https://en.wikipedia.org/wiki/{slug}"
        
        try:
            res = requests.get(wiki_url, headers=headers, timeout=5)
            if res.status_code == 200:
                # Page exists, look for IMDb link
                # Usually regex for imdb.com/title/tt\d+
                match = re.search(r'imdb\.com/title/(tt\d+)', res.text)
                if match:
                    imdb_id = match.group(1)
                    imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
                    print(f"    Wiki ({c}) -> IMDb ({imdb_id})")
                    return scrape_imdb_poster(imdb_url)
        except:
            pass
            
    return None

def process():
    with open(input_json, 'r') as f:
        data = json.load(f)
    
    films = data.get('filmography', [])
    print(f"Found {len(films)} entries")
    
    for film in films:
        title = film.get('title')
        date = film.get('release_date', '')
        if not title: continue
        
        # Skip concert pieces
        if any(x in title for x in ["Op.", "Concerto", "Sonata", "Symphony", "Quartet", "Trio", "Quintet", "Variations", "Motet"]):
            continue

        year = date[:4] if date else ""
        safe_title = sanitize_filename(title)
        save_path = os.path.join(thumb_base, safe_title + ".jpg")
        
        if os.path.exists(save_path):
            continue
            
        print(f"Processing: {title} ({year})")
        
        # Try finding via Wiki bridge
        img_url = find_imdb_via_wiki(title, year)
        
        if img_url:
            try:
                img_data = requests.get(img_url, headers=headers, timeout=10).content
                with open(save_path, 'wb') as f:
                    f.write(img_data)
                print("    Downloaded.")
            except:
                print("    Download failed.")
        else:
            print("    No poster found (via Wiki).")
            
        time.sleep(0.5) # Wiki is fast, but be polite

if __name__ == "__main__":
    process()

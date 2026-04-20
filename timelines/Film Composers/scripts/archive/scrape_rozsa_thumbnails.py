import os
import requests
from bs4 import BeautifulSoup
import time
import random

# CONFIG
base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
thumb_base = os.path.join(base_dir, "thumbnails/Miklós Rózsa")

if not os.path.exists(thumb_base):
    os.makedirs(thumb_base)

# Map Films to verified IMDb IDs to ensure correct poster
films_to_scrape = {
    "Double Indemnity": "tt0036775",
    "The Killers": "tt0038669",
    "Quo Vadis": "tt0043949",
    "El Cid": "tt0054847",
    "King of Kings": "tt0055047",
    "The Thief of Bagdad": "tt0033152",
    "The Jungle Book": "tt0034928"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def download_poster(title, imdb_id):
    url = f"https://www.imdb.com/title/{imdb_id}/"
    print(f"Fetching {title} from {url}...")
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"  Error: HTTP {res.status_code}")
            return
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Method 1: og:image (Standard high quality)
        img_url = None
        meta = soup.find('meta', property='og:image')
        if meta:
            img_url = meta['content']
            
        # Fallback? usually og:image is reliable for main poster on IMDb
        
        if img_url:
            print(f"  Found Image: {img_url}")
            
            # Download
            img_data = requests.get(img_url, headers=headers, timeout=10).content
            
            # Save
            filename = title.replace(":", " ") + ".jpg" # Simple sanitize
            file_path = os.path.join(thumb_base, filename)
            
            with open(file_path, 'wb') as f:
                f.write(img_data)
            print(f"  Saved to {file_path}")
        else:
            print("  Could not find og:image")
            
    except Exception as e:
        print(f"  Exception: {e}")

print("Starting targeted IMDb scrape for Miklós Rózsa...")

for title, imdb_id in films_to_scrape.items():
    download_poster(title, imdb_id)
    time.sleep(random.uniform(1.0, 3.0)) # Be polite

print("Done.")

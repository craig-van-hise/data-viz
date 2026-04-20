import json
import os
import re
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime
import concurrent.futures

# CONFIG
base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
films_dir = os.path.join(base_dir, "data/filmographies")
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def clean_date(date_str):
    try:
        date_str = re.sub(r'\[.*?\]', '', date_str).strip()
        date_str = re.sub(r'\(.*?\)', '', date_str).strip()
        
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
            
        for fmt in ("%d %B %Y", "%B %d, %Y", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None
    except:
        return None

def get_wiki_date(title, year):
    candidates = [
        title,
        f"{title} ({year} film)",
        f"{title} (film)"
    ]
    
    for c in candidates:
        slug = c.replace(" ", "_")
        url = f"https://en.wikipedia.org/wiki/{slug}"
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                infobox = soup.find('table', class_='infobox')
                if infobox:
                    for row in infobox.find_all('tr'):
                        header = row.find('th')
                        if header and "Release date" in header.get_text():
                            cell = row.find('td')
                            if cell:
                                text = cell.get_text(separator="\n").strip()
                                lines = text.split('\n')
                                for line in lines:
                                    cleaned = clean_date(line)
                                    if cleaned:
                                        return cleaned
                                        
                                date_pattern = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})|([A-Za-z]+\s+\d{1,2},\s+\d{4})', text)
                                if date_pattern:
                                    raw_date = date_pattern.group(0)
                                    cleaned = clean_date(raw_date)
                                    if cleaned:
                                         return cleaned

        except Exception:
            pass
            
    return None

def process_film(film):
    # Worker function for a single film
    title = film.get('title')
    curr_date = film.get('release_date', '')
    
    if len(curr_date) == 4 and curr_date.isdigit():
        new_date = get_wiki_date(title, curr_date)
        if new_date:
            return (title, new_date)
    return None

def process_file_threaded(filename):
    filepath = os.path.join(films_dir, filename)
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    print(f"Processing {data.get('composer')} (Threaded)...")
    
    films = data.get('filmography', [])
    updates_made = False
    
    # Identify films needing update
    films_to_update = [f for f in films if len(f.get('release_date','')) == 4]
    
    if not films_to_update:
        return

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_film = {executor.submit(process_film, film): film for film in films_to_update}
        
        for future in concurrent.futures.as_completed(future_to_film):
            film = future_to_film[future]
            try:
                result = future.result()
                if result:
                    title, new_date = result
                    film['release_date'] = new_date
                    print(f"  Refined: {title} -> {new_date}")
                    updates_made = True
            except Exception as e:
                print(f"  Error processing {film.get('title')}: {e}")
                
    if updates_made:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  Saved updates for {filename}")

# Main loop
files = [f for f in os.listdir(films_dir) if f.endswith(".json")]
files.sort()

# Process files sequentially, but films within them in parallel
# Or parallelize files? Parallelizing files is better.
# Let's parallelize files processing.

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(process_file_threaded, files)

print("Done.")

import json
import os
import re
import requests
from bs4 import BeautifulSoup
import time
import random
from datetime import datetime

# CONFIG
base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
films_dir = os.path.join(base_dir, "data/filmographies")
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def clean_date(date_str):
    # Standardize to YYYY-MM-DD
    # Input examples: "July 3, 1944", "3 July 1944", "1944-07-03", "July 1944"
    try:
        # Remove citations like [1]
        date_str = re.sub(r'\[.*?\]', '', date_str).strip()
        # Remove parens like (United States)
        date_str = re.sub(r'\(.*?\)', '', date_str).strip()
        
        # Tyupical formats
        # 1. Full Date: 3 July 1944 or July 3, 1944
        # 2. Year only: 1944
        
        # Try finding YYYY-MM-DD first (already done?)
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return date_str
            
        # Try parse with datetime
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
    # Similar to thumbnail scraper, find the wiki page
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
                    # Look for Release date row
                    for row in infobox.find_all('tr'):
                        header = row.find('th')
                        if header and "Release date" in header.get_text():
                            # The data is in the td
                            cell = row.find('td')
                            if cell:
                                # Often contains list, get the first date
                                # Handle <br> lists
                                text = cell.get_text(separator="\n").strip()
                                lines = text.split('\n')
                                for line in lines:
                                    # Try to extract date
                                    cleaned = clean_date(line)
                                    if cleaned:
                                        print(f"    Found Date: {cleaned} (Wiki: {c})")
                                        return cleaned
                                        
                                # If clean_date failed on strict match, try regex extraction
                                # Look for "Month DD, YYYY" or "DD Month YYYY"
                                # Regex for Day Month Year or Month Day Year
                                date_pattern = re.search(r'(\d{1,2}\s+[A-Za-z]+\s+\d{4})|([A-Za-z]+\s+\d{1,2},\s+\d{4})', text)
                                if date_pattern:
                                    raw_date = date_pattern.group(0)
                                    cleaned = clean_date(raw_date)
                                    if cleaned:
                                         print(f"    Found Date (Regex): {cleaned} (Wiki: {c})")
                                         return cleaned

        except Exception as e:
            # print(f"Error checking {url}: {e}")
            pass
            
    return None

def process_file(filename):
    filepath = os.path.join(films_dir, filename)
    with open(filepath, 'r') as f:
        data = json.load(f)
        
    updated = False
    print(f"Processing {data.get('composer')}...")
    
    for film in data.get('filmography', []):
        curr_date = film.get('release_date', '')
        # Check if it needs refinement (len 4 is just Year)
        if len(curr_date) == 4 and curr_date.isdigit():
            title = film.get('title')
            print(f"  Refining: {title} ({curr_date})")
            
            new_date = get_wiki_date(title, curr_date)
            if new_date:
                film['release_date'] = new_date
                updated = True
                # Don't sleep too long for verified hits, but keep rate limit
                time.sleep(0.5)
            else:
                print(f"    Could not find precise date.")
                time.sleep(0.5)
    
    if updated:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"  Saved updates for {filename}")

# Process all files
files = [f for f in os.listdir(films_dir) if f.endswith(".json")]
files.sort()

for filename in files:
    process_file(filename)
    # Pause between files
    time.sleep(1)

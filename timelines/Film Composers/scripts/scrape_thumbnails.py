import json
import os
import re
import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse

# 1. SETUP
base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
json_path = os.path.join(base_dir, "data/Most important films.json")
thumb_base = os.path.join(base_dir, "thumbnails")

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

def sanitize_filename(title):
    s = re.sub(r"['\".\-]", "", title)
    s = s.replace(":", " ")
    return s.strip()

def get_wikipedia_poster(title, year):
    # Try probable Wikipedia URLs
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
                # Find infobox image
                infobox = soup.find('table', class_='infobox')
                if infobox:
                    img = infobox.find('img')
                    if img:
                        src = img['src']
                        if src.startswith('//'):
                            src = "https:" + src
                        # Get higher res (remove /thumb/ and scale down logic?)
                        # Wiki images are usually: .../thumb/a/a9/Name.jpg/220px-Name.jpg
                        # We want original: .../a/a9/Name.jpg
                        if "/thumb/" in src:
                            parts = src.split('/thumb/')
                            base = parts[0] + '/' + parts[1]
                            # The part after the last slash in parts[1] is the thumb width, remove it
                            # url/thumb/x/y/Filename.jpg/220px-Filename.jpg
                            # We want url/x/y/Filename.jpg
                            # Actually easier: just take parts[0] + '/' + parts[1].split('/')[0] + '/' + parts[1].split('/')[1]
                            # Let's keep it simple: just use the thumb or try to strip the suffix
                            # /a/b/Name.jpg/220px-Name.jpg -> Remove last segment
                            original = os.path.dirname(src) # No, that's not right for Wiki structure
                            
                            # Regex to match /thumb/(...)/220px-...
                            # src: //upload.../thumb/a/b/File.jpg/220px-File.jpg
                            # target: //upload.../a/b/File.jpg
                            
                            # Split by /
                            # .../thumb/a/b/File.jpg/220px-File.jpg
                            # We want everything up to File.jpg, excluding /thumb/
                            
                            sub = src.split('/thumb/')[-1] # a/b/File.jpg/220px-File.jpg
                            path_parts = sub.split('/')
                            # Actual file name is usually path_parts[-2] if it ends with width
                            # Let's construct: "https://upload.wikimedia.org/wikipedia/..."
                            # Just remove "/thumb" and the last segment
                            
                            full_url = src.replace("/thumb/", "/")
                            # Now remove the last slash part
                            full_url = "/".join(full_url.split('/')[:-1])
                            
                            return full_url
                        return src
        except:
            continue
            
    return None

def get_imdb_poster_html(title, year):
    # Search DDG HTML
    # We print more info to debug
    query = f"{title} {year} site:imdb.com"
    ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    
    try:
        res = requests.get(ddg_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Look for result link
        for a in soup.find_all('a', class_='result__a'):
            href = a.get('href', '')
            # Clean DDG redirect
            if 'uddg=' in href:
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(href).query)
                if 'uddg' in qs:
                    href = qs['uddg'][0]
            
            if "imdb.com/title/tt" in href:
                # Found it
                print(f"    IMDb URL: {href}")
                res_imdb = requests.get(href, headers=headers, timeout=10)
                soup_imdb = BeautifulSoup(res_imdb.text, 'html.parser')
                meta = soup_imdb.find('meta', property='og:image')
                if meta:
                    return meta['content']
                break
                
    except Exception as e:
        print(f"    DDG Error: {e}")
    return None

# 2. MAIN LOOP
with open(json_path, 'r') as f:
    data = json.load(f)

for entry in data:
    composer = entry['composer']
    comp_dir = os.path.join(thumb_base, composer)
    if not os.path.exists(comp_dir):
        os.makedirs(comp_dir)
        
    for film in entry['films']:
        title = film['title']
        date = film['release_date']
        year = date.split('-')[0]
        safe_title = sanitize_filename(title)
        
        file_path = os.path.join(comp_dir, safe_title + ".jpg")
        
        if not os.path.exists(file_path):
            print(f"Processing: {title} ({year})")
            
            # Try IMDb via DDG
            img_url = get_imdb_poster_html(title, year)
            if not img_url:
                print("    IMDb not found, trying Wikipedia...")
                img_url = get_wikipedia_poster(title, year)
            
            if img_url:
                print(f"    Found Image: {img_url}")
                try:
                    img_data = requests.get(img_url, headers=headers, timeout=10).content
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                    print("    Downloaded.")
                except Exception as e:
                    print(f"    Failed download: {e}")
            else:
                print("    Could not find poster anywhere.")
            
            time.sleep(random.uniform(0.5, 1.5))

print("Done.")

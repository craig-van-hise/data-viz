import json
import requests
import re
import time
from datetime import datetime
from urllib.parse import unquote

HEADERS = {
    'User-Agent': 'ComposerTimelineBot/1.0 (test@example.com)' 
}

def get_wiki_search(query):
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "opensearch",
            "search": query,
            "limit": 1,
            "namespace": 0,
            "format": "json"
        }
        response = requests.get(url, params=params, headers=HEADERS)
        data = response.json()
        if data[3]:
            return data[3][0] 
        return None
    except Exception as e:
        print(f"Search error for {query}: {e}")
        return None

def get_wiki_content(url):
    try:
        # Decode URL to handle proper titles
        title = unquote(url.split("/")[-1])
        api_url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "format": "json",
            "prop": "revisions",
            "titles": title,
            "rvprop": "content",
            "redirects": 1
        }
        
        response = requests.get(api_url, params=params, headers=HEADERS)
        data = response.json()
        
        page_dict = data['query']['pages']
        # page_dict keys are page_ids, usually just one
        page = next(iter(page_dict.values()))
        
        if 'revisions' in page:
            return page['revisions'][0]['*']
        return ""
    except Exception as e:
        print(f"Error fetching content for {url}: {e}")
        return None

def format_date(year, month, day):
    try:
        d = datetime(int(year), int(month), int(day))
        return d.strftime("%B %-d, %Y")
    except ValueError:
        return None

def parse_template_args(template_str):
    inner = template_str.strip('{}')
    # Use split but be careful of nested templates? Dates usually simplistic.
    parts = inner.split('|')
    args = parts[1:]
    
    positional_digits = []
    
    for arg in args:
        arg = arg.strip()
        if '=' not in arg:
            if arg.isdigit():
                positional_digits.append(arg)
    
    # Typically Y/M/D order in birth/death templates
    if len(positional_digits) >= 3:
        y, m, d = positional_digits[0], positional_digits[1], positional_digits[2]
        if int(y) > 1000 and 1 <= int(m) <= 12 and 1 <= int(d) <= 31:
            return format_date(y, m, d)
            
    return None

def extract_date_from_template_robust(text, template_type):
    keywords = []
    if template_type == 'birth':
        keywords = ['birth date', 'bda', 'dob', 'birth_date']
    else:
        keywords = ['death date', 'dda', 'dod', 'death_date']
        
    regex = r'\{\{(' + '|'.join(keywords) + r')[^}]*\}\}'
    matches = re.finditer(regex, text, re.IGNORECASE)
    
    for match in matches:
        full_match = match.group(0)
        val = parse_template_args(full_match)
        if val:
            return val
            
    return None

def extract_date_from_infobox_text(text, param_name):
    # Fallback to text parsing
    match = re.search(fr'\|\s*{param_name}\s*=\s*(.*?)(?:\n\||\}})', text, re.IGNORECASE | re.DOTALL)
    if match:
        val = match.group(1).strip()
        val = re.sub(r'<ref.*?>.*?</ref>', '', val, flags=re.DOTALL)
        val = re.sub(r'<ref.*?>', '', val)
        val = re.sub(r'<!--.*?-->', '', val, flags=re.DOTALL)
        
        # d B Y (22 July 1980)
        dmy = re.search(r'\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b', val)
        if dmy:
            try:
                d = datetime.strptime(f"{dmy.group(1)} {dmy.group(2)} {dmy.group(3)}", "%d %B %Y")
                return d.strftime("%B %-d, %Y")
            except:
                pass
        
        # B d, Y (July 22, 1980)
        mdy = re.search(r'\b([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})\b', val)
        if mdy:
            try:
                d = datetime.strptime(f"{mdy.group(1)} {mdy.group(2)} {mdy.group(3)}", "%B %d %Y")
                return d.strftime("%B %-d, %Y")
            except:
                pass
                
    return None

def main():
    with open('Film Composers/data/Film Composers list.json', 'r') as f:
        composers = json.load(f)

    results = []
    
    print(f"Processing {len(composers)} composers...")

    for i, composer in enumerate(composers):
        print(f"[{i+1}/{len(composers)}] Processing {composer}...")
        
        wiki_url = get_wiki_search(composer) 
        # Note: Removing "film composer" context because explicit search is better for names like "Miklós Rózsa" 
        # which might be unique enough. 
        # But for common names like "John Williams", we need to be careful?
        # John Williams defaults to the composer usually or disambig page.
        # Let's try with raw name first, fallback to context if url is missing.
        
        if not wiki_url:
            wiki_url = get_wiki_search(composer + " (composer)") # specific
        
        birth_formatted = None
        death_formatted = "-"
        
        if wiki_url:
            content = get_wiki_content(wiki_url)
            
            if content:
                birth_formatted = extract_date_from_template_robust(content, 'birth')
                if not birth_formatted:
                     birth_formatted = extract_date_from_infobox_text(content, 'birth_date')

                death_val = extract_date_from_template_robust(content, 'death')
                if death_val:
                    death_formatted = death_val
                else:
                    d_text = extract_date_from_infobox_text(content, 'death_date')
                    if d_text:
                        death_formatted = d_text
        
        # Tangerine Dream specific override if still null
        if composer == "Tangerine Dream":
             # Still no valid full date, so leave as None or handle manually?
             # User said invalid if not MDY.
             pass

        if not birth_formatted:
             print(f"WARNING: No birth date found for {composer}")
             
        results.append({
            "composer": composer,
            "birth": birth_formatted,
            "death": death_formatted
        })
        
        # time.sleep(0.3)

    with open('Film Composers/data/composer_lifespans.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Done! Saved.")

if __name__ == "__main__":
    main()

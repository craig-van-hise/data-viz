import json
import requests
import re
import time
from datetime import datetime

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
        title = url.split("/")[-1]
        api_url = "https://en.wikipedia.org/w/api.php"
        
        # Get raw wikitext
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
        
        page = next(iter(data['query']['pages'].values()))
        if 'revisions' in page:
            return page['revisions'][0]['*']
        return ""
    except Exception as e:
        print(f"Error fetching content for {url}: {e}")
        return None

def format_date(year, month, day):
    # Ensure year, month, day are integers
    try:
        d = datetime(int(year), int(month), int(day))
        return d.strftime("%B %-d, %Y") # e.g. January 1, 1980 (on non-windows use %-d for no leading zero)
    except ValueError:
        return None

def extract_date_from_template(text, template_type):
    # Regex to find templates like {{Birth date|1980|1|1}} or {{Death date and age|2020|1|1|1980|1|1}}
    # template_type e.g. "Birth date" matches "Birth date", "Birth date and age", "bda", etc.
    
    # Common birth templates: Birth date, Birth date and age, bda, dob
    # Common death templates: Death date, Death date and age, dda, dod
    
    patterns = []
    if template_type == 'birth':
        patterns = [
            r'\{\{Birth date and age\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{Birth date\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{bda\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{birth date and age\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{birth date\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'birth_date\s*=\s*\{\{start date\|(\d{4})\|(\d{1,2})\|(\d{1,2})' # Infobox parameter
        ]
    elif template_type == 'death':
        patterns = [
            r'\{\{Death date and age\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{Death date\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{dda\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{death date and age\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
            r'\{\{death date\|(\d{4})\|(\d{1,2})\|(\d{1,2})',
             r'death_date\s*=\s*\{\{end date\|(\d{4})\|(\d{1,2})\|(\d{1,2})'
        ]

    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return format_date(match.group(1), match.group(2), match.group(3))
            
    return None

def extract_date_from_infobox_text(text, param_name):
    # Fallback: look for | birth_date = 22 July 1980
    # or | birth_date = {{birth date|1980|7|22}} which was handled above hopefully, but maybe not if embedded oddly
    
    # Find the parameter line
    # simple regex for | param = value
    match = re.search(fr'\|\s*{param_name}\s*=\s*(.*?)(?:\n\||\}})', text, re.IGNORECASE | re.DOTALL)
    if match:
        val = match.group(1).strip()
        # Remove refs <ref>...</ref>
        val = re.sub(r'<ref.*?>.*?</ref>', '', val, flags=re.DOTALL)
        val = re.sub(r'<ref.*?>', '', val) # unclosed refs
        
        # Look for Date Month Year or Month Date, Year in the value
        # 22 July 1980
        dmy = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', val)
        if dmy:
            # parsing month name to number is annoying without library, relying on datetime to parse
            try:
                d = datetime.strptime(f"{dmy.group(1)} {dmy.group(2)} {dmy.group(3)}", "%d %B %Y")
                return d.strftime("%B %-d, %Y")
            except:
                pass
                
        # July 22, 1980
        mdy = re.search(r'([A-Za-z]+)\s+(\d{1,2}),\s+(\d{4})', val)
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
        
        wiki_url = get_wiki_search(composer + " film composer")
        if not wiki_url:
             wiki_url = get_wiki_search(composer + " composer")
        if not wiki_url:
            wiki_url = get_wiki_search(composer)
            
        birth_formatted = None
        death_formatted = "-" # Default to alive
        
        if wiki_url:
            content = get_wiki_content(wiki_url)
            
            if content:
                # 1. Try Templates
                birth_formatted = extract_date_from_template(content, 'birth')
                
                # 2. Try Infobox Text Fallback if no template
                if not birth_formatted:
                     birth_formatted = extract_date_from_infobox_text(content, 'birth_date')
                
                # Death
                death_val = extract_date_from_template(content, 'death')
                if death_val:
                    death_formatted = death_val
                else:
                    # Check infobox text for death
                    d_text = extract_date_from_infobox_text(content, 'death_date')
                    if d_text:
                        death_formatted = d_text
                    else:
                        # If no death date found, check if they are "died" in text?
                        # If we have a birth date but the person is 120 years old, maybe suspicious.
                        # But for now, if no death date found, assume alive as per instructions.
                        pass
        
        if not birth_formatted:
             print(f"WARNING: No birth date found for {composer}")
             
        results.append({
            "composer": composer,
            "birth": birth_formatted,
            "death": death_formatted
        })
        
        # time.sleep(0.5)

    with open('Film Composers/data/composer_lifespans.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Done! Saved to Film Composers/data/composer_lifespans.json")

if __name__ == "__main__":
    main()

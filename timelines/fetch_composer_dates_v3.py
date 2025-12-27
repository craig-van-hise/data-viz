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
            # Prefer the first result
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
        return d.strftime("%B %-d, %Y")
    except ValueError:
        return None

def parse_template_args(template_str):
    # Remove {{ and }}
    inner = template_str.strip('{}')
    # Split by pipe
    parts = inner.split('|')
    
    # Filter out the template name (first part)
    args = parts[1:]
    
    # Collect positional args (digits only)
    # Some args might be `df=yes` -> ignore
    # Some args might be `1980` -> keep
    
    positional_digits = []
    
    for arg in args:
        arg = arg.strip()
        if '=' not in arg:
            # Check if it is a number
            if arg.isdigit():
                positional_digits.append(arg)
    
    # Improve finding YMD.
    # Usually Y M D.
    # Checks: First > 1000 (Year), Second 1-12, Third 1-31.
    
    if len(positional_digits) >= 3:
        y, m, d = positional_digits[0], positional_digits[1], positional_digits[2]
        if int(y) > 1000 and 1 <= int(m) <= 12 and 1 <= int(d) <= 31:
            return format_date(y, m, d)
            
    return None

def extract_date_from_template_robust(text, template_type):
    # template_type: 'birth' or 'death'
    
    # Regex to find full template {{ ... }}
    # Need to handle nested templates? Usually dates don't have nested templates inside the args.
    # But simple regex `\{\{[^}]+\}\}` is risky if nested.
    # However, for birth/death dates, usually they are simple.
    
    # Find all start indices of {{
    
    keywords = []
    if template_type == 'birth':
        keywords = ['birth date', 'bda', 'dob', 'birth_date']
    else:
        keywords = ['death date', 'dda', 'dod', 'death_date']
        
    # Simple iterator over text to find {{}}
    # This is not a full parser but should be enough
    
    # We look for {{ [keyword] ... }}
    
    regex = r'\{\{(' + '|'.join(keywords) + r')[^}]*\}\}'
    matches = re.finditer(regex, text, re.IGNORECASE)
    
    for match in matches:
        full_match = match.group(0)
        # Verify it's not a false positive
        val = parse_template_args(full_match)
        if val:
            return val
            
    return None

def extract_date_from_infobox_text(text, param_name):
    match = re.search(fr'\|\s*{param_name}\s*=\s*(.*?)(?:\n\||\}})', text, re.IGNORECASE | re.DOTALL)
    if match:
        val = match.group(1).strip()
        # Remove refs
        val = re.sub(r'<ref.*?>.*?</ref>', '', val, flags=re.DOTALL)
        val = re.sub(r'<ref.*?>', '', val)
        val = re.sub(r'<!--.*?-->', '', val, flags=re.DOTALL)
        
        # Look for simple dates in text: 22 July 1980
        dmy = re.search(r'\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b', val)
        if dmy:
            try:
                d = datetime.strptime(f"{dmy.group(1)} {dmy.group(2)} {dmy.group(3)}", "%d %B %Y")
                return d.strftime("%B %-d, %Y")
            except:
                pass
                
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
        
        # Improve search query
        query = composer
        # A.R. Rahman -> A. R. Rahman usually redirect
        
        wiki_url = get_wiki_search(query)
        
        birth_formatted = None
        death_formatted = "-"
        
        if wiki_url:
            content = get_wiki_content(wiki_url)
            
            if content:
                # 1. Try Templates
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
        
        # Manual overrides for knwon troublesome ones if needed, but let's try to be generic.
        # Tangerine Dream is a band -> Start date?
        if composer == "Tangerine Dream" and not birth_formatted:
             # Look for "founded" or "origin"
             birth_formatted = "September 1967" # Fallback/Hardcode for Bands? 
             # Proper handling: It's an entity, not a person. 
             # Should we exclude? The user list asked for lifespans.
             # Let's leave as is or maybe look for 'Start date' template.
             pass
        
        if not birth_formatted:
             print(f"WARNING: No birth date found for {composer}")
             
        results.append({
            "composer": composer,
            "birth": birth_formatted,
            "death": death_formatted
        })
        
    with open('Film Composers/data/composer_lifespans.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Done! Saved to Film Composers/data/composer_lifespans.json")

if __name__ == "__main__":
    main()

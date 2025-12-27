import json
import requests
import re
import time

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
            return data[3][0] # Return the URL
        return None
    except Exception as e:
        print(f"Search error for {query}: {e}")
        return None

def get_composer_data_from_api(url):
    try:
        title = url.split("/")[-1]
        api_url = "https://en.wikipedia.org/w/api.php"
        
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "titles": title,
            "exintro": True,
            "explaintext": True,
            "redirects": 1
        }
        
        response = requests.get(api_url, params=params, headers=HEADERS)
        data = response.json()
        
        page = next(iter(data['query']['pages'].values()))
        extract = page.get('extract', '')
        
        return extract
    except Exception as e:
        return None

def simple_date_extract(text):
    birth = None
    death = None
    
    # Regex patterns for dates
    # 1. Month Day, Year (e.g. January 1, 1900)
    mdy_pattern = r'[A-Z][a-z]+\s+\d{1,2},\s+\d{4}'
    # 2. Day Month Year (e.g. 1 January 1900)
    dmy_pattern = r'\d{1,2}\s+[A-Z][a-z]+\s+\d{4}'
    
    date_pattern = f"({mdy_pattern}|{dmy_pattern})"
    
    # Check for "born [Date]"
    born_match = re.search(fr'born\s+{date_pattern}', text)
    if born_match:
        birth = born_match.group(1)
            
    # Check for "died [Date]"
    died_match = re.search(fr'died\s+{date_pattern}', text)
    if died_match:
        death = died_match.group(1)
        
    # Check for range (Date – Date) often in parentheses
    if not birth or not death:
        # Look for content in first parentheses
        paren_match = re.search(r'\(([^)]+)\)', text)
        if paren_match:
            content = paren_match.group(1)
            
            # Remove "born" suffix if present to avoid confusion
            
            # Check for full date range: Date – Date
            # Note: Wikipedia uses en-dash usually, but sometimes hyphen
            range_match = re.search(fr'{date_pattern}\s*[–-]\s*{date_pattern}', content)
            if range_match:
                # Groups: 1 is birth date, 2 is (mdy|dmy) inside group 1... wait
                # Because date_pattern has a group, this is tricky. Re.findall might be better on the content.
                dates = re.findall(date_pattern, content)
                if len(dates) >= 2:
                    birth = dates[0][0] # findall returns matching groups, so tuple. 
                    death = dates[1][0]
            
            # Check for range: Date – Place (means died there?) No.
            # Check for Year-Year
            if not birth and not death:
                 year_range = re.search(r'(\d{4})\s*[–-]\s*(\d{4})', content)
                 if year_range:
                     birth = year_range.group(1)
                     death = year_range.group(2)
            
            # Check for "born Date" or "b. Date"
            if not birth:
                b_match = re.search(fr'(?:born|b\.)\s+{date_pattern}', content)
                if b_match:
                    birth = b_match.group(1)
                else:
                    # just Year
                    b_year = re.search(r'(?:born|b\.)\s+(\d{4})', content)
                    if b_year:
                        birth = b_year.group(1)
                        
            # Check for "died Date" or "d. Date"
            if not death:
                d_match = re.search(fr'(?:died|d\.)\s+{date_pattern}', content)
                if d_match:
                    death = d_match.group(1)
                else:
                     d_year = re.search(r'(?:died|d\.)\s+(\d{4})', content)
                     if d_year:
                         death = d_year.group(1)

    # Fallback: if only birth year found, and text says "is a ... composer" implies alive.
    # If text says "was a ... composer", implies dead.
    
    return birth, death

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
            
        if wiki_url:
            extract = get_composer_data_from_api(wiki_url)
            if extract:
                birth, death = simple_date_extract(extract)
                results.append({
                    "composer": composer,
                    "birth": birth,
                    "death": death
                })
            else:
                 results.append({"composer": composer, "birth": None, "death": None})
        else:
            results.append({"composer": composer, "birth": None, "death": None})
        
        # time.sleep(0.5) # slightly faster but still safe

    with open('Film Composers/data/composer_lifespans.json', 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Done!")

if __name__ == "__main__":
    main()

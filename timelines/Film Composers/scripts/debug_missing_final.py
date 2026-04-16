import requests
import json
from urllib.parse import unquote
import re

HEADERS = {
    'User-Agent': 'ComposerTimelineBot/1.0 (test@example.com)' 
}

def debug_wikitext(name):
    # Try exact search first
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": name,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    response = requests.get(url, params=params, headers=HEADERS)
    data = response.json()
    if not data[3]:
        print(f"No URL for {name}")
        return

    wiki_url = data[3][0]
    title = unquote(wiki_url.split("/")[-1])
    print(f"\nFetching content for {title}...")
    
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": title,
        "rvprop": "content",
        "redirects": 1
    }
    
    response = requests.get(url, params=params, headers=HEADERS)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    
    if 'revisions' not in page:
        print("No revisions.")
        return

    content = page['revisions'][0]['*']
    
    print(f"--- Relevant Lines for {name} ---")
    
    # Check if Infobox exists
    if "Infobox" in content:
        print("Infobox found.")
        
    # Print lines with 'birth' or 'born'
    for line in content.split('\n'):
        if 'birth' in line.lower() or 'born' in line.lower():
            if len(line) < 200: # limit noise
                print(line)

targets = [
    "Dario Marianelli",
    "John Barry",
    "John Powell",
    "Malcolm Arnold",
    "Michael Nyman",
    "Roy Webb",
    "Tangerine Dream",
    "Trevor Jones"
]

for t in targets:
    debug_wikitext(t)

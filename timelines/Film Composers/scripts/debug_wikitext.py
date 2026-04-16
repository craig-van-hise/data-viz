import requests
import json
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
        print(f"No URL for {name} via opensearch")
        return

    wiki_url = data[3][0]
    title = wiki_url.split("/")[-1]
    print(f"Fetching content for {title}...")
    
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
    content = page['revisions'][0]['*']
    
    print(f"--- Content Start for {name} ---")
    print(content[:3000])
    print(f"--- Content End for {name} ---")

debug_wikitext("Bronislaw Kaper")
debug_wikitext("Miklós Rózsa")

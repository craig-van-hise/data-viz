import requests
import json
from urllib.parse import unquote

HEADERS = {
    'User-Agent': 'ComposerTimelineBot/1.0 (test@example.com)' 
}

def debug_missing(name):
    print(f"DEBUGGING: {name}")
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
        print("No URL found")
        return

    wiki_url = data[3][0]
    print(f"URL: {wiki_url}")
    # Fix: Decode the URL component
    title = unquote(wiki_url.split("/")[-1])
    print(f"Title: {title}")
    
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
        print("Still no revisions found.")
        return

    content = page['revisions'][0]['*']
    
    print("--- Relevant Lines ---")
    for line in content.split('\n'):
        if 'birth' in line.lower() or 'born' in line.lower() or 'died' in line.lower() or 'death' in line.lower():
            print(line)

debug_missing("Bronislaw Kaper")
debug_missing("Miklós Rózsa")

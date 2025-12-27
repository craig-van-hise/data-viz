import requests
import json

HEADERS = {
    'User-Agent': 'ComposerTimelineBot/1.0 (test@example.com)' 
}

def debug_composer(name):
    # Search
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": name,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    response = requests.get(url, params=params, headers=HEADERS)
    print(f"Search response for {name}: {response.text}")
    data = response.json()
    if not data[3]:
        print("No URL found")
        return

    wiki_url = data[3][0]
    print(f"URL: {wiki_url}")
    title = wiki_url.split("/")[-1]
    
    # Query
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "exintro": True,
        "explaintext": True,
        "redirects": 1
    }
    
    response = requests.get(url, params=params, headers=HEADERS)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    extract = page.get('extract', '')
    print(f"Extract:\n{extract}")

debug_composer("Ennio Morricone")

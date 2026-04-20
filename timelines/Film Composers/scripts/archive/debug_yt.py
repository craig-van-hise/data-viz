import requests
import re
import urllib.parse

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

def get_yt_direct(title, composer):
    query = f"{title} {composer} main theme suite"
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}"
    
    print(f"URL: {url}")
    
    try:
        # We need cookies to look like a real human? sometimes.
        # Let's try raw first.
        res = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {res.status_code}")
        
        # Regex for video ID
        # "videoId":"VIDEO_ID" is common in ytInitialData
        # or /watch?v=VIDEO_ID
        
        # Look for the first "videoId":"..."
        video_ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', res.text)
        
        if video_ids:
            # Filter out duplicates while preserving order
            unique = []
            for v in video_ids:
                if v not in unique:
                    unique.append(v)
            
            print(f"Found IDs: {unique[:3]}") # Show first 3
            return f"https://www.youtube.com/watch?v={unique[0]}"
            
    except Exception as e:
        print(f"Error: {e}")
        
    return None

link = get_yt_direct("The Little Mermaid", "Alan Menken")
print(f"Result: {link}")

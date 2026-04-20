import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

query = "The Little Mermaid Alan Menken theme suite site:youtube.com"
ddg_url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"

print(f"Query URL: {ddg_url}")

res = requests.get(ddg_url, headers=headers)
print(f"Status: {res.status_code}")

with open("debug_ddg.html", "w") as f:
    f.write(res.text)

soup = BeautifulSoup(res.text, 'html.parser')
links = soup.find_all('a', class_='result__a')
print(f"Found {len(links)} result links.")

for a in links:
    print(f"Href: {a.get('href')}")

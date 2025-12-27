import json
from collections import defaultdict

with open('Film Composers/data/Most important films.json', 'r') as f:
    data = json.load(f)

print("Searching for composers with multiple films in the same year...")

for composer in data:
    name = composer['composer']
    films_by_year = defaultdict(list)
    
    for film in composer['films']:
        title = film['title']
        date = film['release_date']
        year = date.split('-')[0]
        films_by_year[year].append((title, date))
        
    for year, films in films_by_year.items():
        if len(films) > 1:
            print(f"\n{name} ({year}):")
            for title, date in films:
                print(f"  - {title} ({date})")

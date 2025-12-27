import json
import os

base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
json_path = os.path.join(base_dir, "data/Most important films.json")

new_films = [
    {
        "title": "Double Indemnity",
        "release_date": "1944-07-03",
        "youtube_link": "https://www.youtube.com/watch?v=fJkI0-9yWzQ"
    },
    {
        "title": "The Killers",
        "release_date": "1946-08-30",
        "youtube_link": "https://www.youtube.com/watch?v=K-n9ENt3mf6"
    },
    {
        "title": "Quo Vadis",
        "release_date": "1951-11-02",
        "youtube_link": "https://www.youtube.com/watch?v=s-iUJkoC0Cs"
    },
    {
        "title": "El Cid",
        "release_date": "1961-12-14",
        "youtube_link": "https://www.youtube.com/watch?v=FqjRM_MK7Zq"
    },
    {
        "title": "King of Kings",
        "release_date": "1961-10-11",
        "youtube_link": "https://www.youtube.com/watch?v=5T1Je62QsUO"
    },
    {
        "title": "The Thief of Bagdad",
        "release_date": "1940-12-25",
        "youtube_link": "https://www.youtube.com/watch?v=EtGRJ6z5Np"
    },
    {
        "title": "The Jungle Book",
        "release_date": "1942-04-03",
        "youtube_link": "https://www.youtube.com/watch?v=4uN0-_2riH"
    }
]

with open(json_path, 'r') as f:
    data = json.load(f)

rozsa_found = False
for composer in data:
    if composer['composer'] == "Miklós Rózsa":
        rozsa_found = True
        print("Found Miklós Rózsa.")
        existing_titles = [f['title'] for f in composer['films']]
        
        for film in new_films:
            if film['title'] not in existing_titles:
                print(f"Adding {film['title']}")
                composer['films'].append(film)
            else:
                print(f"Skipping {film['title']} (already exists)")
        
        # Sort films by release date
        composer['films'].sort(key=lambda x: x['release_date'])
        break

if not rozsa_found:
    print("Miklós Rózsa not found in JSON!")

with open(json_path, 'w') as f:
    json.dump(data, f, indent=4)

print("JSON updated.")

import os
import json
import time
import requests
from dotenv import load_dotenv
from urllib.parse import quote

# 1. Setup paths relative to script location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
COMPOSERS_LIST_PATH = os.path.join(PROJECT_ROOT, "data/Film Composers list.json")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data/filmographies")

# 2. Authentication
load_dotenv(ENV_PATH)
token = os.getenv("TMDB_API_READ_ACCESS_TOKEN")

if not token:
    print(f"Error: TMDB_API_READ_ACCESS_TOKEN not found in {ENV_PATH}")
    # Fallback to root .env if not found
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(PROJECT_ROOT)), ".env"))
    token = os.getenv("TMDB_API_READ_ACCESS_TOKEN")
    if not token:
        exit(1)

HEADERS = {
    "Authorization": f"Bearer {token}",
    "accept": "application/json"
}

# 3. Data Source
with open(COMPOSERS_LIST_PATH, 'r') as f:
    composers = json.load(f)

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 4. Execution Loop
for i, composer in enumerate(composers):
    print(f"[{i+1}/{len(composers)}] Processing {composer}...")
    
    # Step A (Find ID)
    search_url = f"https://api.themoviedb.org/3/search/person?query={quote(composer)}&include_adult=false"
    try:
        search_response = requests.get(search_url, headers=HEADERS)
        search_data = search_response.json()
        
        if not search_data.get("results"):
            print(f"  ⚠️ Warning: No results found for {composer}")
            continue
            
        person_id = search_data["results"][0]["id"]
        
        # Step B (Get Credits)
        credits_url = f"https://api.themoviedb.org/3/person/{person_id}?append_to_response=movie_credits&language=en-US"
        credits_response = requests.get(credits_url, headers=HEADERS)
        credits_data = credits_response.json()
        
        # Step C (Filter)
        crew = credits_data.get("movie_credits", {}).get("crew", [])
        filtered_credits = [
            item for item in crew 
            if item.get("department") == "Sound" and item.get("job") == "Original Music Composer"
        ]
        
        # Step D (Format)
        formatted_list = []
        for film in filtered_credits:
            # Parse Year
            release_date = film.get("release_date", "")
            year = release_date.split("-")[0] if release_date else "9999"
            if not year.isdigit():
                year = "9999"
                
            formatted_list.append({
                "title": film.get("title"),
                "year": year,
                "id": film.get("id"),
                "poster": f"https://image.tmdb.org/t/p/w200{film.get('poster_path')}" if film.get("poster_path") else None
            })
            
        # Step E (Clean & Sort)
        # Deduplicate by id
        seen_ids = set()
        deduped_list = []
        for film in formatted_list:
            if film["id"] not in seen_ids:
                deduped_list.append(film)
                seen_ids.add(film["id"])
        
        # Sort by year
        deduped_list.sort(key=lambda x: x["year"])
        
        # Step F (Save)
        safe_name = composer.replace(" ", "_")
        output_file = os.path.join(OUTPUT_DIR, f"{safe_name}.json")
        
        # Load existing data to preserve youtube_links
        existing_yt_links = {}
        if os.path.exists(output_file):
            try:
                with open(output_file, 'r') as f:
                    old_data = json.load(f)
                    for film in old_data:
                        if "youtube_link" in film:
                            existing_yt_links[film["title"]] = film["youtube_link"]
            except Exception as e:
                print(f"  ⚠️ Could not read existing file {output_file}: {e}")

        # Inject existing youtube_links
        for film in deduped_list:
            if film["title"] in existing_yt_links:
                film["youtube_link"] = existing_yt_links[film["title"]]
        
        with open(output_file, 'w') as f:
            json.dump(deduped_list, f, indent=4)
            
        print(f"  ✅ Saved {len(deduped_list)} films to {safe_name}.json (Preserved {len(existing_yt_links)} YT links)")
        
    except Exception as e:
        print(f"  ❌ Error processing {composer}: {e}")
        
    # Step G (Rate Limiting)
    time.sleep(0.3)

print("\n🚀 Rebuild complete!")

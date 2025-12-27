import json
import os
import re

# Same sanitization logic as JS
def sanitize_filename(title):
    # "Star Wars: Episode IV - A New Hope" -> Remove quotes, dots, dashes. Replace colon with space.
    s = re.sub(r"['\".\-]", "", title)
    s = s.replace(":", " ")
    return s.strip()

base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
json_path = os.path.join(base_dir, "data/Most important films.json")
thumb_base = os.path.join(base_dir, "thumbnails")

with open(json_path, 'r') as f:
    data = json.load(f)

missing = []

print("Checking for missing thumbnails...")

for entry in data:
    composer = entry['composer']
    for film in entry['films']:
        title = film['title']
        safe_title = sanitize_filename(title)
        
        # Check jpg
        thumb_path = os.path.join(thumb_base, composer, safe_title + ".jpg")
        
        if not os.path.exists(thumb_path):
            missing.append({
                "composer": composer,
                "title": title,
                "safe_title": safe_title,
                "expected_path": thumb_path
            })

print(f"Total missing: {len(missing)}")
for m in missing:
    print(f"MISSING: {m['composer']} - {m['title']} -> Expected: {m['safe_title']}.jpg")

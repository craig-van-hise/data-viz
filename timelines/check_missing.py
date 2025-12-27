import json

with open('Film Composers/data/composer_lifespans.json', 'r') as f:
    data = json.load(f)

missing = []
for entry in data:
    if not entry.get('birth'):
        missing.append(entry['composer'])

print(f"Found {len(missing)} missing birth dates:")
for m in missing:
    print(m)

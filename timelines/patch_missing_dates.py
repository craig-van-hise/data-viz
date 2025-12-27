import json

corrections = {
    "Dario Marianelli": {"birth": "June 21, 1963", "death": "-"},
    "John Barry": {"birth": "November 3, 1933", "death": "January 30, 2011"},
    "John Powell": {"birth": "September 18, 1963", "death": "-"},
    "Malcolm Arnold": {"birth": "October 21, 1921", "death": "September 23, 2006"},
    "Michael Nyman": {"birth": "March 23, 1944", "death": "-"},
    "Roy Webb": {"birth": "October 3, 1888", "death": "December 10, 1982"},
    "Tangerine Dream": {"birth": "September 29, 1967", "death": "-"},
    "Trevor Jones": {"birth": "March 23, 1949", "death": "-"}
}

file_path = 'Film Composers/data/composer_lifespans.json'

with open(file_path, 'r') as f:
    data = json.load(f)

for entry in data:
    name = entry['composer']
    if name in corrections:
        print(f"Patching {name}...")
        entry['birth'] = corrections[name]['birth']
        entry['death'] = corrections[name]['death']

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print("Patch complete.")

import json
import re

with open('Film Composers/data/composer_lifespans.json', 'r') as f:
    data = json.load(f)

# Regex for Month Day, Year
# e.g. January 1, 1980
# Simple regex: starts with Upper, word, space, digits, comma, space, 4 digits.
date_regex = re.compile(r'^[A-Z][a-z]+ \d{1,2}, \d{4}$')

errors = 0
for entry in data:
    name = entry['composer']
    birth = entry.get('birth')
    death = entry.get('death')
    
    if not birth:
        print(f"ERROR: {name} has missing birth date.")
        errors += 1
    elif not date_regex.match(birth):
        print(f"ERROR: {name} has invalid birth date format: '{birth}'")
        errors += 1
        
    if not death:
        print(f"ERROR: {name} has missing death date field.")
        errors += 1
    elif death != "-":
        if not date_regex.match(death):
            print(f"ERROR: {name} has invalid death date format: '{death}'")
            errors += 1

if errors == 0:
    print("SUCCESS: All entries are valid.")
else:
    print(f"FAILED: Found {errors} errors.")

import json
from datetime import datetime

def convert_date(date_str):
    if not date_str or date_str == "-":
        return date_str
    try:
        # Parse "Month Day, Year"
        dt = datetime.strptime(date_str, "%B %d, %Y")
        # Format to "MM/DD/YYYY"
        return dt.strftime("%m/%d/%Y")
    except ValueError:
        return date_str

file_path = 'Film Composers/data/composer_lifespans.json'

with open(file_path, 'r') as f:
    data = json.load(f)

for entry in data:
    entry['birth'] = convert_date(entry['birth'])
    entry['death'] = convert_date(entry['death'])

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print("Date conversion complete.")

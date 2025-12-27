import json
import os
import re

base_dir = "/Users/vv2024/Documents/AI Projects/Timelines/Film Composers"
html_path = os.path.join(base_dir, "composers.html")
json_path = os.path.join(base_dir, "data/Most important films.json")

# 1. Read Data
with open(json_path, 'r') as f:
    json_content = f.read()

with open(html_path, 'r') as f:
    html_content = f.read()

# 2. Replace filmData
# Pattern: var filmData = [ ... ];
# We use DOTALL to match newlines
# Locate start index
start_marker = "var filmData = ["
end_marker = "];"
start_idx = html_content.find(start_marker)

if start_idx != -1:
    # Find the matching closing bracket for this variable
    # A simple find("];", start_idx) might be safe enough if the JSON is valid
    end_idx = html_content.find(end_marker, start_idx)
    if end_idx != -1:
        new_data_block = "var filmData = " + json_content + ";"
        
        # Check integrity
        print(f"Replacing block from {start_idx} to {end_idx+2}")
        
        pre = html_content[:start_idx]
        post = html_content[end_idx+2:]
        html_content = pre + new_data_block + post
    else:
        print("Could not find end of filmData block")
else:
    print("Could not find start of filmData block")

# 3. Inject Click Handler
# We look for: marker.className = 'film-marker';
# And inject the click logic after setting the style.left
# Target: marker.className = 'film-marker';
#         marker.style.left = `${filmPct}%`;

search_str = "marker.style.left = `${filmPct}%`;"
injection = """
                            // Click to YouTube
                            if (film.youtube_link) {
                                marker.style.cursor = 'pointer';
                                marker.setAttribute('onclick', `window.open('${film.youtube_link}', '_blank')`);
                            }
"""

if search_str in html_content:
    if "if (film.youtube_link)" not in html_content:
        html_content = html_content.replace(search_str, search_str + injection)
        print("Injected click handler.")
    else:
        print("Click handler already present.")
else:
    print("Could not find marker styling line")

# 4. Bump Version
# 4. Bump Version
# v1.13 -> v1.14
if "(v1.13)" in html_content:
    html_content = html_content.replace("(v1.13)", "(v1.14)")
    print("Bumped version to v1.14")

# 5. Save
with open(html_path, 'w') as f:
    f.write(html_content)

print("HTML updated successfully.")

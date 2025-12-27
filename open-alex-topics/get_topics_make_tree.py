import requests
import json
import time

def fetch_and_build_tree():
    # --- CONFIGURATION ---
    # Add your email here to join the "polite pool" (faster, less likely to fail)
    email = "your_email@example.com" 
    url = f"https://api.openalex.org/topics?mailto={email}"
    
    print("1. Starting download from OpenAlex...")
    
    # Storage for all topics
    flat_topics = []
    
    # Pagination loop
    params = {"per-page": 100, "cursor": "*"}
    page_count = 0
    
    while True:
        try:
            response = requests.get(url, params=params)
            
            # Check if the API request was successful
            if response.status_code != 200:
                print(f"Error: API returned status code {response.status_code}")
                print(response.text)
                break
                
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                break
                
            flat_topics.extend(results)
            
            # Update cursor
            params['cursor'] = data['meta']['next_cursor']
            
            page_count += 1
            if page_count % 5 == 0:
                print(f"   Downloaded {len(flat_topics)} topics so far...")
                
            if not params['cursor']:
                break
                
            time.sleep(0.1) # Be polite to the server
            
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            break

    total_topics = len(flat_topics)
    print(f"2. Download finished. Total topics found: {total_topics}")

    if total_topics == 0:
        print("STOPPING: No data was downloaded. Check your internet connection or API URL.")
        return

    # 3. Build the Hierarchy
    print("3. constructing hierarchy...")
    tree_structure = {}
    meta_lookup = {} 

    for t in flat_topics:
        try:
            # Safely extract IDs (convert to string to be safe)
            d_id = str(t['domain']['id'])
            f_id = str(t['field']['id'])
            s_id = str(t['subfield']['id'])
            
            # Store names
            meta_lookup[d_id] = t['domain']['display_name']
            meta_lookup[f_id] = t['field']['display_name']
            meta_lookup[s_id] = t['subfield']['display_name']
            
            # Initialize dicts if missing
            if d_id not in tree_structure: tree_structure[d_id] = {}
            if f_id not in tree_structure[d_id]: tree_structure[d_id][f_id] = {}
            if s_id not in tree_structure[d_id][f_id]: tree_structure[d_id][f_id][s_id] = []
            
            # Add Topic (Leaf)
            tree_structure[d_id][f_id][s_id].append({
                "name": t['display_name'],
                "value": t.get('works_count', 1), # Default to 1 if missing
                "id": t['id']
            })
        except KeyError as e:
            # Skip malformed records
            continue

    # 4. Convert to D3 "Flare" JSON
    final_tree = {"name": "All Science", "children": []}

    for d_id, fields in tree_structure.items():
        domain_node = {"name": meta_lookup[d_id], "children": []}
        
        for f_id, subfields in fields.items():
            field_node = {"name": meta_lookup[f_id], "children": []}
            
            for s_id, topics in subfields.items():
                subfield_node = {
                    "name": meta_lookup[s_id],
                    "children": topics 
                }
                field_node["children"].append(subfield_node)
            
            domain_node["children"].append(field_node)
        
        final_tree["children"].append(domain_node)

    # 5. Save
    output_file = 'openalex_tree.json'
    with open(output_file, 'w') as f:
        json.dump(final_tree, f)
    
    print(f"SUCCESS! Data saved to '{output_file}'. File size should be approx 1MB.")

if __name__ == "__main__":
    fetch_and_build_tree()
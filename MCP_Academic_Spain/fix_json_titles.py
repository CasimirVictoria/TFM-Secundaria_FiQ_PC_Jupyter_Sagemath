import os
import json
import re

articles_dir = "/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/articles_fulltext/"
bib_file = "/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/03.1.3_Notes_i_Esborranys/Bibliografia_STEAM.md"

def get_doi_title_map():
    mapping = {}
    with open(bib_file, 'r') as f:
        content = f.read()
    
    # Simple regex to find sections like ### Title and then Referència: ... doi.org/DOI
    sections = re.split(r'### ', content)
    for section in sections[1:]:
        lines = section.split('\n')
        title = lines[0].strip()
        # Find DOI in the section
        doi_match = re.search(r'doi\.org/([^\s\)]+)', section)
        if doi_match:
            doi = doi_match.group(1).lower().rstrip('.')
            mapping[doi] = title
            # Also mapping with underscores for easier lookup
            mapping[doi.replace('.', '_').replace('/', '_')] = title
    return mapping

def fix_titles():
    mapping = get_doi_title_map()
    print(f"Loaded {len(mapping)} DOI-Title mappings.")
    
    for filename in os.listdir(articles_dir):
        if filename.endswith(".json"):
            path = os.path.join(articles_dir, filename)
            with open(path, 'r') as f:
                try:
                    data = json.load(f)
                except:
                    continue
            
            if not data.get("title"):
                doi = data.get("doi", "").lower()
                # Try to match DOI or filename base
                base = filename[:-5].lower()
                title = mapping.get(doi) or mapping.get(base)
                
                if title:
                    data["title"] = title
                    with open(path, 'w') as f:
                        json.dump(data, f, indent=2)
                    print(f"Fixed title for {filename}: {title}")
                else:
                    print(f"No title found for {filename} (DOI: {doi})")

if __name__ == "__main__":
    fix_titles()

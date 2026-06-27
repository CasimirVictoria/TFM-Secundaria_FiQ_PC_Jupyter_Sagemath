import asyncio
import os
from server import SemanticScholarClient, RodericScraper
from dotenv import load_dotenv

# Load keys
load_dotenv(os.path.expanduser("~/.mcp_academic_keys"))

async def test_s2():
    query = "computational thinking AND education"
    s2 = SemanticScholarClient()
    roderic = RodericScraper()
    
    print(f"Buscant: {query}...\n")
    print(f"API Key detectada: {'Sí' if s2.api_key else 'No'}")
    
    tasks = [
        s2.search(query, limit=3),
        roderic.search(query, limit=3)
    ]
    
    results = await asyncio.gather(*tasks)
    s2_res, rod_res = results
    
    print(f"\n--- SEMANTIC SCHOLAR ({len(s2_res)}) ---")
    for r in s2_res:
        print(f"- {r['title']} ({r.get('year', 'N/A')})")
        print(f"  DOI: {r.get('doi', 'N/A')}")
        
    print(f"\n--- RODERIC UV ({len(rod_res)}) ---")
    for r in rod_res:
        print(f"- {r['title']} ({r.get('year', 'N/A')})")

if __name__ == "__main__":
    asyncio.run(test_s2())

import asyncio
import json
from server import WOSClient, RodericScraper, DialnetScraper

async def test_combined():
    query = "computational thinking AND education"
    wos = WOSClient()
    roderic = RodericScraper()
    dialnet = DialnetScraper()
    
    print(f"Buscant: {query}...\n")
    
    tasks = [
        wos.search(query, limit=3),
        roderic.search(query, limit=3),
        dialnet.search(query, limit=3)
    ]
    
    results = await asyncio.gather(*tasks)
    
    wos_res, rod_res, dial_res = results
    
    print(f"--- WEB OF SCIENCE ({len(wos_res)}) ---")
    for r in wos_res:
        print(f"- {r['title']} ({r.get('year', 'N/A')})")
        
    print(f"\n--- RODERIC UV ({len(rod_res)}) ---")
    for r in rod_res:
        print(f"- {r['title']} ({r.get('year', 'N/A')})")
        
    print(f"\n--- DIALNET ({len(dial_res)}) ---")
    for r in dial_res:
        print(f"- {r['title']} ({r.get('year', 'N/A')})")

if __name__ == "__main__":
    asyncio.run(test_combined())

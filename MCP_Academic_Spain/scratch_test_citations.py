import asyncio
from server import OpenAlexClient, SemanticScholarClient

async def test():
    oa = OpenAlexClient()
    ss = SemanticScholarClient()
    
    query = '"Computational Thinking" STEM Education'
    print(f"--- Searching for: {query} ---")
    results = await oa.search_works(query, limit=5)
    
    # Filter for a paper that actually mentions CT in title
    paper = None
    for r in results:
        if "Computational Thinking" in r.get("display_name", ""):
            paper = r
            break
    
    if not paper:
        paper = results[0]
    work_id = paper.get("doi") or paper.get("id")
    title = paper.get("display_name")
    
    print(f"\nFound Paper: {title}")
    print(f"ID: {work_id}")
    
    print("\n--- Testing get_citations ---")
    citations = await ss.get_citations(work_id, limit=3)
    for c in citations:
        print(f"- {c['title']} ({c['year']})")
        
    print("\n--- Testing get_references (SS) ---")
    references = await ss.get_references(work_id, limit=3)
    for r in references:
        print(f"- {r['title']} ({r['year']})")
        
    print("\n--- Testing get_references (OA) ---")
    references_oa = await oa.get_references(work_id, limit=3)
    for r in references_oa:
        print(f"- {r.get('display_name')} ({r.get('publication_year')})")

if __name__ == "__main__":
    asyncio.run(test())

import asyncio
import re
from server import OpenAlexClient, SemanticScholarClient, generate_mermaid_network

async def test_viz():
    oa = OpenAlexClient()
    ss = SemanticScholarClient()
    
    work_id = "https://doi.org/10.3102/0013189x12463051"
    limit = 3
    
    print(f"--- Testing Viz for: {work_id} ---")
    
    # Gather citations
    cites = await ss.get_citations(work_id, limit)
    if not cites:
        oa_cites = await oa.get_citations(work_id, limit)
        cites = [{"title": w.get("display_name"), "year": w.get("publication_year")} for w in oa_cites]
        
    # Gather references
    refs = await ss.get_references(work_id, limit)
    if not refs:
        oa_refs = await oa.get_references(work_id, limit)
        refs = [{"title": w.get("display_name"), "year": w.get("publication_year")} for w in oa_refs]
        
    # Try to get the root title
    root_title = "Article Principal"
    try:
        work_info = await oa.get_work(work_id)
        root_title = work_info.get("display_name", "Article Principal")
    except Exception as e: 
        print(f"Error getting work info: {e}")
    
    mermaid_cites = generate_mermaid_network(root_title, cites, "citations")
    print("\nMERMAID CITATIONS:")
    print(mermaid_cites)
    
    mermaid_refs = generate_mermaid_network(root_title, refs, "references")
    print("\nMERMAID REFERENCES:")
    print(mermaid_refs)

if __name__ == "__main__":
    asyncio.run(test_viz())

import asyncio
from server import ProcomunScraper, ScieloScraper, TeseoScraper, QueryExpander

async def test():
    query = "pensamiento computacional"
    
    print("--- Testing QueryExpander ---")
    qe = QueryExpander()
    print(qe.expand(query))
    
    print("\n--- Testing ProcomunScraper ---")
    pro = ProcomunScraper()
    res_pro = await pro.search(query, limit=2)
    print(f"Results: {res_pro}")
    
    print("\n--- Testing ScieloScraper ---")
    sci = ScieloScraper()
    res_sci = await sci.search(query, limit=2)
    print(f"Results: {res_sci}")
    
    print("\n--- Testing TeseoScraper ---")
    tes = TeseoScraper()
    res_tes = await tes.search(query, limit=2)
    print(f"Results: {res_tes}")

if __name__ == "__main__":
    asyncio.run(test())

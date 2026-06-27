import asyncio
from server import GVAScraper

async def test():
    query = "currículo secundaria"
    print(f"--- Testing GVAScraper for '{query}' ---")
    gva = GVAScraper()
    res = await gva.search(query, limit=3)
    print(f"Results: {res}")

if __name__ == "__main__":
    asyncio.run(test())

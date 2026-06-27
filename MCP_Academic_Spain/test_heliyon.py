import asyncio
import os
import sys
sys.path.append("/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/MCP_Academic_Spain")
from server import FulltextRetriever

async def test():
    # Try PMC URL
    res = await FulltextRetriever.retrieve_via_browser('https://pmc.ncbi.nlm.nih.gov/articles/PMC11031765/')
    if "text" in res:
        print(f"SUCCESS: {len(res['text'])} chars")
    else:
        print(f"FAIL: {res.get('error')}")

if __name__ == "__main__":
    asyncio.run(test())

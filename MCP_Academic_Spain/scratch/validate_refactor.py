import sys
import os
import asyncio
import logging
import urllib.parse

sys.path.append("/home/casimiro/Documentos/TFM/MCP_Academic_Spain")

async def run_test():
    from platforms import DialnetSearcher, OpenAlexSearcher, TDRSearcher, RedalycSearcher, CrossRefSearcher, EuropePMCSearcher
    
    SEARCHERS = {
        "dialnet": DialnetSearcher(),
        "openalex": OpenAlexSearcher(),
        "tdr": TDRSearcher(),
        "redalyc": RedalycSearcher(),
        "crossref": CrossRefSearcher(),
        "europepmc": EuropePMCSearcher()
    }
    
    print("Testing OpenAlex...")
    try:
        results = await SEARCHERS["openalex"].search("pensamiento computacional", limit=2)
        for p in results:
            print(f"Found: {p.title} [{p.source}]")
    except Exception as e:
        print(f"OpenAlex Error: {e}")
            
    print("\nTesting Dialnet...")
    try:
        results = await SEARCHERS["dialnet"].search("pensamiento computacional", limit=1)
        if not results:
            print("Dialnet returned no results.")
        for p in results:
            print(f"Found: {p.title} [{p.source}]")
    except Exception as e:
        print(f"Dialnet Error: {e}")

    print("\nTesting TDR...")
    try:
        results = await SEARCHERS["tdr"].search("robotica educativa", limit=1)
        for p in results:
            print(f"Found: {p.title} [{p.source}]")
    except Exception as e:
        print(f"TDR Error: {e}")

    print("\nTesting Redalyc...")
    try:
        results = await SEARCHERS["redalyc"].search("gamificacion", limit=1)
        for p in results:
            print(f"Found: {p.title} [{p.source}]")
    except Exception as e:
        print(f"Redalyc Error: {e}")

    print("\nTesting CrossRef...")
    try:
        results = await SEARCHERS["crossref"].search("computational thinking", limit=1)
        for p in results:
            print(f"Found: {p.title} [{p.source}]")
    except Exception as e:
        print(f"CrossRef Error: {e}")

    print("\nTesting EuropePMC...")
    try:
        results = await SEARCHERS["europepmc"].search("machine learning education", limit=1)
        for p in results:
            print(f"Found: {p.title} [{p.source}]")
    except Exception as e:
        print(f"EuropePMC Error: {e}")

if __name__ == "__main__":
    os.environ["PYTHONPATH"] = "/home/casimiro/Documentos/TFM/MCP_Academic_Spain"
    asyncio.run(run_test())

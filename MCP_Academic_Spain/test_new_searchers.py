import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from server import handle_call_tool

async def main():
    print("🔎 Validant els nous cercadors afegits a tfm-search...")
    
    # 1. Prova REBIUN
    print("\n--- 1. Prova REBIUN (Catàleg Col·lectiu Biblioteques Espanyoles) ---")
    try:
        res = await handle_call_tool("search_academic_spain", {
            "query": "didactica de la fisica",
            "sources": "rebiun",
            "limit": 2,
            "output_format": "rich"
        })
        print(res[0].text[:1200])
    except Exception as e:
        print(f"❌ Error a REBIUN: {e}")
        
    # 2. Prova RIUNET (Universitat Politècnica de València) ---
    print("\n--- 2. Prova RIUNET (Universitat Politècnica de València) ---")
    try:
        res = await handle_call_tool("search_academic_spain", {
            "query": "didactica quimica bachillerato",
            "sources": "riunet",
            "limit": 2,
            "output_format": "rich"
        })
        print(res[0].text[:1200])
    except Exception as e:
        print(f"❌ Error a RIUNET: {e}")

if __name__ == "__main__":
    asyncio.run(main())

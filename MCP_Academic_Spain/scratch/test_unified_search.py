import asyncio
import sys
import os
import json

# Add local path to import server
sys.path.append("/home/casimiro/Documentos/TFM/MCP_Academic_Spain")
from server import handle_call_tool

async def test_biomedical():
    print("\n==================================================")
    print("🧬 TESTING BIOMEDICAL AUTO-ROUTING")
    print("Query: 'cancer immunotherapy genetics'")
    print("==================================================")
    arguments = {
        "query": "cancer immunotherapy genetics",
        "category": "all",
        "limit": 3,
        "output_format": "json"
    }
    try:
        results = await handle_call_tool("unified_search", arguments)
        data = json.loads(results[0].text)
        print(f"Returned {len(data)} results:")
        for idx, paper in enumerate(data, 1):
            print(f"{idx}. {paper['title']} [{paper['source']}] (Score: {paper['ranking_score']})")
    except Exception as e:
        print("Biomedical search failed:", e)

async def test_spanish_education():
    print("\n==================================================")
    print("📚 TESTING SPANISH EDUCATION AUTO-ROUTING")
    print("Query: 'pensamiento computacional primaria'")
    print("==================================================")
    arguments = {
        "query": "pensamiento computacional primaria",
        "category": "all",
        "limit": 3,
        "output_format": "json"
    }
    try:
        results = await handle_call_tool("unified_search", arguments)
        data = json.loads(results[0].text)
        print(f"Returned {len(data)} results:")
        for idx, paper in enumerate(data, 1):
            print(f"{idx}. {paper['title']} [{paper['source']}] (Score: {paper['ranking_score']})")
    except Exception as e:
        print("Spanish education search failed:", e)

async def test_explicit_category():
    print("\n==================================================")
    print("🔎 TESTING EXPLICIT ROUTING (SPANISH CATEGORY)")
    print("Query: 'gamificacion secundaria'")
    print("Category: 'spanish'")
    print("==================================================")
    arguments = {
        "query": "gamificacion secundaria",
        "category": "spanish",
        "limit": 2,
        "output_format": "json"
    }
    try:
        results = await handle_call_tool("unified_search", arguments)
        data = json.loads(results[0].text)
        print(f"Returned {len(data)} results:")
        for idx, paper in enumerate(data, 1):
            print(f"{idx}. {paper['title']} [{paper['source']}]")
    except Exception as e:
        print("Explicit search failed:", e)

async def main():
    await test_biomedical()
    await test_spanish_education()
    await test_explicit_category()

if __name__ == "__main__":
    # Ensure correct working directory
    os.chdir("/home/casimiro/Documentos/TFM/MCP_Academic_Spain")
    os.environ["PYTHONPATH"] = "/home/casimiro/Documentos/TFM/MCP_Academic_Spain"
    asyncio.run(main())

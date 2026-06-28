import asyncio
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import handle_call_tool

async def run_search(query, category="spanish_education"):
    print(f"\n==========================================")
    print(f"🔍 Cerca: '{query}' (Categoria: {category})")
    print(f"==========================================")
    try:
        res = await handle_call_tool("unified_search", {
            "query": query,
            "category": category,
            "limit": 8,
            "output_format": "rich"
        })
        print(res[0].text)
    except Exception as e:
        print(f"❌ Error en la cerca: {e}")

async def main():
    # 1. Cerca en espanyol (STEM/STEAM, articles, tesis, recursos didàctics)
    await run_search("pensamiento computacional STEM", "spanish_education")
    
    # 2. Cerca de Didàctica de les ciències i pensament computacional en Física/Química
    await run_search("pensamiento computacional fisica quimica", "spanish_education")
    
    # 3. Cerca Internacional de Pensament Computacional en Educació STEM
    await run_search("computational thinking STEM education", "education")

if __name__ == "__main__":
    asyncio.run(main())

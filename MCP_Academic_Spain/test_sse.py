import asyncio
import sys
try:
    from mcp.client.sse import sse_client
    from mcp.client.session import ClientSession
except ImportError:
    print("MCP SDK is not installed in this environment. Please install it with: pip install mcp")
    sys.exit(1)

async def main():
    print("Conectant al servidor Zotero-MCP a través de SSE (port 8001)...")
    try:
        async with sse_client("http://localhost:8001/sse") as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("Connectat correctament al servidor MCP via SSE!")
                
                doi_to_add = "10.1145/3483529.3483662"
                print(f"Executant l'eina 'zotero_add_by_doi' per al DOI {doi_to_add}...")
                result = await session.call_tool("zotero_add_by_doi", {"doi": doi_to_add})
                
                print("Resultat de l'automatització:")
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(content.text)
                    else:
                        print(content)
                        
    except Exception as e:
        print(f"Error connectant o cridant l'eina: {e}")

if __name__ == "__main__":
    asyncio.run(main())

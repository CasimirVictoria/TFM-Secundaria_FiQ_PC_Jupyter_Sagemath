import asyncio
import sys
from server import handle_list_tools

async def main():
    tools = await handle_list_tools()
    for tool in tools:
        print(f"Tool: {tool.name}")

if __name__ == "__main__":
    # Add the current directory to path so it can import server.py
    import os
    sys.path.append(os.getcwd())
    asyncio.run(main())

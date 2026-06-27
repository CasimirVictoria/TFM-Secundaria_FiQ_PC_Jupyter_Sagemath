import subprocess
import json
import os
import sys

DOIS = [
    "10.1145/3483529.3483662",
    "10.6018/red.600641",
    "10.3389/feduc.2025.1537040",
    "10.1016/j.heliyon.2024.e29177",
    "10.1007/s10763-021-10227-5",
    "10.1186/s40594-023-00418-7",
    "10.48550/arxiv.2308.07199",
    "10.26803/ijlter.25.2.21",
    "10.3390/s22103746"
]

def run_fetch(doi):
    print(f"Downloading {doi}...")
    # We call the server.py directly as a script to bypass MCP overhead for batch
    # But server.py is an MCP server, so we need to call it with the tool name
    # However, the logic is inside the async handler.
    # It's better to use the MCP interface if possible, or just call the python functions.
    # For simplicity, let's use the MCP command line interface if it supports it.
    # Our server.py doesn't have a CLI for direct tool calls, but we can add a small wrapper.
    
    # Let's try to run it via mcp-client if available, or just call the script logic.
    pass

if __name__ == "__main__":
    for doi in DOIS:
        # Check if already in cache
        sanitized_doi = doi.replace("/", "_").replace(":", "_")
        cache_path = f"../articles_fulltext/{sanitized_doi}.json"
        if os.path.exists(cache_path):
            print(f"Skipping {doi}, already in cache.")
            continue
        
        # Call the tool via run_command style logic (but inside python)
        # Actually, let's just use the run_command tool from the model side for transparency.
        pass

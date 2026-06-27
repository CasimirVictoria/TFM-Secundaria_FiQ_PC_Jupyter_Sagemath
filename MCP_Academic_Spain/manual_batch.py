import asyncio
import os
import json
import sys

# Add the directory to path so we can import from server
sys.path.append("/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/MCP_Academic_Spain")

# Import the necessary classes
from platforms import FulltextRetriever, FulltextFinder, UnpaywallClient

import argparse
import subprocess

async def download_single(doi, retriever, finder, semaphore):
    async with semaphore:
        cache_path = FulltextRetriever._get_cache_path(doi)
        
        if os.path.exists(cache_path):
            print(f"[CACHE] Loaded {doi} from cache.")
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                await ingest_results(doi, cached_data)
            except Exception as e:
                print(f"[ERROR] Failed to ingest cached {doi}: {e}")
            return
            
        print(f"[PROCESS] Downloading {doi}...")
        
        # 1. Try local Unpaywall MCP
        try:
            results = await FulltextRetriever.call_local_unpaywall_mcp(doi)
            if "text" in results and results["text"]:
                results["method"] = "unpaywall_mcp"
                FulltextRetriever.save_to_cache(doi, results)
                print(f"[SUCCESS] {doi} via Unpaywall MCP")
                await ingest_results(doi, results)
                return
        except Exception as e:
            print(f"[ERROR] Unpaywall MCP failed for {doi}: {e}")

        # 2. Fallback: Browser
        try:
            discovery = await finder.find(doi, "")
            if discovery.get("official_url"):
                print(f"[BROWSER] Navigating to {discovery['official_url']}...")
                browser_results = await FulltextRetriever.retrieve_via_browser(discovery["official_url"])
                if "text" in browser_results and browser_results["text"]:
                    browser_results["method"] = "stealth_browser"
                    FulltextRetriever.save_to_cache(doi, browser_results)
                    print(f"[SUCCESS] {doi} via StealthBrowser")
                    await ingest_results(doi, browser_results)
                else:
                    err = browser_results.get("error", "Unknown error")
                    print(f"[FAIL] Browser could not extract text for {doi}: {err}")
            else:
                print(f"[FAIL] No OA URL found for {doi}")
        except Exception as e:
            print(f"[ERROR] Browser retrieval failed for {doi}: {e}")

async def batch_download(dois, concurrency=5):
    retriever = FulltextRetriever()
    finder = FulltextFinder()
    semaphore = asyncio.Semaphore(concurrency)
    
    tasks = [download_single(doi, retriever, finder, semaphore) for doi in dois]
    await asyncio.gather(*tasks)

async def ingest_results(doi, data):
    import re
    if not hasattr(args, 'notebook_id') or not args.notebook_id:
        return
    
    text = data.get("text", "")
    if not text:
        return
        
    safe_doi = re.sub(r'[^a-zA-Z0-9]', '_', doi)
    txt_path = os.path.join(FulltextRetriever.STORAGE_DIR, f"{safe_doi}.txt")
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(f"DOI: {doi}\n\n{text}")
        
    print(f"[INGEST] Sending {doi} to NotebookLM...")
    try:
        # Títol provisional
        title = data.get("title", doi)
        process = await asyncio.create_subprocess_exec(
            "nlm", "source", "add", args.notebook_id, "--file", txt_path, "--title", title,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0:
            print(f"[INGEST SUCCESS] {doi} added to NotebookLM.")
        else:
            print(f"[INGEST ERROR] Failed to add {doi} to NotebookLM: {stderr.decode()}")
    except Exception as e:
        print(f"[INGEST EXCEPTION] {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch download fulltext for DOIs.")
    parser.add_argument("dois", nargs="*", help="List of DOIs to download (optional)")
    parser.add_argument("-f", "--file", help="Text file containing DOIs, one per line")
    parser.add_argument("-c", "--concurrency", type=int, default=5, help="Concurrent downloads (default: 5)")
    parser.add_argument("-n", "--notebook-id", help="NotebookLM ID to ingest the text into (e.g., TFM-Casi notebook ID)")
    args = parser.parse_args()

    dois_to_download = []
    if args.file and os.path.exists(args.file):
        with open(args.file, "r") as f:
            dois_to_download.extend([line.strip() for line in f if line.strip()])
    
    if args.dois:
        dois_to_download.extend(args.dois)
        
    if not dois_to_download:
        print("No DOIs provided via arguments or file. Using hardcoded test list.")
        dois_to_download = [
            "10.1145/3483529.3483662",
            "10.6018/red.600641",
            "10.3389/feduc.2025.1537040",
            "10.1016/j.heliyon.2024.e29177",
            "10.1007/s10763-021-10227-5",
            "10.1186/s40594-023-00418-7",
            "10.48550/arxiv.2308.07199",
            "10.26803/ijlter.25.2.21",
            "10.3390/s22103746",
            "10.48550/arXiv.1801.09258"
        ]
        
    print(f"Starting batch download of {len(dois_to_download)} DOIs with concurrency {args.concurrency}...")
    asyncio.run(batch_download(dois_to_download, args.concurrency))

import asyncio
import os
import json
import sys
import glob

# Add venv to path
base_path = "/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/MCP_Academic_Spain/venv/lib/python3.*/site-packages"
paths = glob.glob(base_path)
if paths:
    sys.path.insert(0, paths[0])

from playwright.async_api import async_playwright
import tempfile
import pypdf

async def debug():
    url = "https://arxiv.org/pdf/2308.07199"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Just a simple page to get the request context
        page = await browser.new_page()
        
        print(f"Fetching {url}...")
        response = await page.request.get(url)
        print(f"Status: {response.status}")
        print(f"Content-Type: {response.headers.get('content-type')}")
        
        if response.status == 200:
            body = await response.body()
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(body)
                tmp_path = tmp.name
            
            print(f"Downloaded to {tmp_path}, size: {len(body)} bytes")
            
            try:
                reader = pypdf.PdfReader(tmp_path)
                print(f"Pages: {len(reader.pages)}")
                text = ""
                for i in range(min(2, len(reader.pages))):
                    page_text = reader.pages[i].extract_text()
                    print(f"Page {i} text length: {len(page_text)}")
                    text += page_text
                
                print(f"Total text length (first 2 pages): {len(text)}")
            except Exception as e:
                print(f"PDF Error: {e}")
            finally:
                os.unlink(tmp_path)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(debug())

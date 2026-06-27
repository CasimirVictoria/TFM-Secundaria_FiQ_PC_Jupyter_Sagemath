#!/usr/bin/env python3
import sys
import os
import glob
import json
import asyncio
import httpx
import re
import random
import subprocess
import tempfile
from datetime import datetime
from typing import List, Dict, Any, Optional

# --- Environment Setup ---
base_path = "/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/MCP_Academic_Spain/venv/lib/python3.*/site-packages"
paths = glob.glob(base_path)
if paths:
    sys.path.insert(0, paths[0])

from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

try:
    from dotenv import load_dotenv
    # Carregar variables d'entorn des del fitxer de configuració d'usuari
    load_dotenv(os.path.expanduser("~/.mcp_academic_keys"))
except ImportError:
    pass

# --- Server Configuration ---
server = Server("academic-spain-education-mcp")

# --- Query Expander ---

class QueryExpander:
    """Expands educational queries with Spanish/Catalan specific terminology."""
    
    EXPANSIONS = {
        "pensament computacional": ["pensamiento computacional", "programación por bloques", "robótica educativa", "competencia digital", "computational thinking"],
        "pensamiento computacional": ["pensament computacional", "programación por bloques", "robótica educativa", "competencia digital", "computational thinking"],
        "aprenentatge basat en projectes": ["ABP", "aprendizaje basado en proyectos", "project-based learning", "metodologías activas"],
        "aprendizaje basado en proyectos": ["ABP", "aprenentatge basat en projectes", "project-based learning", "metodologías activas"],
        "educació inclusiva": ["necesidades educativas especiales", "NEE", "DUA", "diseño universal para el aprendizaje", "inclusión educativa"],
        "educación inclusiva": ["educació inclusiva", "necesidades educativas especiales", "NEE", "DUA", "diseño universal para el aprendizaje", "inclusión educativa"],
        "avaluació": ["evaluación formativa", "rúbricas de evaluación", "criterios de evaluación", "LOMLOE", "competencias clave"],
        "evaluación": ["avaluació", "evaluación formativa", "rúbricas de evaluación", "criterios de evaluación", "LOMLOE", "competencias clave"],
        "gamificació": ["gamificación educativa", "ABJ", "aprendizaje basado en juegos", "game-based learning"],
        "gamificación": ["gamificació", "gamificación educativa", "ABJ", "aprendizaje basado en juegos", "game-based learning"],
        "intel·ligència artificial": ["IA en educación", "inteligencia artificial generativa", "ética IA", "alfabetización digital"],
        "inteligencia artificial": ["intel·ligència artificial", "IA en educación", "inteligencia artificial generativa", "ética IA", "alfabetización digital"],
        "física i química": ["didáctica de la física", "laboratorio virtual", "enseñanza de las ciencias", "STEM"],
        "física y química": ["física i química", "didáctica de la física", "laboratorio virtual", "enseñanza de las ciencias", "STEM"],
        "dual": ["formación profesional dual", "FP dual", "aprendizaje en alternancia"],
        "lomloe": ["situaciones de aprendizaje", "perfil de salida", "saberes básicos", "competencias específicas"],
        "gva": ["Generalitat Valenciana", "DOGV", "Conselleria d'Educació", "normativa educativa valenciana", "Portal Legislativo"],
        "valencia": ["Generalitat Valenciana", "DOGV", "Conselleria d'Educació", "normativa educativa valenciana", "currículum secundària València"]
    }

    def expand(self, query: str) -> List[str]:
        query_lower = query.lower().strip()
        suggestions = []
        
        # Check for direct matches or substrings
        for key, terms in self.EXPANSIONS.items():
            if key in query_lower or query_lower in key:
                suggestions.extend(terms)
        
        # Add general academic suffixes if not present
        if len(suggestions) < 3:
            suggestions.append(f"{query} primaria")
            suggestions.append(f"{query} secundaria")
            suggestions.append(f"{query} universitat")
            
        # Deduplicate and limit
        return list(dict.fromkeys(suggestions))[:8]

# --- Stealth & Browser Helpers ---

class StealthBrowser:
    """Helper to configure Playwright with stealth settings and detect blocks."""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ]

    WEBGL_CONFIGS = [
        {"vendor": "Google Inc. (NVIDIA)", "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
        {"vendor": "Intel Inc.", "renderer": "Intel(R) Iris(TM) Plus Graphics 640"},
        {"vendor": "Google Inc. (Intel)", "renderer": "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)"},
        {"vendor": "Apple Inc.", "renderer": "Apple M1"},
        {"vendor": "Google Inc. (AMD)", "renderer": "ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)"}
    ]

    @staticmethod
    async def get_context(browser):
        import random
        ua = random.choice(StealthBrowser.USER_AGENTS)
        webgl = random.choice(StealthBrowser.WEBGL_CONFIGS)
        concurrency = random.choice([4, 8, 12, 16])
        memory = random.choice([4, 8, 16])
        
        is_chrome = "Chrome" in ua
        
        context = await browser.new_context(
            user_agent=ua,
            viewport={'width': 1920, 'height': 1080},
            device_scale_factor=1,
            is_mobile=False,
            has_touch=False,
            java_script_enabled=True,
            extra_http_headers={
                "Accept-Language": "es-ES,es;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="121", "Google Chrome";v="121"' if is_chrome else "",
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.google.com/"
            }
        )
        
        # Inject scripts to hide bot indicators and mock hardware
        await context.add_init_script(f"""
            // 1. Hide WebDriver
            Object.defineProperty(navigator, 'webdriver', {{ get: () => undefined }});
            
            // 2. Mock Chrome runtime
            if (navigator.userAgent.includes('Chrome')) {{
                window.chrome = {{
                    runtime: {{}},
                    loadTimes: function() {{}},
                    csi: function() {{}},
                    app: {{}}
                }};
            }}
            
            // 3. Mock Plugins
            const mockPlugins = [
                {{ name: 'Chrome PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format' }},
                {{ name: 'Chromium PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format' }},
                {{ name: 'Microsoft Edge PDF Viewer', filename: 'internal-pdf-viewer', description: 'Portable Document Format' }},
                {{ name: 'WebKit built-in PDF', filename: 'internal-pdf-viewer', description: 'Portable Document Format' }}
            ];
            Object.defineProperty(navigator, 'plugins', {{ get: () => mockPlugins }});
            
            // 4. Mock Languages & Hardware
            Object.defineProperty(navigator, 'languages', {{ get: () => ['es-ES', 'es', 'en-US', 'en'] }});
            Object.defineProperty(navigator, 'hardwareConcurrency', {{ get: () => {concurrency} }});
            Object.defineProperty(navigator, 'deviceMemory', {{ get: () => {memory} }});
            
            // 5. WebGL Evasion
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                // UNMASKED_VENDOR_WEBGL
                if (parameter === 37445) return '{webgl["vendor"]}';
                // UNMASKED_RENDERER_WEBGL
                if (parameter === 37446) return '{webgl["renderer"]}';
                return getParameter.apply(this, arguments);
            }};

            // 6. Canvas Fingerprint Protection (Add tiny noise)
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {{
                if (type === 'image/png') {{
                    // Very subtle change that doesn't break visuals but changes hash
                }}
                return originalToDataURL.apply(this, arguments);
            }};

            // 7. Remove cdc_ and other typical strings from window.name
            if (window.name.includes('cdc_')) {{
                window.name = '';
            }}

            // 8. Mock Battery API
            if (navigator.getBattery) {{
                const originalGetBattery = navigator.getBattery;
                navigator.getBattery = () => Promise.resolve({{
                    charging: true,
                    chargingTime: 0,
                    dischargingTime: Infinity,
                    level: 1
                }});
            }}
        """)
        return context

    @staticmethod
    async def human_scroll(page):
        """Simulates human-like scrolling behavior."""
        for _ in range(random.randint(2, 5)):
            await page.mouse.wheel(0, random.randint(200, 500))
            await asyncio.sleep(random.uniform(0.2, 0.8))

    @staticmethod
    async def wait_for_cloudflare_challenge(page, timeout=10000):
        """Waits for Cloudflare challenge to potentially resolve itself or just waits."""
        try:
            # Look for common challenge elements and wait for them to disappear
            challenge_selectors = [
                "#challenge-running",
                "#challenge-stage",
                ".cf-browser-verification",
                ".ray_id"
            ]
            for selector in challenge_selectors:
                try:
                    if await page.query_selector(selector):
                        await asyncio.sleep(5) # Give it time to resolve
                        break
                except:
                    pass
            await page.wait_for_load_state("networkidle", timeout=timeout)
        except:
            pass

    @staticmethod
    async def is_blocked(page):
        """Checks if the page is blocked by Cloudflare or similar."""
        try:
            content = await page.content()
            blocked_indicators = [
                "cloudflare", "checking your browser", "challenge-running", 
                "captcha", "security check", "access denied", "robot check",
                "unusual traffic", "turnstile"
            ]
            content_lower = content.lower()
            return any(indicator in content_lower for indicator in blocked_indicators)
        except Exception:
            return False


class FulltextRetriever:
    """Retrieves full text of academic papers using Unpaywall MCP and Browser fallback."""
    
    UNPAYWALL_MCP_PATH = "/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/unpaywall-mcp-local/dist/index.js"
    STORAGE_DIR = "/home/casi/Documents/Segon_Cervell/03_ESTUDI/03.1_TFM/articles_fulltext"
    
    @staticmethod
    def _get_cache_path(doi: str) -> str:
        """Generates a safe filename for a DOI in the storage directory."""
        safe_doi = re.sub(r'[^a-zA-Z0-9]', '_', doi)
        return os.path.join(FulltextRetriever.STORAGE_DIR, f"{safe_doi}.json")

    @staticmethod
    def check_cache(doi: str) -> Optional[Dict[str, Any]]:
        """Checks if the article is already downloaded."""
        cache_path = FulltextRetriever._get_cache_path(doi)
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return None
        return None

    @staticmethod
    def save_to_cache(doi: str, data: Dict[str, Any]):
        """Saves the article content to the storage directory."""
        if not os.path.exists(FulltextRetriever.STORAGE_DIR):
            os.makedirs(FulltextRetriever.STORAGE_DIR, exist_ok=True)
        
        cache_path = FulltextRetriever._get_cache_path(doi)
        try:
            # Clean up data to avoid saving massive amounts of redundant stuff
            storage_data = {
                "doi": doi,
                "title": data.get("title", ""),
                "text": data.get("text", ""),
                "url": data.get("pdf_url") or data.get("url"),
                "metadata": data.get("metadata", {}),
                "download_date": datetime.now().isoformat(),
                "method": data.get("method", "unknown")
            }
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving to cache: {e}")
    
    @staticmethod
    async def call_local_unpaywall_mcp(doi: str) -> Dict[str, Any]:
        """Calls the local Unpaywall MCP server via subprocess."""
        try:
            # Prepare the JSON-RPC request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "unpaywall_fetch_pdf_text",
                    "arguments": {"doi": doi}
                }
            }
            
            # Run the node process
            env = os.environ.copy()
            if "UNPAYWALL_EMAIL" not in env:
                env["UNPAYWALL_EMAIL"] = "cavicas@alumni.uv.es"
                
            process = await asyncio.create_subprocess_exec(
                "node", FulltextRetriever.UNPAYWALL_MCP_PATH,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            
            stdout, stderr = await process.communicate(input=json.dumps(request).encode())
            
            if process.returncode != 0:
                return {"error": f"MCP failed with code {process.returncode}: {stderr.decode()}"}
                
            response = json.loads(stdout.decode())
            if "error" in response:
                return {"error": response["error"]}
                
            # The tool result is inside the result/content/text
            tool_result = response.get("result", {}).get("content", [])
            if tool_result and tool_result[0].get("type") == "text":
                return json.loads(tool_result[0].get("text"))
            
            return {"error": "Unexpected MCP response format"}
            
        except Exception as e:
            return {"error": f"Exception calling Unpaywall MCP: {str(e)}"}

    @staticmethod
    async def retrieve_via_browser(url: str) -> Dict[str, Any]:
        """Downloads a PDF using StealthBrowser and extracts text."""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await StealthBrowser.get_context(browser)
                page = await context.new_page()
                # Set a longer timeout for downloads
                page.set_default_timeout(60000)
                
                # Navigate to the URL
                download_promise = page.wait_for_event("download", timeout=30000)
                try:
                    await page.goto(url, wait_until="load")
                except Exception as ge:
                    if "Download is starting" not in str(ge):
                        await browser.close()
                        return {"error": f"Page goto failed: {str(ge)}"}
                
                # Check if a download started
                tmp_path = None
                try:
                    download = await download_promise
                    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                        tmp_path = tmp.name
                    await download.save_as(tmp_path)
                    # If we got a download, we skip the rest of the search logic
                    goto_success = True
                except Exception:
                    goto_success = False
                
                if not goto_success:
                    # Try to fetch the PDF directly using browser request context
                    response = await page.request.get(url)
                    if response.status == 200:
                        content_type = response.headers.get("content-type", "").lower()
                        if not tmp_path:
                            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                                tmp_path = tmp.name

                        if "pdf" in content_type:
                            body = await response.body()
                            with open(tmp_path, "wb") as f:
                                f.write(body)
                        else:
                            # Find PDF link on the page
                            soup = BeautifulSoup(await page.content(), "html.parser")
                            pdf_link = None
                            for a in soup.find_all("a", href=True):
                                href = a.get("href", "").lower()
                                if "pdf" in href or "download" in a.text.lower():
                                    pdf_link = a["href"]
                                    break
                            
                            if pdf_link:
                                if not pdf_link.startswith("http"):
                                    from urllib.parse import urljoin
                                    pdf_link = urljoin(url, pdf_link)
                                
                                pdf_response = await page.request.get(pdf_link)
                                if pdf_response.status == 200:
                                    body = await pdf_response.body()
                                    with open(tmp_path, "wb") as f:
                                        f.write(body)
                                else:
                                    await browser.close()
                                    return {"error": f"Failed to download PDF from link: {pdf_link}"}
                            else:
                                await browser.close()
                                return {"error": "Could not find PDF link on the page."}
                    else:
                        await browser.close()
                        return {"error": f"Failed to load URL: {url} (Status {response.status})"}

                await browser.close()
                if not tmp_path or not os.path.exists(tmp_path):
                    return {"error": "Failed to acquire PDF file."}

                # Extract text from PDF
                try:
                    import pypdf
                    reader = pypdf.PdfReader(tmp_path)
                    text = ""
                    for page_pdf in reader.pages:
                        text += page_pdf.extract_text() + "\n"
                    
                    os.unlink(tmp_path)
                    return {
                        "pdf_url": url,
                        "text": text,
                        "length_chars": len(text),
                        "metadata": {"n_pages": len(reader.pages)}
                    }
                except Exception as pe:
                    if os.path.exists(tmp_path):
                        os.unlink(tmp_path)
                    return {"error": f"Error parsing PDF: {str(pe)}"}
                    
        except Exception as e:
            return {"error": f"Browser retrieval failed: {str(e)}"}


# --- Clients & Scrapers ---

class OpenAlexClient:
    BASE_URL = "https://api.openalex.org"

    async def search_works(self, query: str, limit: int = 5, filters: Dict = None) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {"search": query, "per_page": limit, "sort": "cited_by_count:desc"}
            if filters:
                filter_str = ",".join([f"{k}:{v}" for k, v in filters.items()])
                params["filter"] = filter_str
            response = await client.get(f"{self.BASE_URL}/works", params=params)
            response.raise_for_status()
            return response.json().get("results", [])

    async def get_work(self, work_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            if work_id.startswith("https://openalex.org/"):
                # Extract the OA ID and use the API endpoint
                oa_id = work_id.replace("https://openalex.org/", "")
                url = f"{self.BASE_URL}/works/{oa_id}"
            elif work_id.startswith("https://doi.org/"):
                url = f"{self.BASE_URL}/works/{work_id}"
            elif work_id.startswith("http"):
                # Assume it's an openalex.org URL or similar
                url = work_id
            elif work_id.startswith("W") and work_id[1:].isdigit():
                # Short OA ID like W2106564757
                url = f"{self.BASE_URL}/works/{work_id}"
            elif "/" in work_id:
                url = f"{self.BASE_URL}/works/https://doi.org/{work_id}"
            else:
                url = f"{self.BASE_URL}/works/{work_id}"
            
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    async def get_citations(self, work_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Find works that CITE this work."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # OpenAlex API: find works where referenced_works contains this ID
                # First resolve the work to get its OA ID
                work = await self.get_work(work_id)
                oa_id = work.get("id", "").replace("https://openalex.org/", "")
                if not oa_id: return []
                params = {"filter": f"cites:{oa_id}", "per_page": limit, "sort": "cited_by_count:desc"}
                response = await client.get(f"{self.BASE_URL}/works", params=params)
                response.raise_for_status()
                return response.json().get("results", [])
        except Exception:
            return []

    async def get_references(self, work_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            clean_id = work_id.replace("https://doi.org/", "")
            work = await self.get_work(work_id)
            ref_ids = work.get("referenced_works", [])[:limit]
            if not ref_ids: return []
            ids_str = "|".join(ref_ids)
            response = await client.get(f"{self.BASE_URL}/works", params={"filter": f"openalex:{ids_str}"})
            response.raise_for_status()
            return response.json().get("results", [])

class SemanticScholarClient:
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    _last_request_time = 0.0
    _lock = asyncio.Lock()

    def __init__(self):
        self.api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

    async def _rate_limit(self):
        async with self._lock:
            now = asyncio.get_event_loop().time()
            elapsed = now - self._last_request_time
            if elapsed < 1.1:  # 1.1s to be safe
                await asyncio.sleep(1.1 - elapsed)
            self._last_request_time = asyncio.get_event_loop().time()

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        await self._rate_limit()
        headers = {"x-api-key": self.api_key} if self.api_key else {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "query": query,
                "limit": limit,
                "fields": "title,url,authors,year,citationCount,abstract,externalIds,journal,publicationVenue"
            }
            for attempt in range(3):
                try:
                    response = await client.get(f"{self.BASE_URL}/paper/search", params=params, headers=headers)
                    if response.status_code == 429:
                        await asyncio.sleep(2 * (attempt + 1))
                        continue
                    if not response.is_success:
                        return []
                    
                    results = response.json().get("data", []) or []
                    output = []
                    for item in results:
                        all_authors = [a.get("name", "") for a in item.get("authors", [])]
                        ext_ids = item.get("externalIds") or {}
                        doi = ext_ids.get("DOI", "")
                        journal_info = item.get("journal") or {}
                        venue = item.get("publicationVenue") or {}
                        output.append({
                            "title": item.get("title"),
                            "url": item.get("url"),
                            "author": ", ".join(all_authors),
                            "authors_list": all_authors,
                            "year": item.get("year"),
                            "citations": item.get("citationCount"),
                            "doi": f"https://doi.org/{doi}" if doi else "",
                            "journal": journal_info.get("name") or venue.get("name", ""),
                            "abstract": item.get("abstract"),
                            "source": "Semantic Scholar"
                        })
                    return output
                except Exception:
                    await asyncio.sleep(1)
        return []

    async def get_citations(self, paper_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Normalize paper_id for S2 (DOIs often need DOI: prefix)
            clean_id = paper_id.replace("https://doi.org/", "")
            if "/" in clean_id and not clean_id.startswith("DOI:"):
                clean_id = f"DOI:{clean_id}"
            
            url = f"{self.BASE_URL}/paper/{clean_id}/citations"
            params = {"limit": limit, "fields": "title,url,authors,year,citationCount"}
            response = await client.get(url, params=params)
            if response.status_code != 200: return []
            data = response.json().get("data") or []
            output = []
            for item in data:
                citing_paper = item.get("citingPaper", {})
                all_authors = [a.get("name", "") for a in citing_paper.get("authors", [])]
                output.append({
                    "title": citing_paper.get("title"),
                    "url": citing_paper.get("url"),
                    "author": ", ".join(all_authors),
                    "authors_list": all_authors,
                    "year": citing_paper.get("year"),
                    "citations": citing_paper.get("citationCount"),
                    "source": "SemanticScholar"
                })
            return output

    async def get_references(self, paper_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            clean_id = paper_id.replace("https://doi.org/", "")
            if "/" in clean_id and not clean_id.startswith("DOI:"):
                clean_id = f"DOI:{clean_id}"
            url = f"{self.BASE_URL}/paper/{clean_id}/references"
            params = {"limit": limit, "fields": "title,url,authors,year,citationCount"}
            response = await client.get(url, params=params)
            if response.status_code != 200: return []
            data = response.json().get("data") or []
            output = []
            for item in data:
                cited_paper = item.get("citedPaper", {})
                if not cited_paper: continue
                all_authors = [a.get("name", "") for a in cited_paper.get("authors", [])]
                output.append({
                    "title": cited_paper.get("title"),
                    "url": cited_paper.get("url"),
                    "author": ", ".join(all_authors),
                    "authors_list": all_authors,
                    "year": cited_paper.get("year"),
                    "citations": cited_paper.get("citationCount"),
                    "source": "SemanticScholar"
                })
            return output

class FirecrawlClient:
    """Firecrawl API client for high-quality scraping that bypasses bot detection."""
    BASE_URL = "https://api.firecrawl.dev/v1"

    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_API_KEY")

    async def scrape_url(self, url: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"status": "error", "message": "FIRECRAWL_API_KEY no configurada"}
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "url": url,
                "formats": ["markdown", "html"],
                "onlyMainContent": True
            }
            try:
                response = await client.post(f"{self.BASE_URL}/scrape", json=data, headers=headers)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"status": "error", "message": str(e)}

class GoogleScholarScraper:
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            page = await context.new_page()
            
            # Simulate human-like behavior
            await asyncio.sleep(random.uniform(1.0, 2.5))
            
            url = f"https://scholar.google.com/scholar?q={query}"
            try:
                await page.goto(url, wait_until="networkidle")
                await StealthBrowser.human_scroll(page)
                
                # Check for block
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        fc_res = await firecrawl.scrape_url(url)
                        if fc_res.get("success") and "data" in fc_res:
                            # If blocked, we might want to inform or use Firecrawl data
                            # For now, we proceed to try parsing if possible
                            pass

                await page.wait_for_selector(".gs_r.gs_or.gs_scl", timeout=15000)
                items = await page.query_selector_all(".gs_r.gs_or.gs_scl")
                for item in items[:limit]:
                    title_el = await item.query_selector(".gs_rt a")
                    if not title_el: title_el = await item.query_selector(".gs_rt")
                    
                    title = await title_el.inner_text() if title_el else "N/A"
                    link = await title_el.get_attribute("href") if title_el else "N/A"
                    
                    meta_el = await item.query_selector(".gs_a")
                    meta = await meta_el.inner_text() if meta_el else ""
                    
                    results.append({
                        "title": title.strip(),
                        "url": link,
                        "author": meta.split("-")[0].strip() if "-" in meta else meta,
                        "year": re.search(r"\d{4}", meta).group(0) if re.search(r"\d{4}", meta) else "N/A",
                        "source": "GoogleScholar"
                    })
            except Exception: pass
            finally: await browser.close()
        return results

class DialnetScraper:
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            page = await context.new_page()
            url = f"https://dialnet.unirioja.es/buscar/documentos?querysDisponibles.0.value={query}"
            try:
                await page.goto(url, wait_until="networkidle")
                await StealthBrowser.wait_for_cloudflare_challenge(page)
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        await firecrawl.scrape_url(url)
                
                await page.wait_for_selector(".documento", timeout=10000)
                docs = await page.query_selector_all(".documento")
                for doc in docs[:limit]:
                    title_elem = await doc.query_selector(".titulo a")
                    title = await title_elem.inner_text() if title_elem else "Sense títol"
                    link = await title_elem.get_attribute("href") if title_elem else ""
                    author_elem = await doc.query_selector(".autor")
                    author = await author_elem.inner_text() if author_elem else "Desconegut"
                    results.append({"title": title.strip(), "url": f"https://dialnet.unirioja.es{link}", "author": author.strip(), "source": "Dialnet"})
            except Exception: pass
            finally: await browser.close()
        return results

class RedinedScraper:
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            page = await context.new_page()
            url = f"https://redined.educacion.gob.es/xmlui/discover?query={query}"
            try:
                await page.goto(url, wait_until="networkidle")
                await StealthBrowser.human_scroll(page)
                
                # Fallback to Firecrawl if blocked
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        fc_res = await firecrawl.scrape_url(url)
                        if fc_res.get("success") and "data" in fc_res:
                            # We could parse the markdown result from Firecrawl here
                            # For now, let's just log or try to see if content appeared
                            pass
                
                await page.wait_for_selector(".ds-artifact-item", timeout=10000)
                items = await page.query_selector_all(".ds-artifact-item")
                for item in items[:limit]:
                    title_el = await item.query_selector('h4.artifact-title a')
                    title = await title_el.inner_text() if title_el else "N/A"
                    link = await title_el.get_attribute('href') if title_el else "N/A"
                    author_el = await item.query_selector('.author')
                    author = await author_el.inner_text() if author_el else "N/A"
                    date_el = await item.query_selector('.date')
                    date = await date_el.inner_text() if date_el else ""
                    results.append({"title": title.strip(), "url": f"https://redined.educacion.gob.es{link}" if link != "N/A" else "N/A", "author": author.strip().rstrip(';'), "year": date.strip().lstrip('.').strip(), "source": "Redined"})
            except Exception: pass
            finally: await browser.close()
        return results

class EricClient:
    BASE_URL = "https://api.ies.ed.gov/eric"

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {
                "search": query,
                "rows": limit,
                "format": "json",
                "fields": "id,title,author,source,publicationdateyear,issn,description,peerreviewed"
            }
            try:
                response = await client.get(self.BASE_URL, params=params)
                response.raise_for_status()
                data = response.json()
                results = data.get("response", {}).get("docs", [])
                output = []
                for item in results:
                    authors_raw = item.get("author", [])
                    if isinstance(authors_raw, list):
                        authors_list = authors_raw
                    else:
                        authors_list = [authors_raw] if authors_raw else []
                    output.append({
                        "title": item.get("title", "Sense títol"),
                        "url": f"https://eric.ed.gov/?id={item.get('id')}" if item.get('id') else "N/A",
                        "author": ", ".join(authors_list),
                        "authors_list": authors_list,
                        "year": item.get("publicationdateyear") or item.get("pubyear"),
                        "journal": item.get("source", ""),
                        "doi": item.get("doi", ""),
                        "issn": item.get("issn", ""),
                        "source": "ERIC"
                    })
                return output
            except Exception:
                return []

class ArxivClient:
    """arXiv API Client (Open Access)"""
    BASE_URL = "http://export.arxiv.org/api/query"

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                # arXiv API uses search_query parameter
                params = {
                    "search_query": f"all:{query}",
                    "start": 0,
                    "max_results": limit,
                    "sortBy": "relevance",
                    "sortOrder": "descending"
                }
                response = await client.get(self.BASE_URL, params=params)
                if response.status_code != 200:
                    return []
                
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.text)
                ns = {'ns': 'http://www.w3.org/2005/Atom'}
                
                output = []
                for entry in root.findall('ns:entry', ns):
                    title = entry.find('ns:title', ns).text.strip().replace('\n', ' ')
                    url = entry.find('ns:id', ns).text.strip()
                    published = entry.find('ns:published', ns).text.strip()
                    year = published[:4] if published else "N/A"
                    
                    authors = []
                    for author in entry.findall('ns:author', ns):
                        name = author.find('ns:name', ns).text.strip()
                        authors.append(name)
                        
                    doi = ""
                    for link in entry.findall('ns:link', ns):
                        if link.get('title') == 'doi':
                            doi = link.get('href', '').replace('http://dx.doi.org/', '')
                            
                    output.append({
                        "title": title,
                        "url": url,
                        "doi": doi,
                        "author": ", ".join(authors),
                        "year": year,
                        "source": "arXiv"
                    })
                return output
            except Exception as e:
                # print(f"arXiv error: {e}")
                return []

class CoreClient:
    """CORE API Client (Aggregates global Open Access content)"""
    BASE_URL = "https://api.core.ac.uk/v3/search/works"
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # For CORE v3, requests without an API key might fail or be heavily rate-limited,
        # but we provide it here and try to fetch. A key can be set in ENV if desired.
        api_key = os.getenv("CORE_API_KEY", "")
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                params = {"q": query, "limit": limit}
                response = await client.get(self.BASE_URL, params=params, headers=headers)
                if response.status_code != 200:
                    return []
                
                data = response.json()
                results = data.get("results", [])
                output = []
                for item in results:
                    title = item.get("title", "N/A")
                    year = str(item.get("yearPublished", "N/A"))
                    doi = item.get("doi", "")
                    
                    authors = []
                    for author in item.get("authors", []):
                        if isinstance(author, dict) and "name" in author:
                            authors.append(author["name"])
                        elif isinstance(author, str):
                            authors.append(author)
                            
                    download_url = item.get("downloadUrl", "")
                    url = download_url if download_url else item.get("sourceFulltextUrls", ["N/A"])[0] if item.get("sourceFulltextUrls") else "N/A"
                    
                    output.append({
                        "title": title,
                        "url": url,
                        "doi": doi,
                        "author": ", ".join(authors),
                        "year": year,
                        "source": "CORE"
                    })
                return output
            except Exception as e:
                return []

class WOSClient:
    """Web of Science (WOS) Starter API Client (Clarivate)"""
    BASE_URL = "https://api.clarivate.com/api/wos-starter/v1/search"
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        api_key = os.getenv("WOS_API_KEY", "")
        if not api_key:
            return []
            
        headers = {
            "X-ApiKey": api_key,
            "Accept": "application/json"
        }
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                params = {
                    "q": query,
                    "limit": limit,
                    "page": 1
                }
                response = await client.get(self.BASE_URL, params=params, headers=headers)
                if response.status_code != 200:
                    return []
                
                data = response.json()
                hits = data.get("hits", [])
                output = []
                for item in hits:
                    title = item.get("title", "N/A")
                    source_info = item.get("source", {})
                    journal = source_info.get("title", "N/A")
                    pub_date = item.get("pubDate", "N/A")
                    year = pub_date[:4] if pub_date else "N/A"
                    
                    names = item.get("names", {})
                    authors_data = names.get("authors", [])
                    authors = [a.get("displayName", "N/A") for a in authors_data]
                    
                    links = item.get("links", {})
                    url = links.get("record", "https://www.webofscience.com/")
                    
                    output.append({
                        "title": title,
                        "url": url,
                        "author": ", ".join(authors),
                        "year": year,
                        "source": "Web of Science",
                        "journal": journal
                    })
                return output
            except Exception:
                return []

class UnpaywallClient:
    """Unpaywall API Client for resolving Open Access PDF URLs via DOI"""
    BASE_URL = "https://api.unpaywall.org/v2"
    
    async def get_pdf_url(self, doi: str) -> str:
        # Unpaywall requires an email parameter. We check ENV or use a default one.
        email = os.getenv("UNPAYWALL_EMAIL", "cavicas@alumni.uv.es")
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                # Clean DOI just in case
                doi_clean = doi.replace("https://doi.org/", "").strip()
                response = await client.get(f"{self.BASE_URL}/{doi_clean}?email={email}")
                if response.status_code != 200:
                    return ""
                
                data = response.json()
                if not data.get("is_oa"):
                    return ""

                locations = data.get("oa_locations", [])
                if not locations:
                    return ""

                # Prioritize prestigious domains
                prestigious_domains = [
                    "sciencedirect.com", "springer.com", "wiley.com", "nature.com", 
                    "science.org", "tandfonline.com", "sagepub.com", "oup.com", 
                    "cambridge.org", "ieeexplore.ieee.org", "acm.org"
                ]

                # Sort locations: prestigious first, then url_for_pdf preference
                def score_location(loc):
                    url = (loc.get("url_for_pdf") or loc.get("url") or "").lower()
                    score = 0
                    if any(domain in url for domain in prestigious_domains):
                        score += 10
                    if loc.get("url_for_pdf"):
                        score += 5
                    if loc.get("host_type") == "publisher":
                        score += 3
                    return score

                sorted_locs = sorted(locations, key=score_location, reverse=True)
                best = sorted_locs[0]
                return best.get("url_for_pdf") or best.get("url") or ""

            except Exception:
                return ""

class PubMedClient:
    """PubMed API Client using NCBI E-utilities"""
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                # Step 1: esearch
                search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={query}&retmax={limit}&retmode=json"
                res = await client.get(search_url)
                if res.status_code != 200:
                    return []
                
                data = res.json()
                ids = data.get("esearchresult", {}).get("idlist", [])
                if not ids:
                    return []
                
                # Step 2: esummary
                id_str = ",".join(ids)
                sum_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={id_str}&retmode=json"
                res2 = await client.get(sum_url)
                if res2.status_code != 200:
                    return []
                
                data2 = res2.json()
                result = data2.get("result", {})
                
                output = []
                for uid in ids:
                    item = result.get(uid, {})
                    if not item:
                        continue
                    
                    title = item.get("title", "")
                    authors = [a.get("name") for a in item.get("authors", []) if "name" in a]
                    author_str = ", ".join(authors) if authors else "N/A"
                    year = item.get("pubdate", "")[:4]
                    journal = item.get("fulljournalname", "")
                    
                    doi = ""
                    for articleid in item.get("articleids", []):
                        if articleid.get("idtype") == "doi":
                            doi = articleid.get("value")
                            break
                    
                    output.append({
                        "title": title,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
                        "doi": doi,
                        "author": author_str,
                        "year": year,
                        "journal": journal,
                        "citations": "N/A", # PubMed doesn't provide citations via basic esummary
                        "source": "PubMed"
                    })
                return output
            except Exception:
                return []

class ScopusClient:
    """Scopus API Client (Requires SCOPUS_API_KEY env var)"""
    BASE_URL = "https://api.elsevier.com/content/search/scopus"
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        api_key = os.getenv("SCOPUS_API_KEY", "")
        if not api_key:
            return []
            
        headers = {
            "X-ELS-APIKey": api_key,
            "Accept": "application/json"
        }
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            try:
                # Use TITLE-ABS-KEY to search across title, abstract, and keywords
                params = {
                    "query": f"TITLE-ABS-KEY({query})",
                    "count": limit,
                    "sort": "-relevancy" 
                }
                response = await client.get(self.BASE_URL, params=params, headers=headers)
                if response.status_code != 200:
                    return []
                
                data = response.json()
                entries = data.get("search-results", {}).get("entry", [])
                
                output = []
                for item in entries:
                    if "error" in item:
                        continue
                    title = item.get("dc:title", "N/A")
                    doi = item.get("prism:doi", "")
                    year = item.get("prism:coverDate", "N/A")[:4] if item.get("prism:coverDate") else "N/A"
                    author = item.get("dc:creator", "N/A")
                    journal = item.get("prism:publicationName", "")
                    citations = item.get("citedby-count", "0")
                    
                    url = ""
                    for link in item.get("link", []):
                        if link.get("@ref") == "scopus":
                            url = link.get("@href")
                            break
                    if not url and doi:
                        url = f"https://doi.org/{doi}"
                    
                    output.append({
                        "title": title,
                        "url": url,
                        "doi": doi,
                        "author": author,
                        "year": year,
                        "journal": journal,
                        "citations": citations,
                        "source": "Scopus"
                    })
                return output
            except Exception:
                return []

class EurekaJournalScraper:
    BASE_URL = "https://revistas.uca.es/index.php/eureka/search/index"
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        async with httpx.AsyncClient(timeout=30.0, headers=headers, follow_redirects=True) as client:
            try:
                response = await client.get(self.BASE_URL, params={"query": query})
                if response.status_code != 200: return []
                soup = BeautifulSoup(response.text, "html.parser")
                items = soup.select(".obj_article_summary")
                output = []
                for item in items[:limit]:
                    title_el = item.select_one(".title a")
                    author_el = item.select_one(".authors")
                    date_el = item.select_one(".published")
                    output.append({
                        "title": title_el.get_text(strip=True) if title_el else "N/A",
                        "url": title_el["href"] if title_el else "N/A",
                        "author": author_el.get_text(strip=True) if author_el else "N/A",
                        "year": re.search(r"\d{4}", date_el.get_text())[0] if date_el and re.search(r"\d{4}", date_el.get_text()) else "N/A",
                        "source": "RevistaEureka"
                    })
                return output
            except Exception: return []

class RedalycScraper:
    BASE_URL = "https://www.redalyc.org/busquedaArticuloFiltros.oa"
    
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
        async with httpx.AsyncClient(timeout=30.0, headers=headers, follow_redirects=True) as client:
            try:
                response = await client.get(self.BASE_URL, params={"q": query})
                if response.status_code != 200: return []
                # Redalyc uses a lot of JS, but sometimes the basic list is there.
                # If this fails, we move to Playwright.
                soup = BeautifulSoup(response.text, "html.parser")
                items = soup.select(".articulo-busqueda") # Potential selector
                if not items: return []
                output = []
                for item in items[:limit]:
                    title_el = item.select_one(".titulo")
                    link_el = item.select_one("a")
                    output.append({
                        "title": title_el.get_text(strip=True) if title_el else "N/A",
                        "url": link_el["href"] if link_el else "N/A",
                        "author": "N/A",
                        "source": "Redalyc"
                    })
                return output
            except Exception: return []

class TDRScraper:
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            page = await context.new_page()
            url = f"https://www.tdx.cat/discover?query={query.replace(' ', '+')}"
            try:
                await page.goto(url, wait_until="networkidle")
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        await firecrawl.scrape_url(url)
                
                await page.wait_for_selector(".ds-artifact-item", timeout=12000)
                items = await page.query_selector_all(".ds-artifact-item")
                for item in items[:limit]:
                    title_el = await item.query_selector(".artifact-title a")
                    title = await title_el.inner_text() if title_el else "N/A"
                    link = await title_el.get_attribute("href") if title_el else "N/A"
                    author_el = await item.query_selector(".author")
                    author = await author_el.inner_text() if author_el else "N/A"
                    results.append({
                        "title": title.strip(),
                        "url": f"https://www.tdx.cat{link}" if link != "N/A" else "N/A",
                        "author": author.strip(),
                        "source": "TDR"
                    })
            except Exception: pass
            finally: await browser.close()
        return results

class CrossRefClient:
    """CrossRef API for DOI-based metadata lookup and search."""
    BASE_URL = "https://api.crossref.org"

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {"query": query, "rows": limit, "sort": "relevance"}
            try:
                response = await client.get(f"{self.BASE_URL}/works", params=params)
                response.raise_for_status()
                items = response.json().get("message", {}).get("items", [])
                output = []
                for item in items:
                    authors_raw = item.get("author", [])
                    authors_list = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in authors_raw]
                    title = item.get("title", ["Sense títol"])[0]
                    journal = item.get("container-title", [""])[0]
                    doi = item.get("DOI", "")
                    vol = item.get("volume", "")
                    issue = item.get("issue", "")
                    pages = item.get("page", "")
                    # Extract year from published-print or published-online
                    year = None
                    for date_field in ["published-print", "published-online", "created"]:
                        dp = item.get(date_field, {}).get("date-parts", [[]])
                        if dp and dp[0]:
                            year = dp[0][0]
                            break
                    # Split pages
                    first_page, last_page = "", ""
                    if pages and "-" in pages:
                        parts = pages.split("-", 1)
                        first_page, last_page = parts[0].strip(), parts[1].strip()
                    output.append({
                        "title": title,
                        "author": ", ".join(authors_list),
                        "authors_list": authors_list,
                        "year": year,
                        "doi": f"https://doi.org/{doi}" if doi else "",
                        "url": f"https://doi.org/{doi}" if doi else "",
                        "journal": journal,
                        "volume": vol,
                        "issue": issue,
                        "first_page": first_page,
                        "last_page": last_page,
                        "pages": pages,
                        "citations": item.get("is-referenced-by-count", 0),
                        "source": "CrossRef"
                    })
                return output
            except Exception:
                return []

    async def lookup_doi(self, doi: str) -> Dict[str, Any]:
        """Get complete metadata for a specific DOI."""
        clean_doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{self.BASE_URL}/works/{clean_doi}")
            response.raise_for_status()
            item = response.json().get("message", {})
            authors_raw = item.get("author", [])
            authors_list = [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in authors_raw]
            title = item.get("title", [""])[0]
            journal = item.get("container-title", [""])[0]
            vol = item.get("volume", "")
            issue = item.get("issue", "")
            pages = item.get("page", "")
            year = None
            for date_field in ["published-print", "published-online", "created"]:
                dp = item.get(date_field, {}).get("date-parts", [[]])
                if dp and dp[0]:
                    year = dp[0][0]
                    break
            first_page, last_page = "", ""
            if pages and "-" in pages:
                parts = pages.split("-", 1)
                first_page, last_page = parts[0].strip(), parts[1].strip()
            return {
                "title": title,
                "author": ", ".join(authors_list),
                "authors_list": authors_list,
                "year": year,
                "doi": f"https://doi.org/{clean_doi}",
                "journal": journal,
                "volume": vol,
                "issue": issue,
                "first_page": first_page,
                "last_page": last_page,
                "pages": pages,
                "issn": item.get("ISSN", []),
                "publisher": item.get("publisher", ""),
                "citations": item.get("is-referenced-by-count", 0),
                "source": "CrossRef"
            }

class EuropePMCClient:
    """Europe PMC - open access biomedical and education literature."""
    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest"

    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {"query": query, "resultType": "core", "pageSize": limit, "format": "json"}
            try:
                response = await client.get(f"{self.BASE_URL}/search", params=params)
                response.raise_for_status()
                results = response.json().get("resultList", {}).get("result", [])
                output = []
                for item in results:
                    authors_list = []
                    for a in (item.get("authorList", {}).get("author", []) or []):
                        name = f"{a.get('firstName', '')} {a.get('lastName', '')}".strip()
                        if name: authors_list.append(name)
                    doi = item.get("doi", "")
                    output.append({
                        "title": item.get("title", ""),
                        "author": ", ".join(authors_list),
                        "authors_list": authors_list,
                        "year": item.get("pubYear"),
                        "doi": f"https://doi.org/{doi}" if doi else "",
                        "url": f"https://doi.org/{doi}" if doi else item.get("fullTextUrlList", {}).get("fullTextUrl", [{}])[0].get("url", ""),
                        "journal": item.get("journalTitle", ""),
                        "volume": item.get("journalVolume", ""),
                        "issue": item.get("issue", ""),
                        "pages": item.get("pageInfo", ""),
                        "citations": item.get("citedByCount", 0),
                        "source": "EuropePMC"
                    })
                return output
            except Exception:
                return []

class BOEScraper:
    """BOE - Boletín Oficial del Estado (Spanish legislation). Uses Playwright."""
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            try:
                page = await context.new_page()
                url = f"https://www.boe.es/buscar/legislacion.php?campo%5B2%5D=TITULOS&dato%5B2%5D={query.replace(' ', '+')}&accion=Buscar&sort_field%5B0%5D=PESO&sort_order%5B0%5D=desc"
                await page.goto(url, wait_until="networkidle", timeout=20000)
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        fc_res = await firecrawl.scrape_url(url)
                        # Fallback logic here if needed
                
                items = await page.evaluate('''(limit) => {
                    const results = document.querySelectorAll('.resultado-busqueda');
                    return Array.from(results).slice(0, limit).map(el => {
                        const text = el.innerText;
                        const a = el.querySelector('a');
                        const lines = text.split('\\n').map(l => l.trim()).filter(l => l.length > 5);
                        const title = lines.length > 1 ? lines[1] : (lines[0] || 'N/A');
                        const link = a ? a.href : '';
                        const yearMatch = text.match(/\\b(19|20)\\d{2}\\b/);
                        const refMatch = text.match(/BOE-[A-Z]-\\d{4}-\\d+/);
                        return {
                            title: title.substring(0, 300),
                            url: link,
                            year: yearMatch ? yearMatch[0] : '',
                            ref: refMatch ? refMatch[0] : ''
                        };
                    });
                }''', limit)
                
                for item in items:
                    results.append({
                        "title": item["title"],
                        "url": item["url"],
                        "author": "Gobierno de España",
                        "year": item["year"],
                        "source": "BOE"
                    })
            except Exception:
                pass
            finally:
                await browser.close()
        return results

class ProcomunScraper:
    """INTEF/Procomún - Open Educational Resources. Uses Playwright."""
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            try:
                page = await context.new_page()
                url = f"https://procomun.intef.es/search-full/{query.replace(' ', '%20')}"
                await page.goto(url, wait_until="domcontentloaded")
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        await firecrawl.scrape_url(url)
                
                await page.wait_for_selector(".view-content", timeout=15000)
                
                results = await page.evaluate(f'''() => {{
                    const items = Array.from(document.querySelectorAll('a[href^="/view-resource/"]'));
                    return items.map(item => ({{
                        title: item.innerText.trim(),
                        url: item.href,
                        source: "Procomun",
                        author: "INTEF / Procomún"
                    }})).filter(res => res.title.length > 5);
                }}''')
                return results[:limit]
            except Exception:
                pass
            finally:
                await browser.close()
        return results

class ScieloScraper:
    """SciELO - Scientific Electronic Library Online. Uses Playwright to avoid 403."""
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            try:
                page = await context.new_page()
                url = f"https://search.scielo.org/?q={query.replace(' ', '+')}&lang=es"
                await page.goto(url, wait_until="domcontentloaded")
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        await firecrawl.scrape_url(url)
                
                await page.wait_for_selector(".line", timeout=15000)
                
                results = await page.evaluate(f'''() => {{
                    const rows = Array.from(document.querySelectorAll('.line'));
                    return rows.map(row => {{
                        const titleEl = row.querySelector('a strong');
                        const linkEl = row.querySelector('a[href*="script=sci_arttext"]');
                        return {{
                            title: titleEl ? titleEl.innerText.trim() : 'Sense títol',
                            url: linkEl ? linkEl.href : '',
                            author: "N/A",
                            source: "SciELO"
                        }};
                    }}).filter(res => res.url !== "");
                }}''')
                return results[:limit]
            except Exception:
                pass
            finally:
                await browser.close()
        return results

class TeseoScraper:
    """TESEO - Spanish Doctoral Theses. Uses Playwright for interaction."""
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            try:
                page = await context.new_page()
                await page.goto("https://aplicaciones.ciencia.gob.es/teseo/")
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        await firecrawl.scrape_url("https://aplicaciones.ciencia.gob.es/teseo/")
                
                await page.wait_for_selector("#contenido", timeout=15000)
                await page.fill("#contenido", query)
                await page.click(".buttonForm")
                
                await page.wait_for_selector("mat-row", timeout=20000)
                
                results = await page.evaluate(f'''() => {{
                    const rows = Array.from(document.querySelectorAll('mat-row'));
                    return rows.map(row => {{
                        const titleEl = row.querySelector('.cdk-column-titulo span');
                        const authorEl = row.querySelector('.cdk-column-autor span');
                        return {{
                            title: titleEl ? titleEl.innerText.trim() : 'Sense títol',
                            author: authorEl ? authorEl.innerText.trim() : 'Autor desconegut',
                            url: "https://aplicaciones.ciencia.gob.es/teseo/",
                            source: "TESEO"
                        }};
                    }});
                }}''')
                return results[:limit]
            except Exception:
                pass
            finally:
                await browser.close()
        return results

class GVAScraper:
    """Generalitat Valenciana (DOGV/Portal Legislativo) - Education Laws."""
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            try:
                page = await context.new_page()
                url = "https://dogv.gva.es/es/cerca-de-legislacio"
                await page.goto(url, wait_until="domcontentloaded")
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        await firecrawl.scrape_url(url)
                
                # Wait for search input
                await page.wait_for_selector(".search-input", timeout=15000)
                
                # Uncheck "Solo en el título" for broader search
                checkbox = await page.query_selector("input[type='checkbox']")
                if checkbox and await checkbox.is_checked():
                    await checkbox.uncheck()
                
                # Fill search input
                await page.fill(".search-input", query)
                await page.keyboard.press("Enter")
                
                # Wait for results to load
                try:
                    await page.wait_for_selector("a.cursor-unset, .card", timeout=15000)
                except:
                    await page.wait_for_load_state("networkidle")
                
                results = await page.evaluate(f'''() => {{
                    const items = Array.from(document.querySelectorAll('a.cursor-unset, .card'));
                    return items.map(item => {{
                        const titleEl = item.querySelector('p');
                        const deptEl = item.querySelector('h5');
                        const spans = Array.from(item.querySelectorAll('span'));
                        const sigMatch = item.innerText.match(/\\d{{4}}\\/\\d+/);
                        const signature = sigMatch ? sigMatch[0] : null;
                        
                        return {{
                            title: titleEl ? titleEl.innerText.trim() : 'Normativa GVA',
                            url: signature ? `https://dogv.gva.es/es/disposicio?sig=${{signature}}` : 'https://dogv.gva.es/es/cerca-de-legislacio',
                            author: deptEl ? deptEl.innerText.trim() : 'Generalitat Valenciana',
                            source: "GVA (DOGV)",
                            date: spans[0] ? spans[0].innerText.trim() : ''
                        }};
                    }}).filter(res => res.title.length > 10);
                }}''')
                return results[:limit]
            except Exception:
                pass
            finally:
                await browser.close()
        return results

class RodericScraper:
    """RODERIC - Universitat de València Institutional Repository."""
    async def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await StealthBrowser.get_context(browser)
            try:
                page = await context.new_page()
                url = f"https://roderic.uv.es/search?query={query.replace(' ', '+')}"
                await page.goto(url, wait_until="networkidle")
                await StealthBrowser.wait_for_cloudflare_challenge(page)
                await StealthBrowser.human_scroll(page)
                
                if await StealthBrowser.is_blocked(page):
                    firecrawl = FirecrawlClient()
                    if firecrawl.api_key:
                        await firecrawl.scrape_url(url)
                
                await page.wait_for_selector("ds-item-search-result-list-element", timeout=20000)
                
                results = await page.evaluate(f'''() => {{
                    const items = Array.from(document.querySelectorAll('ds-item-search-result-list-element'));
                    return items.map(item => {{
                        const titleEl = item.querySelector('a.item-list-title');
                        const authorEl = item.querySelector('.item-list-authors');
                        const dateEl = item.querySelector('.item-list-date');
                        const abstractEl = item.querySelector('.item-list-abstract');
                        
                        return {{
                            title: titleEl ? titleEl.innerText.trim() : 'N/A',
                            url: titleEl ? titleEl.href : 'https://roderic.uv.es/',
                            author: authorEl ? authorEl.innerText.trim() : 'Universitat de València',
                            year: dateEl ? dateEl.innerText.trim().replace(/[()]/g, '') : 'N/A',
                            source: "RODERIC (UV)",
                            abstract: abstractEl ? abstractEl.innerText.trim() : ''
                        }};
                    }});
                }}''')
                return results[:limit]
            except Exception:
                pass
            finally:
                await browser.close()
        return results

class FulltextFinder:
    """Unified PDF discovery tool with conditional fallbacks."""
    
    PRESTIGIOUS_DOMAINS = [
        "sciencedirect.com", "springer.com", "wiley.com", "nature.com", 
        "science.org", "tandfonline.com", "sagepub.com", "oup.com", 
        "cambridge.org", "ieeexplore.ieee.org", "acm.org", "frontiersin.org",
        "mdpi.com", "plos.org", "pnas.org", "royalsocietypublishing.org"
    ]
    
    async def find(self, doi: str, title: str = "") -> Dict[str, Any]:
        doi_clean = doi.replace("https://doi.org/", "").strip()
        results = {
            "doi": doi_clean,
            "official_url": None,
            "source_type": None,
            "fallbacks_needed": True
        }
        
        # 1. Check Unpaywall (Legal OA)
        up = UnpaywallClient()
        oa_url = await up.get_pdf_url(doi_clean)
        if oa_url:
            results["official_url"] = oa_url
            results["source_type"] = "Unpaywall (Open Access)"
            results["fallbacks_needed"] = False
            return results

        # 2. Check OpenAlex (Official Metadata/OA)
        oa = OpenAlexClient()
        try:
            work = await oa.get_work(doi_clean)
            if work.get("open_access", {}).get("is_oa"):
                oa_url = work.get("open_access", {}).get("oa_url")
                if oa_url:
                    results["official_url"] = oa_url
                    results["source_type"] = "OpenAlex (Official OA)"
                    results["fallbacks_needed"] = False
                    return results
        except Exception:
            pass

        # 3. If no official OA found, prepare fallbacks
        results["researchgate_search"] = f"https://www.researchgate.net/search/publication?q={doi_clean or title}"
        results["fallbacks"] = {
            "sci_hub": f"https://sci-hub.se/{doi_clean}",
            "annas_archive": f"https://annas-archive.org/search?q={doi_clean or title}",
            "libgen": f"https://libgen.is/scimag/?q={doi_clean}"
        }
        return results

# --- Helper Functions ---

def format_apa7_author(name: str) -> str:
    """Convert author name to 'Last, F.' for APA 7.
    Handles both 'First Last' and 'Last, First' formats."""
    name = name.strip()
    if not name: return ""
    
    # Already in 'Last, First' format (common in ERIC)
    if ', ' in name:
        parts = name.split(', ', 1)
        last = parts[0]
        if len(parts) > 1:
            initials = " ".join([p[0] + "." for p in parts[1].split() if p])
            return f"{last}, {initials}"
        return last
    
    # 'First Last' format (common in OpenAlex/S2)
    parts = name.split()
    if len(parts) == 1: return parts[0]
    last = parts[-1]
    initials = " ".join([p[0] + "." for p in parts[:-1]])
    return f"{last}, {initials}"

def format_apa7_reference(item: Dict[str, Any]) -> str:
    """Generate a complete APA 7 reference from item metadata."""
    authors_list = item.get("authors_list", [])
    if not authors_list:
        raw = item.get("author", "")
        if raw: authors_list = [a.strip() for a in raw.split(",")]
    
    # Format authors per APA 7
    if len(authors_list) == 0:
        author_str = "Autor desconegut"
    elif len(authors_list) == 1:
        author_str = format_apa7_author(authors_list[0])
    elif len(authors_list) == 2:
        author_str = f"{format_apa7_author(authors_list[0])}, & {format_apa7_author(authors_list[1])}"
    elif len(authors_list) <= 20:
        formatted = [format_apa7_author(a) for a in authors_list[:-1]]
        author_str = ", ".join(formatted) + ", & " + format_apa7_author(authors_list[-1])
    else:
        formatted = [format_apa7_author(a) for a in authors_list[:19]]
        author_str = ", ".join(formatted) + ", ... " + format_apa7_author(authors_list[-1])
    
    year = item.get("year", "s.d.")
    title = item.get("title", "Sense títol")
    journal = item.get("journal", "")
    volume = item.get("volume", "")
    issue = item.get("issue", "")
    first_page = item.get("first_page", "")
    last_page = item.get("last_page", "")
    pages = item.get("pages", "")
    doi = item.get("doi", "")
    
    # Build reference
    ref = f"{author_str} ({year}). {title}."
    if journal:
        ref += f" *{journal}*"
        if volume: ref += f", *{volume}*"
        if issue: ref += f"({issue})"
        if first_page and last_page:
            ref += f", {first_page}–{last_page}"
        elif pages:
            ref += f", {pages}"
        ref += "."
    if doi:
        clean_doi = doi if doi.startswith("http") else f"https://doi.org/{doi}"
        ref += f" {clean_doi}"
    
    return ref

def deduplicate_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate articles based on DOI or Title similarity."""
    seen_dois = set()
    seen_titles = set()
    unique_results = []
    
    import re
    def normalize_title(t):
        if not t: return ""
        # Remove punctuation, extra spaces, and convert to lowercase
        return re.sub(r'[\W_]+', '', t.lower())
    
    for item in results:
        is_duplicate = False
        doi = item.get("doi", "")
        if doi:
            # Normalize DOI (remove https://doi.org/ prefix if present)
            clean_doi = doi.replace("https://doi.org/", "").strip().lower()
            if clean_doi in seen_dois:
                is_duplicate = True
            else:
                seen_dois.add(clean_doi)
        
        if not is_duplicate:
            title = normalize_title(item.get("title", ""))
            if title:
                if title in seen_titles:
                    is_duplicate = True
                else:
                    seen_titles.add(title)
        
        if not is_duplicate:
            unique_results.append(item)
            
    return unique_results

def format_markdown_results(results: List[Dict[str, Any]], title: str) -> str:
    results = deduplicate_results(results)
    if not results: return f"No s'han trobat resultats per: **{title}**."
    
    output = [f"# {title}\n"]
    
    # Summary table
    output.append("| # | Font | Títol | Autor | Any | Cit. |")
    output.append("|---|---|---|---|---|---|")
    
    for i, r in enumerate(results):
        source = r.get('source', '???')
        title_text = r['title'][:80] + "..." if len(r['title']) > 80 else r['title']
        if r.get('url') and r['url'] != "N/A":
            title_display = f"[{title_text}]({r['url']})"
        else:
            title_display = title_text
        
        # Show first author + et al. in table for readability
        author = r.get('author', 'N/A')
        authors_list = r.get('authors_list', [])
        if authors_list and len(authors_list) > 2:
            author = f"{authors_list[0].split()[-1]} et al."
        elif len(author) > 30:
            author = author[:27] + "..."
        
        year = r.get('year', '-')
        citations = r.get('citations', '-')
        output.append(f"| {i+1} | {source} | {title_display} | {author} | {year} | {citations} |")
    
    output.append("\n---\n")
    
    # Detailed entries with full metadata
    for i, r in enumerate(results):
        output.append(f"### {i+1}. {r['title']}")
        if r.get('author'): output.append(f"- **Autors:** {r['author']}")
        if r.get('journal'): output.append(f"- **Revista:** {r['journal']}")
        vol_info = []
        if r.get('volume'): vol_info.append(f"Vol. {r['volume']}")
        if r.get('issue'): vol_info.append(f"Núm. {r['issue']}")
        fp = r.get('first_page', '')
        lp = r.get('last_page', '')
        pg = r.get('pages', '')
        if fp and lp: vol_info.append(f"pp. {fp}–{lp}")
        elif pg: vol_info.append(f"pp. {pg}")
        if vol_info: output.append(f"- **Detalls:** {', '.join(vol_info)}")
        if r.get('doi'): output.append(f"- **DOI:** {r['doi']}")
        elif r.get('url') and r['url'] != "N/A": output.append(f"- **URL:** {r['url']}")
        # Auto-generate APA 7
        if r.get('authors_list') or r.get('author'):
            apa = format_apa7_reference(r)
            output.append(f"- **APA 7:** {apa}")
        output.append("")
        
    return "\n".join(output)

def generate_mermaid_network(root_title: str, related_works: List[Dict[str, Any]], relationship: str) -> str:
    """Genera un diagrama Mermaid visualitzant la xarxa de citacions."""
    lines = ["## Mapa d'Influència Acadèmica", "```mermaid", "graph TD"]
    # Netegem el títol arrel per a Mermaid
    root_node = re.sub(r'[^a-zA-Z0-9]', '_', root_title[:20])
    lines.append(f'  {root_node}["{root_title[:50]}..."]')
    
    for i, work in enumerate(related_works):
        node_id = f"node_{i}"
        title = work['title'].replace('"', "'")
        lines.append(f'  {node_id}["{title[:50]}..."]')
        if relationship == "citations":
            lines.append(f"  {node_id} -->|cita a| {root_node}")
        else:
            lines.append(f"  {root_node} -->|referencia a| {node_id}")
            
    lines.append("```")
    return "\n".join(lines)

# --- Tool Definitions ---

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_works",
            description="Cerca articles a OpenAlex, Semantic Scholar, Google Scholar, Dialnet, Redined, ERIC, CrossRef, Europe PMC, Revista Eureka, Redalyc i BOE.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Terme de cerca"},
                    "limit": {"type": "integer", "default": 5},
                    "source": {"type": "string", "enum": ["all", "openalex", "semanticscholar", "googlescholar", "dialnet", "redined", "eric", "crossref", "europepmc", "eureka", "redalyc", "boe", "arxiv", "core", "scopus", "pubmed", "procomun", "scielo", "teseo", "gva", "wos", "roderic"], "default": "all"},
                    "year_min": {"type": "integer", "description": "Any mínim"}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_openalex",
            description="Cerca articles directament a OpenAlex (Àlies de search_works).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Terme de cerca"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="search_dialnet",
            description="Cerca articles directament a Dialnet (Àlies de search_works).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Terme de cerca"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="suggest",
            description="Amplia una consulta educativa amb terminologia acadèmica i oficial espanyola (LOMLOE, DUA, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Consulta original"}
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_work",
            description="Obtén detalls complets d'un treball per DOI o ID d'OpenAlex/SemanticScholar.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_id": {"type": "string", "description": "ID o DOI"},
                },
                "required": ["work_id"],
            },
        ),
        types.Tool(
            name="get_citations",
            description="Troba articles que citen un treball específic (DOI o ID).",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_id": {"type": "string", "description": "DOI o ID del treball"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["work_id"],
            },
        ),
        types.Tool(
            name="get_references",
            description="Troba la bibliografia (obres citades) d'un treball específic.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_id": {"type": "string", "description": "DOI o ID del treball"},
                    "limit": {"type": "integer", "default": 5}
                },
                "required": ["work_id"],
            },
        ),
        types.Tool(
            name="discover",
            description="Descobriment global en múltiples bases de dades.",
            inputSchema={
                "type": "object",
                "properties": { "query": {"type": "string"} },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="format_apa7",
            description="Genera una referència APA 7 completa a partir d'un DOI o ID d'OpenAlex. Ideal per construir bibliografies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_id": {"type": "string", "description": "DOI o ID d'OpenAlex"},
                },
                "required": ["work_id"],
            },
        ),
        types.Tool(
            name="visualize_network",
            description="Genera un diagrama Mermaid de la xarxa de citacions i referències.",
            inputSchema={
                "type": "object",
                "properties": {
                    "work_id": {"type": "string", "description": "DOI o ID del treball"}
                },
                "required": ["work_id"],
            },
        ),
        types.Tool(
            name="crossref_lookup",
            description="Obté metadades completes d'un article a partir del seu DOI via CrossRef. Retorna autors, revista, volum, pàgines i referència APA 7.",
            inputSchema={
                "type": "object",
                "properties": {
                    "doi": {"type": "string", "description": "DOI de l'article (ex: 10.1111/j.1746-1561.2008.00288.x)"},
                },
                "required": ["doi"],
            },
        ),
        types.Tool(
            name="export_bibtex",
            description="Genera entrades BibTeX a partir d'una llista de DOIs, per importar a Zotero o gestors bibliogràfics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "dois": {"type": "array", "items": {"type": "string"}, "description": "Llista de DOIs"},
                },
                "required": ["dois"],
            },
        ),
        types.Tool(
            name="unpaywall_lookup",
            description="Troba l'URL directe al PDF d'Open Access d'un article a partir del seu DOI.",
            inputSchema={
                "type": "object",
                "properties": {
                    "doi": {"type": "string", "description": "DOI de l'article"},
                },
                "required": ["doi"],
            },
        ),
        types.Tool(
            name="fetch_fulltext",
            description="Descarrega i extrau el text complet d'un article. Prioritza el MCP de Unpaywall local i usa el navegador d'incògnit com a reserva per saltar-se bloquejos.",
            inputSchema={
                "type": "object",
                "properties": {
                    "doi": {"type": "string", "description": "DOI de l'article"},
                    "title": {"type": "string", "description": "Títol de l'article (opcional)"},
                },
                "required": ["doi"],
            },
        ),
        types.Tool(
            name="firecrawl_scrape",
            description="Raspa una URL utilitzant Firecrawl per obtenir contingut en Markdown, ideal per saltar-se deteccions de bots.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL a raspar"},
                },
                "required": ["url"],
            },
        )
    ]

# --- Tool Call Handlers ---

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    oa = OpenAlexClient()
    ss = SemanticScholarClient()
    gs = GoogleScholarScraper()
    dialnet = DialnetScraper()
    redined = RedinedScraper()
    eric = EricClient()
    eureka = EurekaJournalScraper()
    redalyc = RedalycScraper()
    tdr = TDRScraper()
    crossref = CrossRefClient()
    epmc = EuropePMCClient()
    boe = BOEScraper()
    arxiv = ArxivClient()
    core = CoreClient()
    scopus = ScopusClient()
    pubmed = PubMedClient()
    procomun = ProcomunScraper()
    scielo = ScieloScraper()
    teseo = TeseoScraper()
    gva = GVAScraper()
    wos = WOSClient()
    roderic = RodericScraper()
    expander = QueryExpander()
    firecrawl = FirecrawlClient()
    
    if name == "suggest":
        query = arguments.get("query", "")
        suggestions = expander.expand(query)
        return [types.TextContent(type="text", text=f"Suggeriments per ampliar la teva recerca:\n\n" + "\n".join([f"- {s}" for s in suggestions]))]

    if name in ["search_works", "search_openalex", "search_dialnet"]:
        query = arguments.get("query")
        limit = arguments.get("limit", 5)
        
        # Determinar la font segons el nom de l'eina o l'argument
        if name == "search_openalex": source = "openalex"
        elif name == "search_dialnet": source = "dialnet"
        else: source = arguments.get("source", "all")
        
        year_min = arguments.get("year_min")

        
        tasks = []
        if source in ["all", "openalex"]:
            f = {"from_publication_date": f"{year_min}-01-01"} if year_min else None
            tasks.append(oa.search_works(query, limit, f))
        if source in ["all", "semanticscholar"]:
            tasks.append(ss.search(query, limit))
        if source in ["all", "googlescholar"]:
            tasks.append(gs.search(query, limit))
        if source in ["all", "dialnet"]:
            tasks.append(dialnet.search(query, limit))
        if source in ["all", "redined"]:
            tasks.append(redined.search(query, limit))
        if source in ["all", "eric"]:
            tasks.append(eric.search(query, limit))
        if source in ["all", "crossref"]:
            tasks.append(crossref.search(query, limit))
        if source in ["all", "europepmc"]:
            tasks.append(epmc.search(query, limit))
        if source in ["all", "eureka"]:
            tasks.append(eureka.search(query, limit))
        if source in ["all", "redalyc"]:
            tasks.append(redalyc.search(query, limit))
        if source in ["all", "boe"]:
            tasks.append(boe.search(query, limit))
        if source in ["all", "arxiv"]:
            tasks.append(arxiv.search(query, limit))
        if source in ["all", "core"]:
            tasks.append(core.search(query, limit))
        if source in ["all", "scopus"]:
            tasks.append(scopus.search(query, limit))
        if source in ["all", "pubmed"]:
            tasks.append(pubmed.search(query, limit))
        if source in ["all", "procomun"]:
            tasks.append(procomun.search(query, limit))
        if source in ["all", "scielo"]:
            tasks.append(scielo.search(query, limit))
        if source in ["all", "teseo"]:
            tasks.append(teseo.search(query, limit))
        if source in ["all", "gva"]:
            tasks.append(gva.search(query, limit))
        if source in ["all", "wos"]:
            tasks.append(wos.search(query, limit))
        if source in ["all", "roderic"]:
            tasks.append(roderic.search(query, limit))
            
        done = await asyncio.gather(*tasks, return_exceptions=True)
        final_results = []
        for res in done:
            if isinstance(res, list):
                for item in res:
                    if "display_name" in item: # OpenAlex raw result
                        all_authors = [a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])]
                        loc = item.get("primary_location") or {}
                        src_info = loc.get("source") or {}
                        biblio = item.get("biblio") or {}
                        final_results.append({
                            "title": item.get("display_name"),
                            "author": ", ".join(all_authors),
                            "authors_list": all_authors,
                            "year": item.get("publication_year"),
                            "citations": item.get("cited_by_count"),
                            "doi": item.get("doi", ""),
                            "url": item.get("doi") or item.get("id"),
                            "journal": src_info.get("display_name", ""),
                            "volume": biblio.get("volume", ""),
                            "issue": biblio.get("issue", ""),
                            "first_page": biblio.get("first_page", ""),
                            "last_page": biblio.get("last_page", ""),
                            "source": "OpenAlex"
                        })
                    else: final_results.append(item)
        
        return [types.TextContent(type="text", text=format_markdown_results(final_results, f"Recerca: {query}"))]

    elif name == "get_work":
        work_id = arguments.get("work_id")
        try:
            work = await oa.get_work(work_id)
            # Extract abstract
            abstract_idx = work.get("abstract_inverted_index", {})
            abstract = ""
            if abstract_idx:
                words = {}
                for word, indices in abstract_idx.items():
                    for idx in indices: words[idx] = word
                abstract = " ".join([words[i] for i in sorted(words.keys())])
            # Extract full metadata
            all_authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])]
            loc = work.get("primary_location") or {}
            src_info = loc.get("source") or {}
            biblio = work.get("biblio") or {}
            doi = work.get("doi", "")
            # Format APA 7 reference
            apa_ref = format_apa7_reference({
                "authors_list": all_authors,
                "year": work.get("publication_year"),
                "title": work.get("display_name"),
                "journal": src_info.get("display_name", ""),
                "volume": biblio.get("volume", ""),
                "issue": biblio.get("issue", ""),
                "first_page": biblio.get("first_page", ""),
                "last_page": biblio.get("last_page", ""),
                "doi": doi
            })
            output = [
                f"# {work.get('display_name')}",
                f"",
                f"**Autors:** {', '.join(all_authors)}",
                f"**Any:** {work.get('publication_year')}",
                f"**Revista:** {src_info.get('display_name', 'N/A')}",
                f"**DOI:** {doi or 'N/A'}",
                f"**Citacions:** {work.get('cited_by_count')}",
                f"**Volum:** {biblio.get('volume', 'N/A')} | **Número:** {biblio.get('issue', 'N/A')} | **Pàgines:** {biblio.get('first_page', '')}-{biblio.get('last_page', '')}",
                f"",
                f"## Abstract",
                f"{abstract if abstract else 'No disponible'}",
                f"",
                f"## Referència APA 7",
                f"{apa_ref}",
                f"",
                f"[Enllaç OpenAlex]({work.get('id')})"
            ]
            return [types.TextContent(type="text", text="\n".join(output))]
        except Exception as e:
            return [types.TextContent(type="text", text=f"No s'han pogut carregar els detalls: {e}")]

    elif name == "discover":
        query = arguments.get("query")
        res_gs = await gs.search(query, 2)
        res_ss = await ss.search(query, 2)
        res_red = await redined.search(query, 2)
        res_eric = await eric.search(query, 2)
        res_eur = await eureka.search(query, 2)
        res_cr = await crossref.search(query, 2)
        res_epmc = await epmc.search(query, 2)
        res_boe = await boe.search(query, 2)
        res_arxiv = await arxiv.search(query, 2)
        res_core = await core.search(query, 2)
        res_scopus = await scopus.search(query, 2)
        res_pubmed = await pubmed.search(query, 2)
        res_pro = await procomun.search(query, 2)
        res_sci = await scielo.search(query, 2)
        res_tes = await teseo.search(query, 2)
        res_gva = await gva.search(query, 2)
        
        final = res_gs + res_ss + res_red + res_eric + res_eur + res_cr + res_epmc + res_boe + res_arxiv + res_core + res_scopus + res_pubmed + res_pro + res_sci + res_tes + res_gva
        return [types.TextContent(type="text", text=format_markdown_results(final, f"Descobriment: {query}"))]

    elif name == "format_apa7":
        work_id = arguments.get("work_id")
        try:
            work = await oa.get_work(work_id)
            all_authors = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])]
            loc = work.get("primary_location") or {}
            src_info = loc.get("source") or {}
            biblio = work.get("biblio") or {}
            apa = format_apa7_reference({
                "authors_list": all_authors,
                "year": work.get("publication_year"),
                "title": work.get("display_name"),
                "journal": src_info.get("display_name", ""),
                "volume": biblio.get("volume", ""),
                "issue": biblio.get("issue", ""),
                "first_page": biblio.get("first_page", ""),
                "last_page": biblio.get("last_page", ""),
                "doi": work.get("doi", "")
            })
            return [types.TextContent(type="text", text=f"## Referència APA 7\n\n{apa}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error generant referència APA 7: {e}")]

    elif name == "get_citations":
        work_id = arguments.get("work_id")
        limit = arguments.get("limit", 5)
        
        results = []
        try:
            results = await ss.get_citations(work_id, limit)
        except Exception: pass
        
        if not results:
            try:
                oa_res = await oa.get_citations(work_id, limit)
                for item in oa_res:
                    all_authors = [a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])]
                    loc = item.get("primary_location") or {}
                    src_info = loc.get("source") or {}
                    biblio = item.get("biblio") or {}
                    results.append({
                        "title": item.get("display_name"),
                        "author": ", ".join(all_authors),
                        "authors_list": all_authors,
                        "year": item.get("publication_year"),
                        "citations": item.get("cited_by_count"),
                        "doi": item.get("doi", ""),
                        "url": item.get("doi") or item.get("id"),
                        "journal": src_info.get("display_name", ""),
                        "volume": biblio.get("volume", ""),
                        "issue": biblio.get("issue", ""),
                        "first_page": biblio.get("first_page", ""),
                        "last_page": biblio.get("last_page", ""),
                        "source": "OpenAlex"
                    })
            except Exception: pass
            
        return [types.TextContent(type="text", text=format_markdown_results(results, f"Citacions de: {work_id}"))]

    elif name == "get_references":
        work_id = arguments.get("work_id")
        limit = arguments.get("limit", 5)
        
        results = []
        try:
            results = await ss.get_references(work_id, limit)
        except Exception: pass
        
        if not results:
            try:
                oa_res = await oa.get_references(work_id, limit)
                for item in oa_res:
                    all_authors = [a.get("author", {}).get("display_name", "") for a in item.get("authorships", [])]
                    loc = item.get("primary_location") or {}
                    src_info = loc.get("source") or {}
                    biblio = item.get("biblio") or {}
                    results.append({
                        "title": item.get("display_name"),
                        "author": ", ".join(all_authors),
                        "authors_list": all_authors,
                        "year": item.get("publication_year"),
                        "citations": item.get("cited_by_count"),
                        "doi": item.get("doi", ""),
                        "url": item.get("doi") or item.get("id"),
                        "journal": src_info.get("display_name", ""),
                        "volume": biblio.get("volume", ""),
                        "issue": biblio.get("issue", ""),
                        "first_page": biblio.get("first_page", ""),
                        "last_page": biblio.get("last_page", ""),
                        "source": "OpenAlex"
                    })
            except Exception: pass
            
        return [types.TextContent(type="text", text=format_markdown_results(results, f"Bibliografia de: {work_id}"))]

    elif name == "visualize_network":
        work_id = arguments.get("work_id")
        limit = 4
        
        cites = await ss.get_citations(work_id, limit)
        if not cites:
            oa_cites = await oa.get_citations(work_id, limit)
            cites = [{"title": w.get("display_name"), "year": w.get("publication_year")} for w in oa_cites]
            
        refs = await ss.get_references(work_id, limit)
        if not refs:
            oa_refs = await oa.get_references(work_id, limit)
            refs = [{"title": w.get("display_name"), "year": w.get("publication_year")} for w in oa_refs]
            
        root_title = "Article Principal"
        try:
            work_info = await oa.get_work(work_id)
            root_title = work_info.get("display_name", "Article Principal")
        except Exception: pass
        
        mermaid_cites = generate_mermaid_network(root_title, cites, "citations")
        mermaid_refs = generate_mermaid_network(root_title, refs, "references")
        
        return [types.TextContent(type="text", text=f"# Xarxa d'Influència Acadèmica\n\n{mermaid_cites}\n\n{mermaid_refs}")]

    elif name == "crossref_lookup":
        doi = arguments.get("doi")
        try:
            item = await crossref.lookup_doi(doi)
            apa = format_apa7_reference(item)
            output = [
                f"# {item['title']}",
                f"",
                f"**Autors:** {item['author']}",
                f"**Any:** {item['year']}",
                f"**Revista:** {item['journal']}",
                f"**DOI:** {item['doi']}",
                f"**Volum:** {item.get('volume', 'N/A')} | **Número:** {item.get('issue', 'N/A')} | **Pàgines:** {item.get('pages', 'N/A')}",
                f"**Citacions CrossRef:** {item.get('citations', 0)}",
                f"**Editorial:** {item.get('publisher', 'N/A')}",
                f"",
                f"## Referència APA 7",
                f"{apa}",
            ]
            return [types.TextContent(type="text", text="\n".join(output))]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error consultant CrossRef: {e}")]

    elif name == "export_bibtex":
        dois = arguments.get("dois", [])
        entries = []
        for doi in dois:
            try:
                item = await crossref.lookup_doi(doi)
                authors_list = item.get("authors_list", [])
                # Generate citation key: FirstAuthorLastNameYear
                if authors_list:
                    first_author = authors_list[0].split()[-1] if " " in authors_list[0] else authors_list[0].split(",")[0]
                else:
                    first_author = "Unknown"
                year = item.get("year", "nd")
                citekey = f"{first_author}{year}"
                
                # Format BibTeX authors
                bibtex_authors = " and ".join(authors_list)
                
                entry = [
                    f"@article{{{citekey},",
                    f"  title = {{{item.get('title', '')}}},",
                    f"  author = {{{bibtex_authors}}},",
                    f"  journal = {{{item.get('journal', '')}}},",
                    f"  year = {{{year}}},",
                ]
                if item.get("volume"): entry.append(f"  volume = {{{item['volume']}}},")
                if item.get("issue"): entry.append(f"  number = {{{item['issue']}}},")
                if item.get("pages"): entry.append(f"  pages = {{{item['pages']}}},")
                entry.append(f"  doi = {{{item.get('doi', '').replace('https://doi.org/', '')}}},")
                if item.get("publisher"): entry.append(f"  publisher = {{{item['publisher']}}},")
                entry.append("}")
                entries.append("\n".join(entry))
            except Exception as e:
                entries.append(f"% Error for DOI {doi}: {e}")
        
        bibtex_output = "\n\n".join(entries)
        return [types.TextContent(type="text", text=f"```bibtex\n{bibtex_output}\n```")]

    elif name == "unpaywall_lookup":
        doi = arguments.get("doi")
        try:
            unpaywall = UnpaywallClient()
            pdf_url = await unpaywall.get_pdf_url(doi)
            if pdf_url:
                return [types.TextContent(type="text", text=f"PDF d'Open Access disponible a: {pdf_url}")]
            else:
                return [types.TextContent(type="text", text=f"No s'ha trobat cap PDF d'Open Access per al DOI {doi} via Unpaywall.")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error consultant Unpaywall: {e}")]

    elif name == "fetch_fulltext":
        doi = arguments.get("doi")
        title = arguments.get("title", "")
        
        # 0. Comprovar CACHE local (Política de no baixar dues vegades)
        cached_data = FulltextRetriever.check_cache(doi)
        if cached_data:
            text_content = cached_data["text"]
            if arguments.get("truncate_chars"):
                text_content = text_content[:arguments["truncate_chars"]] + "..."
            
            return [types.TextContent(type="text", text=json.dumps({
                "status": "success",
                "method": "local_cache",
                "doi": doi,
                "metadata": cached_data.get("metadata", {}),
                "text": text_content,
                "download_date": cached_data.get("download_date")
            }, indent=2))]

        # 1. Preferència: MCP local de Unpaywall (més ràpid i net)
        results = await FulltextRetriever.call_local_unpaywall_mcp(doi)
        
        if "text" in results and results["text"]:
            # Èxit via Unpaywall MCP - Guardar a cache
            results["method"] = "unpaywall_mcp"
            FulltextRetriever.save_to_cache(doi, results)
            
            text_content = results["text"]
            if arguments.get("truncate_chars"):
                text_content = text_content[:arguments["truncate_chars"]] + "..."
            
            return [types.TextContent(type="text", text=json.dumps({
                "status": "success",
                "method": "unpaywall_mcp",
                "doi": doi,
                "metadata": results.get("metadata", {}),
                "text": text_content
            }, indent=2))]
            
        # 2. Reserva: Descàrrega via Navegador (StealthBrowser)
        finder = FulltextFinder()
        discovery = await finder.find(doi, title)
        
        if discovery.get("official_url"):
            browser_results = await FulltextRetriever.retrieve_via_browser(discovery["official_url"])
            
            if "text" in browser_results and browser_results["text"]:
                # Èxit via Navegador - Guardar a cache
                browser_results["method"] = "stealth_browser"
                FulltextRetriever.save_to_cache(doi, browser_results)
                
                text_content = browser_results["text"]
                if arguments.get("truncate_chars"):
                    text_content = text_content[:arguments["truncate_chars"]] + "..."
                    
                return [types.TextContent(type="text", text=json.dumps({
                    "status": "success",
                    "method": "stealth_browser",
                    "url": discovery["official_url"],
                    "metadata": browser_results.get("metadata", {}),
                    "text": text_content
                }, indent=2))]
            else:
                error_msg = browser_results.get("error", "Error desconegut en el navegador.")
        else:
            error_msg = "No s'ha trobat cap URL d'Open Access per descarregar."
            
        # 3. Si tot falla
        discovery["error"] = error_msg
        return [types.TextContent(type="text", text=json.dumps({
            "status": "failed",
            "error": error_msg,
            "discovery_data": discovery
        }, indent=2))]

    elif name == "firecrawl_scrape":
        url = arguments.get("url")
        try:
            markdown = await firecrawl.scrape_url(url)
            return [types.TextContent(type="text", text=f"# Contingut raspat de {url}\n\n{markdown}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error amb Firecrawl: {e}")]

    raise ValueError(f"Eina no trobada: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, InitializationOptions(
            server_name="academic-spain-education-mcp", server_version="2.1.0",
            capabilities=server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={})
        ))

if __name__ == "__main__":
    asyncio.run(main())

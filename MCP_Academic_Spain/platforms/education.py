from typing import List
import httpx
import re
from bs4 import BeautifulSoup
from .base import PaperSource
from .models import Paper

class EricSearcher(PaperSource):
    """ERIC - Education Resources Information Center."""
    BASE_URL = "https://api.ies.ed.gov/eric"

    async def search(self, query: str, limit: int = 5, **kwargs) -> List[Paper]:
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
                    authors_list = authors_raw if isinstance(authors_raw, list) else ([authors_raw] if authors_raw else [])
                    
                    output.append(Paper(
                        paper_id=item.get("id", ""),
                        title=item.get("title", "Sense títol"),
                        authors=authors_list,
                        published_date=str(item.get("publicationdateyear") or item.get("pubyear", "")),
                        url=f"https://eric.ed.gov/?id={item.get('id')}" if item.get('id') else "https://eric.ed.gov/",
                        journal=item.get("source", ""),
                        abstract=item.get("description", ""),
                        source="ERIC"
                    ))
                return output
            except Exception:
                return []

class EurekaSearcher(PaperSource):
    """Revista Eureka sobre Enseñanza y Divulgación de las Ciencias."""
    BASE_URL = "https://revistas.uca.es/index.php/eureka/search/index"
    
    async def search(self, query: str, limit: int = 5, **kwargs) -> List[Paper]:
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
                    
                    year = "N/A"
                    if date_el:
                        year_match = re.search(r"\d{4}", date_el.get_text())
                        if year_match:
                            year = year_match[0]
                            
                    output.append(Paper(
                        paper_id=title_el["href"].split("/")[-1] if title_el else "eureka-" + str(len(output)),
                        title=title_el.get_text(strip=True) if title_el else "N/A",
                        authors=[author_el.get_text(strip=True)] if author_el else [],
                        published_date=year,
                        url=title_el["href"] if title_el else "https://revistas.uca.es/index.php/eureka/",
                        source="RevistaEureka"
                    ))
                return output
            except Exception:
                return []

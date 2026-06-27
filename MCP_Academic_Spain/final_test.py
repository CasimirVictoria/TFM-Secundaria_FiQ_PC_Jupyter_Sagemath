import asyncio
import sys
import os

# Afegim el directori actual al path per importar server
sys.path.append(os.getcwd())

from server import EurekaJournalScraper, RedalycScraper, TDRScraper, OpenAlexClient, SemanticScholarClient, format_markdown_results

async def test_all():
    print("🚀 Iniciant proves de validació FINAL...")
    
    # 1. Prova Revista Eureka
    print("\n--- Revista Eureka ---")
    eureka = EurekaJournalScraper()
    res = await eureka.search("pensamiento computacional", limit=2)
    print(f"Trobats: {len(res)}")
    for r in res: print(f"- {r['title']} ({r['year']})")

    # 2. Prova TDR (Tesis)
    print("\n--- TDR (Tesis Doctorals) ---")
    tdr = TDRScraper()
    res = await tdr.search("fisica pensamiento computacional", limit=1)
    print(f"Trobats: {len(res)}")
    for r in res: print(f"- {r['title']} ({r['author']})")

    # 3. Prova Citacions (Semantic Scholar)
    print("\n--- Citacions (Semantic Scholar) ---")
    ss = SemanticScholarClient()
    # DOI d'un article molt citat sobre Pensament Computacional (Wing 2006)
    doi = "10.1145/1118178.1118215"
    res = await ss.get_citations(doi, limit=3)
    print(f"Citacions trobades: {len(res)}")
    for r in res: print(f"- Citat per: {r['title']}")

    # 4. Prova format TAULA
    print("\n--- Validació de Formateig (Taula) ---")
    test_data = [
        {"title": "Article de Prova 1", "author": "Autor A", "year": "2024", "citations": 10, "source": "Test", "url": "http://example.com/1"},
        {"title": "Article de Prova 2 amb un títol molt llarg per comprovar el truncament que hem implementat a la taula", "author": "Autor B", "year": "2023", "citations": 5, "source": "Test", "url": "http://example.com/2"}
    ]
    markdown = format_markdown_results(test_data, "Test Taula")
    print("Markdown generat:")
    print(markdown)

if __name__ == "__main__":
    asyncio.run(test_all())

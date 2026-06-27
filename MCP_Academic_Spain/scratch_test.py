import httpx
from bs4 import BeautifulSoup

def test_tdr():
    print("Testing TDR (TDX.cat)...")
    url = "https://www.tdx.cat/discover?query=pensamiento+computacional"
    with httpx.Client(follow_redirects=True, timeout=30.0) as client:
        response = client.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            items = soup.select(".ds-artifact-item")
            print(f"Found {len(items)} items.")
            for item in items[:3]:
                title_el = item.select_one(".artifact-title a")
                title = title_el.get_text(strip=True) if title_el else "N/A"
                link = title_el["href"] if title_el else "N/A"
                print(f"- {title} | https://www.tdx.cat{link}")

if __name__ == "__main__":
    test_tdr()

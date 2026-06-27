import asyncio
from playwright.async_api import async_playwright

async def test():
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            print("Navegador obert correctament")
            page = await browser.new_page()
            await page.goto("https://dialnet.unirioja.es")
            title = await page.title()
            print(f"Títol de la pàgina: {title}")
            await browser.close()
            print("Navegador tancat")
    except Exception as e:
        print(f"Error en Playwright: {e}")

if __name__ == "__main__":
    asyncio.run(test())

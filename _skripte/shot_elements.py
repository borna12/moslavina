import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto('http://127.0.0.1:8765/gora.html', wait_until='networkidle')
        await page.wait_for_timeout(300)
        fig = page.locator('figure.figure').first
        await fig.scroll_into_view_if_needed()
        await page.wait_for_timeout(300)
        await fig.screenshot(path='_tekst/shots/cross-section.png')

        await page.goto('http://127.0.0.1:8765/staza.html', wait_until='networkidle')
        await page.wait_for_timeout(300)
        mp = page.locator('.map-card')
        await mp.screenshot(path='_tekst/shots/map.png')
        await b.close()

asyncio.run(main())

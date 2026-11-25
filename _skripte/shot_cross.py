import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        for w, h, name in [(1440, 1000, 'cross3'), (390, 844, 'cross3-m')]:
            page = await b.new_page(viewport={'width': w, 'height': h})
            await page.goto('http://127.0.0.1:8765/krizaljka.html', wait_until='networkidle')
            await page.add_style_tag(content='.site-header{position:static!important}.reveal{opacity:1!important;animation:none!important}')
            await page.wait_for_timeout(250)
            await page.screenshot(path=f'_tekst/shots/{name}.png', full_page=True)
            await page.close()
        await b.close()

asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await browser.new_page(viewport={'width': 1440, 'height': 1000})
        await page.goto('http://127.0.0.1:8765/staza.html', wait_until='networkidle')
        await page.add_style_tag(content='.site-header{position:static!important}.reveal{opacity:1!important;animation:none!important;transform:none!important}')
        await page.wait_for_timeout(300)
        await page.screenshot(path='_tekst/shots/staza2.png', full_page=True)
        await browser.close()

asyncio.run(main())

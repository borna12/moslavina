import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await b.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
        await page.goto('http://127.0.0.1:8766/index.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        await page.screenshot(path='assets/img/og-cover.png')
        await b.close()

asyncio.run(main())

import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await b.new_page(viewport={'width': 1440, 'height': 1000})
        await page.goto('http://127.0.0.1:8765/index.html', wait_until='networkidle')
        vals = await page.eval_on_selector_all('.stat__num', 'els => els.map(e => e.textContent)')
        print(vals)
        await page.locator('.stat-strip').screenshot(path='_tekst/stats.png')
        await b.close()

asyncio.run(main())

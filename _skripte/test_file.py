import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        await page.goto('file:///C:/posao/radovi/moslvačka%20gora/index.html', wait_until='load')
        await page.wait_for_timeout(800)
        print('title', await page.title())
        print('games', await page.locator('.game-card').count())
        print('errors', errs[:5])
        await page.click('.nav-toggle') if await page.locator('.nav-toggle').is_visible() else None
        await b.close()

asyncio.run(main())

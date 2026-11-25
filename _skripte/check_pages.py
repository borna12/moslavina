import asyncio
from playwright.async_api import async_playwright

PAGES = ['index.html', 'gora.html', 'zivi-svijet.html', 'povijest.html', 'staza.html', 'igre.html', 'izvori.html',
         'igre/kviz.html?k=stijene', 'igre/kviz.html?k=biljke', 'igre/kviz.html?k=zivotinje', 'igre/kviz.html?k=cinjenice',
         'krizaljka.html']

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        errors = []
        page.on('console', lambda m: errors.append(('console', m.type, m.text)) if m.type in ('error', 'warning') else None)
        page.on('pageerror', lambda e: errors.append(('pageerror', str(e))))
        page.on('response', lambda r: errors.append(('http', r.status, r.url)) if r.status >= 400 else None)
        for path in PAGES:
            await page.goto('http://127.0.0.1:8766/' + path, wait_until='networkidle')
            await page.wait_for_timeout(250)
            t = await page.title()
            print('OK', path, '|', t)
        print('--- issues ---')
        for e in errors:
            print(e)
        await b.close()

asyncio.run(main())

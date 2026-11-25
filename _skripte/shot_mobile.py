import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        m = await b.new_page(viewport={'width': 390, 'height': 844})
        await m.goto('http://127.0.0.1:8765/index.html', wait_until='networkidle')
        await m.add_style_tag(content='.site-header{position:static!important}.reveal{opacity:1!important;animation:none!important;transform:none!important}')
        for i, y in enumerate([0, 700, 1400]):
            await m.evaluate(f'window.scrollTo(0,{y})')
            await m.wait_for_timeout(200)
            await m.screenshot(path=f'_tekst/shots/m-index-{i}.png')
        await b.close()

asyncio.run(main())

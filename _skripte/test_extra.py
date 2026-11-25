import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto('http://127.0.0.1:8765/igre/kviz.html?k=cinjenice', wait_until='networkidle')
        await page.click('#quiz-start')
        n = await page.evaluate('window.KVIZOVI.cinjenice.pitanja.length')
        for i in range(n):
            a = await page.evaluate(f'window.KVIZOVI.cinjenice.pitanja[{i}].a')
            await page.click(f'.quiz-option[data-i="{a}"]')
            await page.click('#quiz-next')
        await page.wait_for_timeout(300)
        print('TRUE/FALSE:', (await page.inner_text('.result__score')).replace('\n', ' '))

        m = await b.new_page(viewport={'width': 390, 'height': 844})
        await m.goto('http://127.0.0.1:8765/index.html', wait_until='networkidle')
        await m.click('.nav-toggle')
        open1 = await m.get_attribute('#site-nav', 'class')
        await m.click('.nav-toggle')
        open2 = await m.get_attribute('#site-nav', 'class')
        print('MENU:', open1, '->', open2)
        await b.close()

asyncio.run(main())

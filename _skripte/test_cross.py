import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8765/'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await browser.new_page(viewport={'width': 1280, 'height': 1000})

        # question view
        await page.goto(BASE + 'igre/kviz.html?k=biljke', wait_until='networkidle')
        await page.click('#quiz-start')
        await page.screenshot(path='_tekst/shots/quiz-question.png', full_page=True)
        await page.click('.quiz-option[data-i="0"]')
        await page.wait_for_timeout(300)
        await page.screenshot(path='_tekst/shots/quiz-feedback.png', full_page=True)

        # crossword solved
        await page.goto(BASE + 'krizaljka.html', wait_until='networkidle')
        await page.evaluate("""
          () => {
            const sol = window.KRIZALJKA.grid;
            document.querySelectorAll('.cross-cell input').forEach(inp => {
              const r = +inp.dataset.r, c = +inp.dataset.c;
              inp.value = sol[r][c];
              inp.dispatchEvent(new Event('input', {bubbles:true}));
            });
          }
        """)
        await page.click('#cross-check')
        await page.wait_for_timeout(400)
        status = await page.inner_text('#cross-status')
        print('CROSS status:', status)
        await page.screenshot(path='_tekst/shots/cross-solved.png', full_page=True)
        await browser.close()

asyncio.run(main())

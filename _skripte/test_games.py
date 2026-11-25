import asyncio
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8765/'

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await browser.new_page(viewport={'width': 1280, 'height': 1000})

        # --- quiz full run ---
        await page.goto(BASE + 'igre/kviz.html?k=stijene', wait_until='networkidle')
        await page.click('#quiz-start')
        n = await page.evaluate('window.KVIZOVI.stijene.pitanja.length')
        for i in range(n):
            correct = await page.evaluate(f'window.KVIZOVI.stijene.pitanja[{i}].a')
            await page.click(f'.quiz-option[data-i="{correct}"]')
            await page.click('#quiz-next')
        await page.wait_for_timeout(500)
        score = await page.inner_text('.result__score')
        print('QUIZ score:', score.replace('\n', ' '))
        await page.screenshot(path='_tekst/shots/quiz-result.png', full_page=True)

        # --- crossword solve ---
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
        await page.wait_for_timeout(300)
        status = await page.inner_text('#cross-status')
        print('CROSS status:', status)
        await page.screenshot(path='_tekst/shots/cross-solved.png', full_page=True)

        # --- crossword wrong letter path ---
        await page.goto(BASE + 'krizaljka.html', wait_until='networkidle')
        await page.evaluate("""
          () => {
            const inp = document.querySelector('.cross-cell input');
            inp.value = 'X';
            inp.dispatchEvent(new Event('input', {bubbles:true}));
          }
        """)
        await page.click('#cross-check')
        print('CROSS wrong:', await page.inner_text('#cross-status'))

        await browser.close()

asyncio.run(main())

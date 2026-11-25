import asyncio, os
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:8765/'
PAGES = ['index.html', 'gora.html', 'zivi-svijet.html', 'povijest.html', 'staza.html', 'igre.html', 'izvori.html', 'igre/kviz.html?k=stijene', 'krizaljka.html']

STYLE = """
  .site-header { position: static !important; }
  .reveal, .reveal.is-in { opacity: 1 !important; animation: none !important; transform: none !important; }
"""

SCROLL = """
async () => {
  const h = document.body.scrollHeight;
  for (let y = 0; y < h; y += 400) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 40));
  }
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 200));
}
"""

async def main():
    os.makedirs('_tekst/shots', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=r'C:\Program Files\Google\Chrome\Application\chrome.exe')
        page = await browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
        for path in PAGES:
            name = path.replace('/', '_').replace('?', '_').replace('=', '-').replace('.html', '')
            await page.goto(BASE + path, wait_until='networkidle')
            await page.add_style_tag(content=STYLE)
            await page.wait_for_timeout(250)
            await page.screenshot(path=f'_tekst/shots/{name}.png', full_page=True)
            print(name, await page.evaluate('document.body.scrollHeight'))

        # mobile
        m = await browser.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=1)
        for path, name in [('index.html', 'm-index'), ('zivi-svijet.html', 'm-zivi'), ('staza.html', 'm-staza'), ('krizaljka.html', 'm-krizaljka')]:
            await m.goto(BASE + path, wait_until='networkidle')
            await m.add_style_tag(content=STYLE)
            await m.wait_for_timeout(250)
            await m.screenshot(path=f'_tekst/shots/{name}.png', full_page=True)
            print(name, await m.evaluate('document.body.scrollHeight'))
        await browser.close()

asyncio.run(main())

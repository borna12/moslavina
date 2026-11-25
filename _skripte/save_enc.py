import json, re, html

enc = json.load(open('_tekst/enc_pages.json', encoding='utf-8'))
for slug, title in [('moslavacka-gora', 'Moslavačka gora'), ('moslavina', 'Moslavina')]:
    h = enc[slug]
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    body = re.sub(r'<[^>]+>', '\n', body)
    body = html.unescape(body)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in body.split('\n')]
    lines = [l for l in lines if l]
    txt = '\n'.join(lines)
    start = txt.find('struka(e)')
    end = txt.find('Citiranje:')
    article = txt[start:end].strip()
    # strip leading heading remnants
    out = (f'{title}\nHrvatska enciklopedija, mrežno izdanje. Leksikografski zavod Miroslav Krleža.\n'
           f'https://www.enciklopedija.hr/clanak/{slug}\n'
           f'Pristupljeno: 25. 11. 2026.\n\n{article}\n')
    fn = f'izvori/enciklopedija_{slug}.txt'
    open(fn, 'w', encoding='utf-8').write(out)
    print(fn, len(out))

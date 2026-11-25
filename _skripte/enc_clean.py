import json, re, html

enc = json.load(open('_tekst/enc_pages.json', encoding='utf-8'))
out = []
for slug in ['moslavacka-gora', 'moslavina']:
    h = enc[slug]
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    body = re.sub(r'<[^>]+>', '\n', body)
    body = html.unescape(body)
    lines = [re.sub(r'\s+', ' ', l).strip() for l in body.split('\n')]
    lines = [l for l in lines if l]
    # cut everything before the article lead (approx)
    txt = '\n'.join(lines)
    start = txt.find('struka(e)')
    end = txt.find('Citiranje:')
    out.append(f'### {slug}\n' + txt[start:end])
open('_tekst/enciklopedija_tekst.txt', 'w', encoding='utf-8').write('\n\n'.join(out))
print(open('_tekst/enciklopedija_tekst.txt', encoding='utf-8').read())

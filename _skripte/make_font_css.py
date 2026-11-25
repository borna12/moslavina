import urllib.request, re

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
families = {
    'fraunces': ('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..800&display=swap', ['latin-ext', 'latin'], {'latin-ext': 1, 'latin': 2}),
    'inter': ('https://fonts.googleapis.com/css2?family=Inter:wght@300..700&display=swap', ['latin-ext', 'latin'], {'latin-ext': 5, 'latin': 6}),
}
blocks = []
for name, (url, wanted, idx) in families.items():
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    css = urllib.request.urlopen(req, timeout=45).read().decode('utf-8')
    for m in re.finditer(r'/\* ([a-z-]+) \*/\s*(@font-face\s*\{.*?\})', css, re.S):
        subset, block = m.group(1), m.group(2)
        if subset not in wanted:
            continue
        i = idx[subset]
        block = re.sub(r'url\(https://[^)]+\)', f'url(../fonts/{name}-{i}.woff2)', block)
        block = block.replace('font-family: \'%s\'' % name.capitalize(), f"font-family: '{name.capitalize()}'")
        blocks.append(f'/* {name} {subset} */\n' + block)
open('assets/css/fonts.css', 'w', encoding='utf-8').write('\n'.join(blocks))
print('\n'.join(blocks)[:1500])

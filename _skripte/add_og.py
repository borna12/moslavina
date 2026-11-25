import glob, io, os, re, html

BASE = 'https://borna12.github.io/moslavina/'
for p in glob.glob('*.html') + glob.glob('igre/*.html'):
    s = io.open(p, encoding='utf-8').read()
    if 'property="og:title"' in s:
        continue
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', s, re.S)
    title = html.unescape(t.group(1)).strip() if t else 'Moslavina'
    desc = html.unescape(d.group(1)).strip() if d else ''
    rel = p.replace('\\', '/')
    url = BASE + ('' if rel == 'index.html' else rel)
    block = (
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:site_name" content="Moslavina — edukativni portal">\n'
        f'  <meta property="og:title" content="{html.escape(title, quote=True)}">\n'
        f'  <meta property="og:description" content="{html.escape(desc, quote=True)}">\n'
        f'  <meta property="og:url" content="{url}">\n'
        '  <meta property="og:image" content="' + BASE + 'assets/img/og-cover.png">\n'
        '  <meta property="og:image:width" content="1200">\n'
        '  <meta property="og:image:height" content="630">\n'
        '  <meta property="og:image:alt" content="Naslovnica portala Moslavina: ilustracija Moslavačke gore">\n'
        '  <meta property="og:locale" content="hr_HR">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
    )
    if 'kviz.html' not in rel:
        block += f'  <link rel="canonical" href="{url}">\n'
    # insert after description meta (or viewport if no description)
    marker = re.search(r'<meta name="description" content=".*?">\n', s, re.S)
    if marker:
        pos = marker.end()
        s = s[:pos] + block + s[pos:]
    else:
        marker2 = '<meta name="theme-color" content="#1b3a2d">\n'
        pos = s.find(marker2) + len(marker2)
        s = s[:pos] + block + s[pos:]
    io.open(p, 'w', encoding='utf-8').write(s)
    print('og', p)

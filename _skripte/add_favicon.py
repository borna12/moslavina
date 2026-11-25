import glob, io, os

for p in glob.glob('*.html') + glob.glob('igre/*.html'):
    s = io.open(p, encoding='utf-8').read()
    if 'rel="icon"' in s:
        continue
    prefix = '../' if os.path.dirname(p) else ''
    link = f'  <link rel="icon" href="{prefix}assets/img/favicon.svg" type="image/svg+xml">\n'
    marker = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    s = s.replace(marker, marker + link, 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('icon', p)

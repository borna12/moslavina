import glob, io

for p in glob.glob('*.html') + glob.glob('igre/*.html'):
    s = io.open(p, encoding='utf-8').read()
    if 'name="theme-color"' in s:
        continue
    marker = '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
    s = s.replace(marker, marker + '  <meta name="theme-color" content="#1b3a2d">\n', 1)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('theme', p)

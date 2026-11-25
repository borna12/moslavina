import glob, io

MAP = {
    '\u0430': 'a', '\u0435': 'e', '\u043e': 'o', '\u0440': 'p', '\u0441': 'c',
    '\u0443': 'y', '\u0445': 'x', '\u0410': 'A', '\u0415': 'E', '\u041e': 'O',
    '\u0420': 'P', '\u0421': 'C', '\u0423': 'Y', '\u0425': 'X', '\u041a': 'K',
    '\u041c': 'M', '\u041d': 'H', '\u0422': 'T', '\u0412': 'B',
}
for p in glob.glob('*.html') + glob.glob('assets/**/*.js', recursive=True) + glob.glob('assets/**/*.css', recursive=True) + glob.glob('assets/**/*.svg', recursive=True):
    s = io.open(p, encoding='utf-8').read()
    orig = s
    for k, v in MAP.items():
        s = s.replace(k, v)
    if s != orig:
        io.open(p, 'w', encoding='utf-8').write(s)
        print('fixed', p)

# typo fixes
fixes = {
    'assets/js/data/kvizovi.js': [('amfibolii', 'amfibolitu')],
    'assets/js/trail.js': [('Moss i sjever', 'Mahovina i sjever')],
}
for p, pairs in fixes.items():
    s = io.open(p, encoding='utf-8').read()
    for a, b in pairs:
        s = s.replace(a, b)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('typo', p)

# remaining cyrillic report
for p in glob.glob('*.html') + glob.glob('assets/**/*.js', recursive=True):
    s = io.open(p, encoding='utf-8').read()
    bad = sorted({c for c in s if '\u0400' <= c <= '\u04FF'})
    if bad:
        print('STILL', p, [hex(ord(c)) for c in bad])

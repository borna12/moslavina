import glob, io, re

for p in glob.glob('*.html') + glob.glob('assets/**/*.js', recursive=True) + glob.glob('assets/**/*.css', recursive=True) + glob.glob('assets/**/*.svg', recursive=True):
    s = io.open(p, encoding='utf-8').read()
    bad = [(i, c) for i, c in enumerate(s) if '\u0400' <= c <= '\u04FF']
    if bad:
        print(p, '->', [(i, c, hex(ord(c))) for i, c in bad[:10]])
        for i, c in bad:
            pass

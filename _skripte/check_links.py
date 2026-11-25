import glob, os, re, io, urllib.parse

root = os.getcwd()
errors = []
for p in glob.glob('*.html') + glob.glob('igre/*.html'):
    s = io.open(p, encoding='utf-8').read()
    base = os.path.dirname(p)
    for url in re.findall(r'(?:href|src)="([^"]+)"', s):
        if url.startswith(('http://', 'https://', 'mailto:', '#', 'data:')):
            continue
        path = urllib.parse.unquote(url.split('#')[0].split('?')[0])
        if not path:
            continue
        target = os.path.normpath(os.path.join(base, path))
        if not os.path.exists(target):
            errors.append((p, url, target))

print('errors:', len(errors))
for e in errors:
    print(e)

# check all images referenced exist and all illustration files used
used = set()
for p in glob.glob('*.html') + glob.glob('igre/*.html') + glob.glob('assets/js/*.js') + glob.glob('assets/css/*.css'):
    s = io.open(p, encoding='utf-8').read()
    for m in re.findall(r'([\w\-./]+\.(?:png|jpg|svg|woff2|css|js))', s):
        used.add(os.path.basename(m))
unused = [f for f in glob.glob('assets/img/ilustracije/*.png') if os.path.basename(f) not in used]
print('unused illustrations:', [os.path.basename(u) for u in unused])

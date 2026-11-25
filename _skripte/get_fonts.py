import urllib.request, re, os

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
os.makedirs('assets/fonts', exist_ok=True)

families = {
    'fraunces': 'https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..800&display=swap',
    'inter': 'https://fonts.googleapis.com/css2?family=Inter:wght@300..700&display=swap',
}
for name, url in families.items():
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            css = r.read().decode('utf-8')
        print(name, len(css), css[:120].replace('\n', ' '))
        # grab latin and latin-ext blocks
        urls = re.findall(r'url\((https://[^)]+\.woff2)\)', css)
        seen = []
        for u in urls:
            if u not in seen:
                seen.append(u)
        print('fonts found', len(seen))
        for i, u in enumerate(seen):
            try:
                with urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=45) as r:
                    data = r.read()
                fn = f'assets/fonts/{name}-{i}.woff2'
                open(fn, 'wb').write(data)
                print('saved', fn, len(data))
            except Exception as e:
                print('ERR font', i, e)
    except Exception as e:
        print('ERR css', name, e)

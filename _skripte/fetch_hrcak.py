import urllib.request, urllib.parse, re, os, ssl

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'hr,en-US;q=0.7,en;q=0.5',
        'Referer': 'https://hrcak.srce.hr/',
    })
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()

url = 'https://hrcak.srce.hr/search/?q=' + urllib.parse.quote('moslavačka gora')
try:
    data = get(url)
    print('status ok', len(data))
    open('_tekst/hrcak_search.html', 'wb').write(data)
    html = data.decode('utf-8', 'replace')
    links = sorted(set(re.findall(r'href="(/[^"]*?/\d+)"', html)))
    print('\n'.join(links[:80]))
except Exception as e:
    print('ERR', type(e).__name__, e)

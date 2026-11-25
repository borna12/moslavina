import urllib.request, urllib.parse, re, html

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'hr,en;q=0.8'})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode('utf-8', 'replace')
    except Exception as e:
        return 'ERR ' + repr(e)

for q in ['site:hrcak.srce.hr Moslavina biljke', 'site:hrcak.srce.hr Moslavačka gora']:
    h = get('https://lite.duckduckgo.com/lite/?q=' + urllib.parse.quote(q))
    print('###', q, len(h))
    print(h[:600].replace('\n', ' '))
    links = re.findall(r'href="([^"]*hrcak[^"]*)"', h)
    print('links', links[:10])

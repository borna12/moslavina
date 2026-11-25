import urllib.request, urllib.parse, re

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'hr,en;q=0.8'})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.read().decode('utf-8', 'replace')
    except Exception as e:
        return 'ERR ' + repr(e)

print('--- robots')
print(get('https://hrcak.srce.hr/robots.txt')[:800])
print('--- oai')
print(get('https://hrcak.srce.hr/oai?verb=Identify')[:800])
print('--- ddg')
h = get('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote('site:hrcak.srce.hr "Moslavačka gora"'))
print(len(h))
for m in re.findall(r'uddg=([^&"]+)', h)[:40]:
    print(urllib.parse.unquote(m))

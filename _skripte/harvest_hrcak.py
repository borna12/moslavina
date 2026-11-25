import urllib.request, urllib.parse, re, html, json, os, time

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
        'Accept-Language': 'hr,en;q=0.8',
    })
    for _ in range(2):
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except Exception as e:
            err = e
            time.sleep(1)
    print('ERR', url, err)
    return b''

queries = [
    'site:hrcak.srce.hr "Moslavačka gora"',
    'site:hrcak.srce.hr Moslavačka gora geologija granit',
    'site:hrcak.srce.hr Moslavina flora',
    'site:hrcak.srce.hr Moslavina fauna',
    'site:hrcak.srce.hr Moslavina šuma biljke',
    'site:hrcak.srce.hr "Crkveni jarak"',
    'site:hrcak.srce.hr pavlinski samostan Moslavina',
    'site:hrcak.srce.hr Moslavina nafta',
    'site:hrcak.srce.hr Moslavačka gora Humka',
    'site:hrcak.srce.hr Moslavina kamenolom',
]

found = {}
for q in queries:
    h = get('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)).decode('utf-8', 'replace')
    blocks = re.split(r'<div class="result results_links', h)
    for b in blocks[1:]:
        mt = re.search(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', b, re.S)
        sn = re.search(r'class="result__snippet"[^>]*>(.*?)</a>', b, re.S)
        if not mt:
            continue
        href = html.unescape(mt.group(1))
        m = re.search(r'uddg=([^&]+)', href)
        if m:
            href = urllib.parse.unquote(m.group(1))
        title = re.sub('<[^>]+>', '', html.unescape(mt.group(2))).strip()
        snippet = re.sub('<[^>]+>', '', html.unescape(sn.group(1))).strip() if sn else ''
        mid = re.search(r'hrcak\.srce\.hr/(?:clanak/|en/)?(\d+)', href)
        fid = re.search(r'hrcak\.srce\.hr/file/(\d+)', href)
        if mid:
            found.setdefault(mid.group(1), {'title': title, 'snippet': snippet, 'url': href})
    time.sleep(1)

print(len(found), 'candidates')
for k, v in found.items():
    print(k, '|', v['title'][:90], '|', v['snippet'][:90])
json.dump(found, open('_tekst/hrcak_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

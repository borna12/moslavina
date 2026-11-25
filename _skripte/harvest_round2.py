import urllib.request, urllib.parse, re, html, json, time

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept-Language': 'hr,en;q=0.8'})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read().decode('utf-8', 'replace')
    except Exception as e:
        return 'ERR ' + repr(e)

queries = [
    'site:hrcak.srce.hr Moslavina biljni svijet',
    'site:hrcak.srce.hr Moslavačka gora šuma vegetacija',
    'site:hrcak.srce.hr "Zbornik Moslavine"',
    'site:hrcak.srce.hr Garić grad',
    'site:hrcak.srce.hr "Bela crkva" Moslavačka',
    'site:hrcak.srce.hr Moslavina krajobraz regionalni park',
    'site:hrcak.srce.hr Moslavačka gora vode potok',
    'site:hrcak.srce.hr Moslavina turizam poučna staza',
    'site:hrcak.srce.hr Moslavačka gora minerali',
    'site:hrcak.srce.hr Moslavina plemstvo srednji vijek',
    'site:hrcak.srce.hr Moslavačka gora potres seizmologija',
]

found = {}
for q in queries:
    h = get('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q))
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
        if mid:
            found.setdefault(mid.group(1), {'title': title, 'snippet': snippet, 'url': href, 'q': q})
    time.sleep(1)

old = json.load(open('_tekst/hrcak_candidates.json', encoding='utf-8'))
new = {k: v for k, v in found.items() if k not in old}
print(len(found), 'total,', len(new), 'new')
for k, v in new.items():
    print(k, '|', v['title'][:95])
old.update(new)
json.dump(old, open('_tekst/hrcak_candidates.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# encyclopedia
enc = {}
for slug in ['moslavacka-gora', 'moslavina', 'gari%C4%87-grad', 'kutina', 'lonjsko-polje', 'granit', 'pavlini']:
    h = get('https://www.enciklopedija.hr/clanak/' + slug)
    print('ENC', slug, len(h), h[:60].replace('\n', ' '))
    enc[slug] = h
json.dump(enc, open('_tekst/enc_pages.json', 'w', encoding='utf-8'), ensure_ascii=False)

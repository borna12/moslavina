import urllib.request, re, html, json, time, os

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

def get(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,*/*;q=0.8',
        'Accept-Language': 'hr,en;q=0.8',
    })
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

cands = json.load(open('_tekst/hrcak_candidates.json', encoding='utf-8'))
out = {}
for cid, c in cands.items():
    try:
        raw = get(f'https://hrcak.srce.hr/clanak/{cid}')
    except Exception as e:
        print('ERR', cid, e)
        continue
    h = raw.decode('utf-8', 'replace')
    open(f'_tekst/hrcak_{cid}.html', 'w', encoding='utf-8').write(h)

    def meta(name, attr='name'):
        m = re.search(rf'<meta\s+{attr}="{name}"\s+content="([^"]*)"', h, re.I)
        return html.unescape(m.group(1)).strip() if m else ''

    title = meta('citation_title') or meta('DC.title')
    journal = meta('citation_journal_title')
    date = meta('citation_publication_date') or meta('citation_date')
    authors = re.findall(r'<meta\s+name="citation_author"\s+content="([^"]*)"', h)
    pdfs = re.findall(r'<meta\s+name="citation_pdf_url"\s+content="([^"]*)"', h)
    desc = meta('description') or meta('DC.description')
    keywords = re.findall(r'<meta\s+name="citation_keywords"\s+content="([^"]*)"', h)
    out[cid] = {
        'title': title, 'journal': journal, 'date': date,
        'authors': [html.unescape(a) for a in authors],
        'pdfs': pdfs, 'keywords': keywords, 'desc': desc, 'page': c['url'],
    }
    print(cid, '|', title[:80], '|', journal, date, '| pdfs', len(pdfs), '| keys', keywords[:6])
    time.sleep(0.5)

json.dump(out, open('_tekst/hrcak_meta.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

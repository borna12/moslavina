import urllib.request, urllib.parse, json

UA = 'OpenWorkResearch/1.0 (mailto:research@example.org)'

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

queries = ['Moslavačka gora', 'Moslavina gora', 'Moslavina flora fauna', 'Crkveni jarak']
seen = {}
for q in queries:
    url = ('https://api.crossref.org/works?rows=50&select=DOI,title,container-title,issued,author,URL,link,abstract'
           '&query.bibliographic=' + urllib.parse.quote(q))
    d = get(url)
    for it in d['message']['items']:
        title = (it.get('title') or [''])[0]
        cont = (it.get('container-title') or [''])[0]
        url_ = it.get('URL', '')
        links = [l.get('URL', '') for l in it.get('link', [])]
        blob = ' '.join([title, cont, url_] + links).lower()
        if 'moslav' in blob or 'crkveni jarak' in blob:
            seen[it['DOI']] = {
                'title': title, 'container': cont,
                'year': (it.get('issued', {}).get('date-parts') or [[None]])[0][0],
                'url': url_, 'links': links,
                'authors': [f"{a.get('given','')} {a.get('family','')}".strip() for a in it.get('author', [])],
            }
print(len(seen))
for doi, v in seen.items():
    print(doi, '|', v['year'], '|', v['title'][:80], '|', v['container'][:40], '|', v['url'])
json.dump(seen, open('_tekst/crossref.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

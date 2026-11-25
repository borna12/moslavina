import json, re, html

enc = json.load(open('_tekst/enc_pages.json', encoding='utf-8'))
for slug, h in enc.items():
    t = re.search(r'<title>(.*?)</title>', h, re.S)
    print('###', slug, '|', html.unescape(t.group(1)).strip() if t else '')
    # strip scripts/styles and tags
    body = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    body = re.sub(r'<[^>]+>', ' ', body)
    body = html.unescape(re.sub(r'\s+', ' ', body))
    print(body[:1200])
    print()

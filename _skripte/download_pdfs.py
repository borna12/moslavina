import urllib.request, json, os, re

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

meta = json.load(open('_tekst/hrcak_meta.json', encoding='utf-8'))
wanted = {
    '498158': 'Mravunac_Balen_Zorovac_mramor',
    '20503': 'Metalogenija_Juzne_Tisije_Moslavacka_gora',
    '454689': 'Dumortierit_Moslavacka_gora',
    '338405': 'Krajobrazna_i_bioloska_raznolikost_RP_Moslavacka_gora',
}
os.makedirs('izvori', exist_ok=True)
for cid, base in wanted.items():
    m = meta.get(cid)
    if not m or not m['pdfs']:
        print('no pdf', cid)
        continue
    url = m['pdfs'][0]
    if url.startswith('//'):
        url = 'https:' + url
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Referer': f'https://hrcak.srce.hr/clanak/{cid}'})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
        fn = f'izvori/hrcak_{base}.pdf'
        open(fn, 'wb').write(data)
        print('OK', fn, len(data), data[:5])
    except Exception as e:
        print('ERR', cid, e)

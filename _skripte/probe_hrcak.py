import urllib.request

UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

def get(url, referer='https://www.google.com/'):
    req = urllib.request.Request(url, headers={
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/pdf,*/*;q=0.8',
        'Accept-Language': 'hr,en;q=0.8',
        'Referer': referer,
    })
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            data = r.read()
            print(url, '->', r.status, len(data), r.headers.get('content-type'))
            return data
    except Exception as e:
        print(url, '-> ERR', type(e).__name__, e)
        return None

get('https://hrcak.srce.hr/')
get('https://hrcak.srce.hr/12345')
get('https://hrcak.srce.hr/clanak/12345')
get('https://hrcak.srce.hr/file/12345')

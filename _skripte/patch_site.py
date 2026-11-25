import io

p = 'assets/js/site.js'
s = io.open(p, encoding='utf-8').read()

s = s.replace('function headerHTML(active) {', 'function headerHTML(active, ROOT) {')
s = s.replace("return '<a href=\"' + p.href + '\"'", "return '<a href=\"' + ROOT + p.href + '\"'")
s = s.replace("'<a class=\"brand\" href=\"index.html\"", "'<a class=\"brand\" href=\"' + ROOT + 'index.html\"")
s = s.replace('function footerHTML() {', 'function footerHTML(ROOT) {')
s = s.replace('var page = document.body.getAttribute("data-page") || "";',
              'var page = document.body.getAttribute("data-page") || "";\n    var ROOT = document.body.getAttribute("data-root") || "";')
s = s.replace('header.innerHTML = headerHTML(page);', 'header.innerHTML = headerHTML(page, ROOT);')
s = s.replace('footer.innerHTML = footerHTML();', 'footer.innerHTML = footerHTML(ROOT);')

for href in ['gora.html', 'zivi-svijet.html', 'povijest.html', 'staza.html', 'igre.html',
             'igre/kviz.html?k=stijene', 'igre/kviz.html?k=biljke', 'krizaljka.html', 'izvori.html']:
    s = s.replace('href=\\"' + href + '\\"', 'href=\\"' + href + '\\"')  # no-op placeholder
    s = s.replace("href=\"" + href + "\"", "href=\"' + ROOT + '" + href + "\"")

io.open(p, 'w', encoding='utf-8').write(s)
print('done')

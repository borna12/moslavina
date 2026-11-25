import io

p = 'krizaljka.html'
s = io.open(p, encoding='utf-8').read()
s = s.replace('href="../assets/', 'href="assets/')
s = s.replace('src="../assets/', 'src="assets/')
s = s.replace('href="../igre.html"', 'href="igre.html"')
s = s.replace('data-root="../"', 'data-root=""')
io.open(p, 'w', encoding='utf-8').write(s)
print('fixed krizaljka paths')

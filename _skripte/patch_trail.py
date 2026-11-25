import io
p = 'assets/js/trail.js'
s = io.open(p, encoding='utf-8').read()
pairs = [('x: 196, y: 352', 'x: 182, y: 366'), ('x: 240, y: 316', 'x: 226, y: 333'),
         ('x: 286, y: 282', 'x: 270, y: 300'), ('x: 330, y: 244', 'x: 314, y: 266'),
         ('x: 360, y: 204', 'x: 348, y: 230'), ('x: 384, y: 168', 'x: 376, y: 194'),
         ('x: 396, y: 140', 'x: 400, y: 160'), ('x: 408, y: 118', 'x: 420, y: 132'),
         ('x: 424, y: 102', 'x: 458, y: 96'), ('x: 318, y: 300', 'x: 344, y: 330')]
for a, b in pairs:
    s = s.replace(a, b)
s = s.replace('b.textContent = s.extra ? "•" : s.id;', 'b.textContent = s.extra ? s.short : s.id;')
for tag, short in [('id: "humka"', 'short: "H", '), ('id: "vis"', 'short: "V", '),
                   ('id: "jezero"', 'short: "J", '), ('id: "slap"', 'short: "S", ')]:
    s = s.replace(tag, short + tag)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok')

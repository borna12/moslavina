import io

# 1) trail.js: render letters for extra stops too
p = 'assets/js/trail.js'
s = io.open(p, encoding='utf-8').read()
old = """      '<circle cx="' + s.x + '" cy="' + s.y + '" r="' + (s.extra ? 13 : 15) + '" fill="#f8f4e9" stroke="#b3542f" stroke-width="2.2"/>' +
      (s.extra
        ? '<circle cx="' + s.x + '" cy="' + s.y + '" r="4.5" fill="#b3542f"/>'
        : '<text x="' + s.x + '" y="' + (s.y + 4.5) + '" text-anchor="middle" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#173327">' + s.id + "</text>");"""
new = """      '<circle cx="' + s.x + '" cy="' + s.y + '" r="' + (s.extra ? 13 : 15) + '" fill="' + (s.extra ? "#f0cd8a" : "#f8f4e9") + '" stroke="#b3542f" stroke-width="2.2"/>' +
      '<text x="' + s.x + '" y="' + (s.y + 4.5) + '" text-anchor="middle" font-family="Inter, sans-serif" font-size="' + (s.extra ? 10 : 12) + '" font-weight="700" fill="#173327">' + (s.extra ? s.short : s.id) + "</text>";"""
s = s.replace(old, new)
io.open(p, 'w', encoding='utf-8').write(s)

# 2) staza.html: move labels, soften tree pattern
p = 'staza.html'
h = io.open(p, encoding='utf-8').read()
h = h.replace('<rect width="700" height="540" rx="14" fill="url(#treeDots)"/>',
              '<rect width="700" height="540" rx="14" fill="url(#treeDots)" opacity=".55"/>')
h = h.replace('<rect x="360" y="40" width="96" height="24" rx="12" fill="#f8f4e9" stroke="#173327"/>',
              '<rect x="300" y="34" width="96" height="24" rx="12" fill="#f8f4e9" stroke="#173327"/>')
h = h.replace('<text x="408" y="56" text-anchor="middle">ULAZ · Humka</text>',
              '<text x="348" y="50" text-anchor="middle">ULAZ · Humka</text>')
h = h.replace('<text x="356" y="78" font-size="11" font-weight="700" fill="#173327">HUMKA · 488 m</text>',
              '<text x="466" y="86" font-size="11" font-weight="700" fill="#173327">HUMKA · 488 m</text>')
h = h.replace('<text x="432" y="98" font-size="11" font-weight="700" fill="#173327">HUMKA · 488 m</text>',
              '<text x="466" y="86" font-size="11" font-weight="700" fill="#173327">HUMKA · 488 m</text>')
io.open(p, 'w', encoding='utf-8').write(h)
print('map labels updated')

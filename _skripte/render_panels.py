import fitz
d = fitz.open('Crkveni jarak_poucni infopaneli.pdf')
for i in [1, 2, 3, 4]:
    pg = d[i]
    pix = pg.get_pixmap(dpi=110)
    pix.save(f'_tekst/panel_p{i+1}.png')
    print(i + 1, pix.width, pix.height)

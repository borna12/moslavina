import fitz
d = fitz.open('Crkveni jarak_poucni infopaneli.pdf')
for i in range(4, 9):
    pix = d[i].get_pixmap(dpi=45)
    pix.save(f'_tekst/panel_small_p{i+1}.png')
    print(i + 1, pix.width, pix.height)

import fitz
d = fitz.open('Crkveni jarak_poucni infopaneli.pdf')
for i in [1, 2, 3]:
    pg = d[i]
    print('=== page', i + 1)
    for x in pg.get_images(full=True):
        print('xref', x[0], 'smask', x[1], 'w', x[2], 'h', x[3], 'bpc', x[4], 'cs', x[5], 'filter', x[8])
    pix = pg.get_pixmap(dpi=45)
    pix.save(f'_tekst/panel_small_p{i+1}.png')
    print('render', pix.width, pix.height)

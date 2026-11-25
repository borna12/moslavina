import fitz, os

os.makedirs('assets/img/raw', exist_ok=True)
srcs = {
    'paneli': 'Crkveni jarak_poucni infopaneli.pdf',
    'geo': 'MOSLAVINA_IZ_GEOLOSKE_PERSPEKTIVE.pdf',
}
count = 0
for tag, p in srcs.items():
    d = fitz.open(p)
    for pi, pg in enumerate(d):
        for x in pg.get_images(full=True):
            xref, w, h = x[0], x[2], x[3]
            if w < 300 or h < 300:
                continue
            pix = fitz.Pixmap(d, xref)
            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            fn = f'assets/img/raw/{tag}_p{pi+1}_x{xref}_{w}x{h}.png'
            pix.save(fn)
            count += 1
print('saved', count)

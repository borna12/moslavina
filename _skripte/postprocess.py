from PIL import Image

def clear_rects(path, frac_rects=None, top_frac=None):
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    px = im.load()
    if top_frac is not None:
        for y in range(0, int(h * top_frac)):
            for x in range(w):
                r, g, b, a = px[x, y]
                px[x, y] = (r, g, b, 0)
    for x0, y0, x1, y1 in (frac_rects or []):
        for y in range(int(h * y0), int(h * y1)):
            for x in range(int(w * x0), int(w * x1)):
                r, g, b, a = px[x, y]
                px[x, y] = (r, g, b, 0)
    im.save(path)
    print('post', path, im.size)

clear_rects('assets/img/ilustracije/hrast-grana.png', top_frac=0.075)
clear_rects('assets/img/ilustracije/mahovina.png', top_frac=0.062)
clear_rects('assets/img/ilustracije/jelen.png', frac_rects=[(0.595, 0.30, 0.64, 0.325)])

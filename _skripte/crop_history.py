import fitz
from PIL import Image

DPI = 260
SW, SH = 930.0, 2082.0
crops = [
    (8, 'samostan-tlocrt', 116, 492, 366, 702),
    (8, 'pavlinski-grb', 52, 1492, 258, 1748),
]
doc = fitz.open('Crkveni jarak_poucni infopaneli.pdf')
cache = {}
for pi, name, x0, y0, x1, y1 in crops:
    if pi not in cache:
        cache[pi] = doc[pi].get_pixmap(dpi=DPI)
    pix = cache[pi]
    sx, sy = pix.width / SW, pix.height / SH
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples).crop(
        (int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy))).copy()
    g = img.convert('L')
    alpha = g.point(lambda v: 0 if v >= 214 else min(255, int((214 - v) * 255 / 110)))
    out = Image.new('RGBA', img.size, (17, 43, 34, 255))
    out.putalpha(alpha)
    out.thumbnail((1000, 1000), Image.LANCZOS)
    out.save(f'assets/img/ilustracije/{name}.png')
    print(name, out.size)

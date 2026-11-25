import fitz, os
from PIL import Image, ImageDraw

os.makedirs('assets/img/ilustracije', exist_ok=True)
DPI = 260
SW, SH = 930.0, 2082.0

# (page_index, name, x0, y0, x1, y1, [erase rects in crop-local small coords])
crops = [
    (1, 'zimzelen', 55, 490, 292, 772, [(210, 250, 240, 290)]),
    (1, 'kopitnjak', 383, 478, 693, 740, [(0, 245, 70, 275)]),
    (1, 'bujad', 52, 1420, 270, 1742, []),
    (1, 'jelenja-paprat', 506, 1440, 664, 1742, []),
    (2, 'kuna', 52, 492, 440, 758, []),
    (2, 'veprina', 470, 592, 748, 826, []),
    (2, 'jelen', 95, 1300, 660, 1970, [(0, 410, 118, 595)]),
    (3, 'hrast-grana', 512, 742, 712, 925, []),
    (3, 'bukva', 92, 1682, 330, 1952, []),
    (3, 'grab', 328, 1468, 488, 1688, []),
    (3, 'mahovina', 552, 1658, 706, 1952, []),
    (4, 'granit', 85, 1388, 365, 1600, []),
    (4, 'turmalin', 95, 1692, 292, 1942, []),
    (4, 'kvarc', 405, 1650, 625, 1900, []),
    (4, 'geoloska-karta', 60, 380, 610, 800, []),
    (5, 'tektonska-karta', 240, 705, 735, 1145, []),
    (5, 'granice-ploca', 45, 1468, 625, 1990, []),
]

doc = fitz.open('Crkveni jarak_poucni infopaneli.pdf')
cache = {}
for pi, name, x0, y0, x1, y1, erases in crops:
    if pi not in cache:
        cache[pi] = doc[pi].get_pixmap(dpi=DPI)
    pix = cache[pi]
    sx = pix.width / SW
    sy = pix.height / SH
    box = (int(x0 * sx), int(y0 * sy), int(x1 * sx), int(y1 * sy))
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples).crop(box).copy()

    # fill unwanted text areas with the flat background colour sampled from a blank spot
    bg = (152, 217, 231)
    dr = ImageDraw.Draw(img)
    for ex0, ey0, ex1, ey1 in erases:
        dr.rectangle([ex0 * sx, ey0 * sy, ex1 * sx, ey1 * sy], fill=bg)

    g = img.convert('L')
    alpha = g.point(lambda v: 0 if v >= 198 else min(255, int((198 - v) * 255 / 160)))
    out = Image.new('RGBA', img.size, (17, 43, 34, 255))
    out.putalpha(alpha)
    out.thumbnail((1200, 1200), Image.LANCZOS)
    out.save(f'assets/img/ilustracije/{name}.png')
    print(name, out.size, 'bg', bg)

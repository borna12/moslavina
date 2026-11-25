import fitz
from PIL import Image, ImageDraw
d = fitz.open('Crkveni jarak_poucni infopaneli.pdf')
pix = d[8].get_pixmap(dpi=45)
im = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
dr = ImageDraw.Draw(im)
for x in range(0, im.width, 50):
    dr.line([(x, 0), (x, im.height)], fill='red', width=1)
    if x % 100 == 0:
        dr.text((x + 2, 4), str(x), fill='red')
for y in range(0, im.height, 50):
    dr.line([(0, y), (im.width, y)], fill='red', width=1)
    if y % 100 == 0:
        dr.text((3, y + 2), str(y), fill='red')
im.save('_tekst/grid_p9.png')
print(im.size)

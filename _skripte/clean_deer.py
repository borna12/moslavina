from PIL import Image, ImageDraw
import glob, os, math

# clean text from deer illustration
p = 'assets/img/ilustracije/jelen.png'
im = Image.open(p).convert('RGBA')
w, h = im.size
px = im.load()
rects = [
    (int(w * 0.51), int(h * 0.10), int(w * 1.0), int(h * 0.395)),
    (int(w * 0.86), int(h * 0.53), int(w * 1.0), int(h * 0.72)),
]
for x0, y0, x1, y1 in rects:
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 0)
im.save(p)
print('cleaned', p)

files = sorted(glob.glob('assets/img/ilustracije/*.png'))
thumb = 280
cols = 5
rows = math.ceil(len(files) / cols)
sheet = Image.new('RGB', (cols * thumb, rows * (thumb + 22)), '#f8f4e9')
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    src = Image.open(f).convert('RGBA')
    bg = Image.new('RGBA', src.size, (248, 244, 233, 255))
    bg.alpha_composite(src)
    img = bg.convert('RGB')
    img.thumbnail((thumb - 8, thumb - 8))
    x = (i % cols) * thumb
    y = (i // cols) * (thumb + 22)
    sheet.paste(img, (x + (thumb - img.width) // 2, y))
    d.text((x + 4, y + thumb + 4), os.path.basename(f)[:-4], fill='#111')
sheet.save('_tekst/contact_final.png')
print(sheet.size)

from PIL import Image, ImageDraw
import glob, os, math

files = sorted(glob.glob('assets/img/ilustracije/*.png'))
thumb = 260
cols = 5
rows = math.ceil(len(files) / cols)
sheet = Image.new('RGB', (cols * thumb, rows * (thumb + 22)), '#f6f2e7')
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f)
    bg = Image.new('RGBA', im.size, (246, 242, 231, 255))
    bg.alpha_composite(im)
    im = bg.convert('RGB')
    im.thumbnail((thumb - 10, thumb - 10))
    x = (i % cols) * thumb
    y = (i // cols) * (thumb + 22)
    sheet.paste(im, (x + (thumb - im.width) // 2, y))
    d.text((x + 4, y + thumb + 4), os.path.basename(f)[:-4], fill='black')
sheet.save('_tekst/contact_crops.png')
print(sheet.size)

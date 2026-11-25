from PIL import Image
import glob, os, math

files = sorted(glob.glob('assets/img/raw/paneli*.png'))
thumb = 320
cols = 5
rows = math.ceil(len(files) / cols)
sheet = Image.new('RGB', (cols * thumb, rows * (thumb + 20)), '#f6f3ea')
for i, f in enumerate(files):
    im = Image.open(f).convert('RGBA')
    bg = Image.new('RGBA', im.size, (246, 243, 234, 255))
    bg.alpha_composite(im)
    im = bg.convert('RGB')
    im.thumbnail((thumb, thumb))
    x = (i % cols) * thumb
    y = (i // cols) * (thumb + 20)
    sheet.paste(im, (x + (thumb - im.width) // 2, y))
    from PIL import ImageDraw
    ImageDraw.Draw(sheet).text((x + 3, y + thumb + 4), os.path.basename(f)[:-4], fill='#333')
sheet.save('_tekst/contact_paneli.png')
print(sheet.size)

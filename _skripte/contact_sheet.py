from PIL import Image, ImageDraw
import glob, os, math

files = sorted(glob.glob('assets/img/raw/*.png'))
thumb = 300
cols = 6
rows = math.ceil(len(files) / cols)
sheet = Image.new('RGB', (cols * thumb, rows * (thumb + 22)), 'white')
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB')
    im.thumbnail((thumb, thumb))
    x = (i % cols) * thumb
    y = (i // cols) * (thumb + 22)
    sheet.paste(im, (x + (thumb - im.width) // 2, y))
    d.text((x + 3, y + thumb + 5), os.path.basename(f)[:44], fill='black')
sheet.save('_tekst/contact_sheet.png')
print(sheet.size)

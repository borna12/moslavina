from PIL import Image
import glob

# boost line-art contrast a little
for p in glob.glob('assets/img/ilustracije/*.png'):
    im = Image.open(p).convert('RGBA')
    r, g, b, a = im.split()
    a = a.point(lambda v: min(255, int(v * 1.28)))
    im = Image.merge('RGBA', (r, g, b, a))
    im.save(p)
print('boosted', len(glob.glob('assets/img/ilustracije/*.png')))

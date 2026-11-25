from PIL import Image
for name in ['samostan-tlocrt', 'pavlinski-grb', 'hrast-grana', 'mahovina', 'jelen']:
    p = f'assets/img/ilustracije/{name}.png'
    im = Image.open(p).convert('RGBA')
    bg = Image.new('RGBA', im.size, (248, 244, 233, 255))
    bg.alpha_composite(im)
    bg.convert('RGB').save(f'_tekst/prev_{name}.jpg', quality=90)
    alphas = im.getchannel('A')
    print(name, im.size, alphas.getextrema())

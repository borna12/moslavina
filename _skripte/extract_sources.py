import fitz, glob, os

for p in glob.glob('izvori/*.pdf'):
    d = fitz.open(p)
    out = []
    for i, page in enumerate(d):
        out.append(f'===== STRANICA {i+1} =====\n' + page.get_text())
    base = os.path.splitext(os.path.basename(p))[0]
    open(f'_tekst/{base}.txt', 'w', encoding='utf-8').write('\n'.join(out))
    print(base, len(d), sum(len(x) for x in out))

import random, json, io, sys

WORDS = [
    ('GRANIT', 'Kisela dubinska magmatska stijena, glavna stijena Moslavačke gore'),
    ('ANDALUZIT', 'Mineral koji je Vukotinović prvi opisao u moslavačkom granitu'),
    ('HUMKA', 'Najviši vrh Moslavačke gore (488 m)'),
    ('KAMENJAČA', 'Potok koji teče kroz Crkveni jarak'),
    ('SAMOSTAN', 'Pavlinska zgrada u klancu Kamenjače (Bela crkva)'),
    ('PAVLINI', 'Red braće sv. Pavla prvoga pustinjaka'),
    ('BUKVA', 'Drvo glatke sive kore; plod joj je bukvica'),
    ('GRAB', 'Drvo oštro nazubljenog lista, koristi se za alate i glazbala'),
    ('JELEN', 'Kralj šume'),
    ('KUNA', 'Životinja čije je krzno nekad bilo porez – marturina'),
    ('VEPRINA', 'Zaštićeni vazdazeleni grm s filokladijima'),
    ('PAPRAT', 'Biljka koja se razmnožava sporama i nema cvijet'),
    ('MAHOVINA', 'Prirodni kompas – raste na vlažnijoj, sjevernoj strani debla'),
    ('GABRO', 'Bazična magmatska stijena oceanske kore, nađena u Kamenjači'),
    ('RASJED', 'Pukotina u Zemljinoj kori s pomakom krila'),
    ('POTRES', 'Naglo oslobađanje energije u Zemljinoj kori'),
    ('MIGMATIT', 'Stijena na granici metamorfnog i magmatskog'),
    ('KVARC', 'Mineral koji s mikroklinom i biotitom gradi granit'),
    ('TURMALIN', 'Mineral čiji se radijalno-zrakasti agregat zove „sunce“'),
    ('NAFTA', 'Moslavina je najstarija hrvatska regija po eksploataciji ove sirovine'),
    ('ZIMZELEN', 'Vazdazelena biljka ljubičastih cvjetova koja sprječava eroziju'),
    ('PLUĆNJAK', 'Ljekovita biljka čiji list podsjeća na plućna krila'),
    ('KRISTAL', 'Pravilno oblikovano tijelo minerala'),
    ('ZLATAR', 'Zanimanje koje obrađuje dragocjene kovine'),
]

SIZE = 15
TARGET = 17


def can_place(grid, word, r, c, dr, dc):
    n = len(word)
    er, ec = r + dr * (n - 1), c + dc * (n - 1)
    if not (0 <= r < SIZE and 0 <= c < SIZE and 0 <= er < SIZE and 0 <= ec < SIZE):
        return None
    cross = 0
    br, bc = r - dr, c - dc
    if 0 <= br < SIZE and 0 <= bc < SIZE and grid[br][bc]:
        return None
    ar, ac = er + dr, ec + dc
    if 0 <= ar < SIZE and 0 <= ac < SIZE and grid[ar][ac]:
        return None
    for i in range(n):
        rr, cc = r + dr * i, c + dc * i
        cur = grid[rr][cc]
        if cur:
            if cur != word[i]:
                return None
            cross += 1
        else:
            if dr == 0:
                for nr in (rr - 1, rr + 1):
                    if 0 <= nr < SIZE and grid[nr][cc]:
                        return None
            else:
                for nc in (cc - 1, cc + 1):
                    if 0 <= nc < SIZE and grid[rr][nc]:
                        return None
    return cross


def score(r, c):
    mid = (SIZE - 1) / 2
    return -((abs(r - mid) + abs(c - mid)) * 0.4)


def build(seed, n_words):
    rnd = random.Random(seed)
    words = WORDS[:]
    rnd.shuffle(words)
    words.sort(key=lambda x: -len(x[0]))
    grid = [['' for _ in range(SIZE)] for _ in range(SIZE)]
    placed = []
    w, clue = words[0]
    r, c = SIZE // 2, (SIZE - len(w)) // 2
    for i, ch in enumerate(w):
        grid[r][c + i] = ch
    placed.append({'word': w, 'clue': clue, 'r': r, 'c': c, 'dir': 'A'})

    remaining = words[1:]
    progress = True
    while progress and len(placed) < n_words:
        progress = False
        best = None
        for w, clue in remaining:
            for pr in placed:
                pw = pr['word']
                for i, ch in enumerate(pw):
                    for j, wch in enumerate(w):
                        if ch != wch:
                            continue
                        if pr['dir'] == 'A':
                            r = pr['r'] - j
                            c = pr['c'] + i
                            dr, dc = 1, 0
                        else:
                            r = pr['r'] + i
                            c = pr['c'] - j
                            dr, dc = 0, 1
                        cross = can_place(grid, w, r, c, dr, dc)
                        if cross is None or cross == 0:
                            continue
                        s = cross * 10 + score(r, c)
                        if best is None or s > best[0]:
                            best = (s, w, clue, r, c, dr, dc)
        if best:
            s, w, clue, r, c, dr, dc = best
            for i, ch in enumerate(w):
                grid[r + dr * i][c + dc * i] = ch
            placed.append({'word': w, 'clue': clue, 'r': r, 'c': c, 'dir': 'A' if dr == 0 else 'D'})
            remaining = [(x, y) for x, y in remaining if x != w]
            progress = True

    rows = [i for i in range(SIZE) if any(grid[i])]
    cols = [j for j in range(SIZE) if any(grid[i][j] for i in range(SIZE))]
    r0, r1, c0, c1 = min(rows), max(rows), min(cols), max(cols)
    sub = [row[c0:c1 + 1] for row in grid[r0:r1 + 1]]
    for p in placed:
        p['r'] -= r0
        p['c'] -= c0
    return placed, sub


best = None
for seed in range(800):
    placed, sub = build(seed, TARGET)
    if len(placed) < 14:
        continue
    area = len(sub) * len(sub[0])
    val = (len(placed), -area)
    if best is None or val > best[0]:
        best = (val, seed, placed, sub)

val, seed, placed, sub = best
h, w = len(sub), len(sub[0])

# numbering
nums = {}
counter = 0
for r in range(h):
    for c in range(w):
        if not sub[r][c]:
            continue
        starts = False
        if (c == 0 or not sub[r][c - 1]) and c + 1 < w and sub[r][c + 1]:
            starts = True
        if (r == 0 or not sub[r - 1][c]) and r + 1 < h and sub[r + 1][c]:
            starts = True
        if starts:
            counter += 1
            nums[(r, c)] = counter

for p in placed:
    p['num'] = nums[(p['r'], p['c'])]

across = sorted([p for p in placed if p['dir'] == 'A'], key=lambda p: p['num'])
down = sorted([p for p in placed if p['dir'] == 'D'], key=lambda p: p['num'])

data = {
    'cols': w,
    'rows': h,
    'grid': [''.join(ch if ch else ' ' for ch in row) for row in sub],
    'nums': [[nums.get((r, c), 0) for c in range(w)] for r in range(h)],
    'across': [{'num': p['num'], 'clue': p['clue'], 'len': len(p['word'])} for p in across],
    'down': [{'num': p['num'], 'clue': p['clue'], 'len': len(p['word'])} for p in down],
    'words': [p['word'] for p in placed],
}
print('seed', seed, 'words', len(placed), 'grid', h, 'x', w)
print('\n'.join(''.join(ch if ch else '·' for ch in row) for row in sub))
print(json.dumps(data, ensure_ascii=False, indent=1)[:1200])

js = 'window.KRIZALJKA = ' + json.dumps(data, ensure_ascii=False, indent=2) + ';\n'
open('assets/js/data/krizaljka.js', 'w', encoding='utf-8').write(js)

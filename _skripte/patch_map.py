import io, re

p = 'assets/js/trail.js'
s = io.open(p, encoding='utf-8').read()
coords = [
    (182, 366, 196, 356), (226, 333, 240, 310), (270, 300, 284, 266),
    (314, 266, 330, 216), (348, 230, 368, 170), (376, 194, 400, 132),
    (400, 160, 456, 170), (420, 132, 466, 205), (458, 96, 420, 100),
    (344, 330, 392, 310),
]
for old, new in [((a, b), (c, d)) for a, b, c, d in coords]:
    s = s.replace(f'x: {old[0]}, y: {old[1]}', f'x: {new[0]}, y: {new[1]}')
io.open(p, 'w', encoding='utf-8').write(s)

p = 'staza.html'
h = io.open(p, encoding='utf-8').read()
h = h.replace(
    '<path id="trail-path" d="M132 408c26-18 42-44 68-66s52-22 74-44 34-52 56-72 44-36 78-42" fill="none" stroke="#f8f4e9" stroke-width="9" stroke-linecap="round" opacity=".9"/>',
    '<path id="trail-path" d="M132 408C160 396 178 380 196 356 214 332 222 326 240 310 258 294 266 286 284 266 302 246 312 238 330 216 348 194 356 186 368 170 380 154 388 142 400 130 406 124 412 118 420 112 440 118 452 132 458 152 466 178 464 196 456 216 448 236 436 248 422 264 408 280 400 292 392 310 384 328 372 342 360 356 348 370 338 382 324 394 310 406 292 416 270 422 246 428 218 430 196 426 176 422 158 416 146 410" fill="none" stroke="#f8f4e9" stroke-width="9" stroke-linecap="round" opacity=".9"/>')
h = h.replace(
    '<path d="M132 408c26-18 42-44 68-66s52-22 74-44 34-52 56-72 44-36 78-42" fill="none" stroke="#b3542f" stroke-width="2" stroke-dasharray="6 8" stroke-linecap="round"/>',
    '<path d="M132 408C160 396 178 380 196 356 214 332 222 326 240 310 258 294 266 286 284 266 302 246 312 238 330 216 348 194 356 186 368 170 380 154 388 142 400 130 406 124 412 118 420 112 440 118 452 132 458 152 466 178 464 196 456 216 448 236 436 248 422 264 408 280 400 292 392 310 384 328 372 342 360 356 348 370 338 382 324 394 310 406 292 416 270 422 246 428 218 430 196 426 176 422 158 416 146 410" fill="none" stroke="#b3542f" stroke-width="2" stroke-dasharray="6 8" stroke-linecap="round"/>')
h = h.replace(
    '<path d="M210 342c-4-26 6-44 24-56s42-8 52-28" fill="none" stroke="#b3542f" stroke-width="2" stroke-dasharray="6 8" stroke-linecap="round" opacity=".6"/>',
    '')
h = h.replace('<text x="432" y="98" font-size="11" font-weight="700" fill="#173327">HUMKA · 488 m</text>',
              '<text x="356" y="78" font-size="11" font-weight="700" fill="#173327">HUMKA · 488 m</text>')
io.open(p, 'w', encoding='utf-8').write(h)
print('updated')

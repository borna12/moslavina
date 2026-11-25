import io

# crossword clue improvement
p = 'assets/js/data/krizaljka.js'
s = io.open(p, encoding='utf-8').read()
s = s.replace('Bela crkva bila je pavlinski...', 'Pavlinska zgrada u klancu Kamenjače (Bela crkva)')
io.open(p, 'w', encoding='utf-8').write(s)

p = '_skripte/crossword.py'
s = io.open(p, encoding='utf-8').read()
s = s.replace('Bela crkva bila je pavlinski...', 'Pavlinska zgrada u klancu Kamenjače (Bela crkva)')
io.open(p, 'w', encoding='utf-8').write(s)

# do not record a fully revealed crossword as solved
p = 'assets/js/crossword.js'
s = io.open(p, encoding='utf-8').read()
s = s.replace('''    setStatus("Cijela je križaljka otkrivena. Prouči rješenje pa je pokušaj riješiti sam.");''',
              '''    solved = true;
    setStatus("Cijela je križaljka otkrivena. Prouči rješenje pa je pokušaj riješiti sam.");''')
io.open(p, 'w', encoding='utf-8').write(s)
print('patched')

import io
p = '_skripte/crossword.py'
s = io.open(p, encoding='utf-8').read()
s = s.replace("('KAMENJACA', 'Potok koji teče kroz Crkveni jarak')", "('KAMENJAČA', 'Potok koji teče kroz Crkveni jarak')")
io.open(p, 'w', encoding='utf-8').write(s)
print('updated')

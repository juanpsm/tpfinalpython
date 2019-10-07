import pattern.es
import random
import string
# ~ print(dir(pattern.es))

#problem:

x= "danzar amigable barrilete asdfg"
print(pattern.es.tag(x, tokenize=True, encoding='utf-8'))


x = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
print(pattern.es.tag(x, tokenize=True, encoding='utf-8'))
# ~ c = 0
# ~ for x in pattern.es.lexicon.keys():
	# ~ if not (x in pattern.es.spelling.keys()):
		# ~ print(x, end=', ')
		# ~ c += 1
# ~ print("\n")
# ~ print('Cantidad de palabras de lexicon que NO están en spelling: ',c)

# ~ c = 0
# ~ for x in pattern.es.spelling.keys():
	# ~ if not (x in pattern.es.lexicon.keys()):
		# ~ print(x, end=', ')
		# ~ c += 1
# ~ print("\n")
# ~ print('Cantidad de palabras de spelling que NO están en lexicon: ',c)

# ~ c = 0
# ~ for x in pattern.es.spelling.keys():
	# ~ if x in pattern.es.lexicon.keys():
		# ~ print(x, end=', ')
		# ~ c += 1
# ~ print("\n")
# ~ print('Cantidad de palabras de spelling que TAMBIÉN están en lexicon: ',c)

# ~ lista = list(pattern.es.spelling.keys())
# ~ mas_largo = max(lista, key=len)
# ~ print(mas_largo,' - ', len(mas_largo))

# ~ from collections import Counter
# ~ c = Counter(pattern.es.lexicon.values())

# ~ print(c)

# ~ for x in pattern.es.lexicon:
	# ~ if pattern.es.lexicon[x] != pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL')[0][1]:
		# ~ print(x, end=', ')

# ~ x= "buchón perchero"
# ~ print(pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL'))
# ~ print()
# ~ print(type(pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL')))
# ~ print("\n")
# ~ print(pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL')[0])
# ~ print()
# ~ print(type(pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL')[0]))
# ~ print("\n")
# ~ print(pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL')[0][1])
# ~ print()
# ~ print(type(pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL')[0][1]))

# ~ for x in pattern.es.lexicon:
	# ~ t = pattern.es.tag(x, tokenize=True, encoding='utf-8', tagset = 'UNIVERSAL')[0]
	# ~ if pattern.es.lexicon[x] != t[1]:
		# ~ print(t, end=', ')

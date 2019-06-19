from pattern.es import verbs, tag, spelling, lexicon
import string
def clasificar(palabra):
	# tag(palabra, tokenize=True, encoding='utf-8',tagset = 'UNIVERSAL')
	t = tag(palabra, tokenize=True, encoding='utf-8')[0][1] # si fueran varias palabras devuelve una lista de pares (palabra, tag)
	print('tag:',t)
	return t

def buscar_en_pattern(palabra):

	print('Buscar',palabra, 'en pattern')
	if not palabra.lower() in verbs:
		if not palabra.lower() in spelling:
			if (not(palabra.lower() in lexicon) and not(palabra.upper() in lexicon) and not(palabra.capitalize() in lexicon)):
				print('No se encuentra en pattern.es')
				return '_Ninguna_'
			else:
				print('La encontró en lexicon')
				return clasificar(palabra)
		else:
			print('La encontró en spelling')
			return clasificar(palabra)
	else:
		print('La encontró en verbs')
		return clasificar(palabra)
			
	print('\n?\n')

		
	# ~ c = 0
	# ~ for x in verbs:
		# ~ if not x in spelling:
			# ~ if not x in lexicon:
				# ~ print (x, end=', ')
				# ~ c+=1
			
	# ~ print(c)
	# ~ for x in lexicon:
		# ~ if x != x.lower():
			# ~ if x != x.upper():
				# ~ if x != x.capitalize():
					# ~ print(x,end=', ')

if __name__ == "__main__":
	buscar_en_pattern('Camino')

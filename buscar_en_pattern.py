# -*- coding: utf-8 -*-
from pattern.es import verbs, tag, spelling, lexicon
import string
def clasificar(palabra):
	t = tag(palabra, tokenize=True, encoding='utf-8')[0][1] # si fueran varias palabras devuelve una lista de pares (palabra, tag)
	print('  tag:',t)
	return t

def buscar_en_pattern(palabra):

	print('\n  Buscar "',palabra,'" en pattern', sep='')
	if not palabra.lower() in verbs:
		if not palabra.lower() in spelling:
			if (not(palabra.lower() in lexicon) and not(palabra.upper() in lexicon) and not(palabra.capitalize() in lexicon)):
				print('\n  No se encuentra en pattern.es')
				return '_Ninguna_'
			else:
				print('\n  La encontró en lexicon')
				return clasificar(palabra)
		else:
			print('\n  La encontró en spelling')
			return clasificar(palabra)
	else:
		print('\n  La encontró en verbs')
		return clasificar(palabra)
			
	print('\n?\n')

if __name__ == "__main__":
	palabra = 'Camino'
	while(palabra!='q'):
		buscar_en_pattern(palabra)
		palabra = input('\n--------------------------------------------------------------------------\nPalabra: ')

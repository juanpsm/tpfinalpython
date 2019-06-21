# -*- coding: utf-8 -*-
from pattern.web import Wiktionary, plaintext
from buscar_en_pattern import buscar_en_pattern

def buscar_en_wiktionary(palabra):
	
	##resultado = buscar_en_wiktionary(palabra)
	# resultado tiene los campos:
	# 'palabra' [str] la que busqué
	# 'clasif_wik' [str] si se encontro en wiktionario
	# 'clasif_patt' [str] si se encontro en pattern
	# 'definicion' [str] si se encontro en wiktionario
	# los campos que no se pudieron recuperar tendran '_Ninguna_'
	resultado ={}
	resultado['palabra'] = palabra
	resultado['clasificacion_wiktionario'] = '_Ninguna_'
	resultado['definicion'] = '_Ninguna_'
	resultado['clasificacion_pattern'] = '_Ninguna_'


	engine = Wiktionary(language="es")
	sch=engine.search(palabra)
	print('Buscar "',palabra,'" en wiktionario', end='')
	print()
	if sch != None:

		pos_1 = sch.source.find('<dt>1</dt>')
		pos_2 = sch.source.find('<dt>2</dt>',pos_1)
		
		# ~ debug(sch.source[pos_1:pos_2])
		# ~ debug(plaintext(sch.source[pos_1:pos_2]))
		pos_punto=plaintext(sch.source[pos_1:pos_2]).find('.')
		
		print('slice:',pos_1,pos_punto)
		
		definicion = plaintext(sch.source[pos_1:pos_2])[1:pos_punto+1]
		print('Def: ',definicion)
		
		cat = '_no_sabe_'
		if('ES:Sustantivos' in sch.categories):
			print('Wik dice que es Sustantivo!')
			cat = 'sust'
		if('ES:Adjetivos' in sch.categories):
			print('Wik dice que es Adjetivo!')
			if cat == '' :
				cat = 'adj'
			else: cat = 'MIXTA'
		if('ES:Verbos' in sch.categories):
			print('Wik dice que es verbo!')
			if cat == '' :
				cat = 'verb'
			else: cat = 'MIXTA'
	
		resultado['clasificacion_wiktionario'] = cat
	
		resultado['definicion'] = definicion
	else:
		print('No se encontró en wiktionario')

		
		
	cat_pattern = buscar_en_pattern(palabra)
	
	if cat_pattern != '_Ninguna_':
		if cat_pattern[:1] == 'N':
			print('Pattern dice que es sust!')
			cat_pattern = 'sust'
		if cat_pattern[:1] == 'V':
			print('Pattern dice que es verbo!')
			cat_pattern = 'verb'
		if cat_pattern[:1] == 'J':
			print('Pattern dice que es adj!')
			cat_pattern = 'adj'
		
		resultado['clasificacion_pattern'] = cat_pattern
		
	return resultado
if __name__ == "__main__":
	palabra = 'diccionario'
	while(palabra!='q'):
		buscar_en_wiktionary(palabra)
		palabra = input('\n--------------------------------------------------------------------------\nPalabra :')

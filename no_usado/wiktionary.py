# ~ from wiktionaryparser import WiktionaryParser
# ~ parser = WiktionaryParser()
# ~ word = parser.fetch('test')
# ~ another_word = parser.fetch('test', 'french')
# ~ print(another_word)
# ~ parser.set_default_language('french')
# ~ parser.exclude_part_of_speech('noun')
# ~ parser.include_relation('alternative forms')
# ~ print(word)
# ~ print(another_word)

from pattern.web import Wiktionary, plaintext
import re

from pprint import pprint
import traceback
def debug(__x):
	'''Devuelve el nombre_var = valor_var, type: tipo_var'''
	name = traceback.extract_stack(limit=2)[0][3][6:][:-1]
	print ('\n',name,'  --  ','(type:',type(__x),')\n\n','      ',__x,'\n\n')
	# ~ print('[',end='');print(*__x, sep=', ', end='');print(']')

# ~ debug = pprint
palabra = 'gato'


def buscar_en_wiktionary(palabra):
	
	##resultado = buscar_en_wiktionary(palabra)
	# resultado tiene los campos:
	# 'palabra' [str] la que busqué
	# 'clasif_wik' [str] si se encontro en wiktionario
	# 'clasif_patt' [str] si se encontro en pattern
	# 'definicion' [str] si se encontro en wiktionario
	# los campos que no se pudieron recuperar tendran None
	resultado ={}
	resultado['palabra'] = palabra
	resultado['clasificacion_wiktionario'] = None
	resultado['definicion'] = None
	resultado['clasificacion_pattern'] = None
	#return resultado
	
	
	# ~ engine = Wikipedia(license=None, throttle=5.0, language=None)
	# ~ engine.search("dodo",
	   # ~ start = 1,			   # Starting page.
	   # ~ count = 10,			  # Results per page.
		# ~ size = None,			 # Image size: TINY | SMALL | MEDIUM | LARGE
	  # ~ cached = True)			# Cache locally?

	# ~ from pattern.web import Bing, SEARCH, plaintext

	# ~ engine = Bing(license=None) # Enter your license key.
	# ~ for i in range(1,5):
	   # ~ for result in engine.search('holy handgrenade', type=SEARCH, start=i):
		   # ~ print(repr(plaintext(result.text)))
		   # ~ print()
	engine = Wiktionary(language="es")
	
	palabra = palabra.lower()
	
	sch=engine.search(palabra)
	debug(palabra)
	# ~ debug(vars(sch))
	# ~ debug(dir(sch))
	if sch != None:
		# ~ debug(sch.string)
		# ~ debug(sch.source)
		pos_1 = sch.source.find('<dt>1</dt>')
		
		if pos_1 == -1:
			debug(pos_1)
			pos_1 = sch.source.find('<dt>')
			debug( pos_1 )
			pos_cierre_1 = sch.source.find('</dt>',pos_1+1) #busca a partir de pos 1
			debug( pos_cierre_1 )
		else:
			pos_cierre_1 = pos_1
			
		pos_2 = sch.source.find('<dt>2</dt>',pos_1+1)
		if pos_2 == -1:
			debug(pos_2)
			pos_2 = sch.source.find('<dt>',pos_1+1)
			debug(pos_2)
			pos_cierre_2 = sch.source.find('</dt>',pos_2+1)
		else:
			pos_cierre_2 = pos_2
		
		print(pos_cierre_1, pos_2)
		debug(sch.source[pos_cierre_1: pos_2])

		debug(plaintext(sch.source[pos_cierre_1:pos_2]))
		
		pos_punto=plaintext(sch.source[pos_cierre_1:pos_2]).find('.')
		

		definicion = plaintext(sch.source[pos_cierre_1: pos_2])
		debug(definicion[:pos_punto+1])
		if definicion[:1] == '1':
			debug(definicion[1:pos_punto+1])
		# ~ debug(sch.title)
		# ~ debug(sch.categories)
		# ~ debug(sch.sections)
		# ~ debug(dir(sch.sections[0]))
		# ~ for section in sch.sections:
			# ~ for children in section.children:
				# ~ if section.title == 'Español' or section.title == palabra:
					# ~ debug(section)
					# ~ debug(section.content)
					# ~ debug(section.string)
					# ~ debug(section.children)
					# ~ for sub in section.children:
						# ~ debug(sub)
						# ~ debug(sub.content)
					
					# ~ patron = re.compile('a[3-5]+')
					# ~ if len(section.children) > 1:
						# ~ debug(section.children[1])
						# ~ sss= section.children[1].content
						# ~ debug(sss)
						
						# ~ s1 = sss.find('1')

						# ~ s_ = sss.find('.')

						# ~ s2 = sss.find('2')

						# ~ debug(sss[s1:s_+1])
		
		
		# ~ if('ES:Sustantivos' in sch.categories):
			# ~ print('es sustantivo!')
		# ~ if('ES:Adjetivos' in sch.categories):
			# ~ print('es Adjetivo!')
		# ~ if('ES:Verbos' in sch.categories):
			# ~ print('es verbo!')
	else:
		print('No la encuentra!!')
	# ~ return resultado
if __name__ == "__main__":
	while(palabra!='q'):
		buscar_en_wiktionary(palabra)
		palabra = input('\n--------------------------------------------------------------------------\nPalabra :')

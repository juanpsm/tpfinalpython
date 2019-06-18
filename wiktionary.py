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

from pattern.web import Wikipedia, SEARCH, Wiktionary
import re
palabra = 'tancat'
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
	return resultado
	
	
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
	sch=engine.search(palabra)
	# ~ print('\n obj:',sch)
	# ~ print('\n dir:',dir(sch))
	if sch != None:
		# ~ print('\n title',sch.title)
		# ~ print('\n cat',sch.categories)
		print('\n sec',sch.sections)
		# ~ print('\n sec type elemtos',dir(sch.sections[0]))
		for x in sch.sections:
			if x.title == 'Español':
				print('\n x',x)
				# ~ print('\n x.string',x.string)
				# ~ print('\n x.children',x.children)
				# ~ for sub in x.children:
					# ~ print('\n sub',sub)
					# ~ print('\n sub content',sub.content)
				
				# ~ patron = re.compile('a[3-5]+')
				
				sss= x.children[1].content
				t = sss.find('1')
				t2 = sss.find('.')
				t3 = sss.find('2')
				print('\n-------------',sss[t+1:t+20])
				print('\n-------------',sss[t+1:t2])
				print('\n-------------',sss[t+1:t3])
				print(len(sss))
		
		
		if('ES:Sustantivos' in sch.categories):
			print('es sustantivo!')
		if('ES:Adjetivos' in sch.categories):
			print('es Adjetivo!')
		if('ES:Verbos' in sch.categories):
			print('es verbo!')
	# ~ for result in engine.search('papa'):
	   # ~ print ('\n title',result.title)
	   # ~ print ('\n text', result)
	   # ~ print('\n result',result)
	   # ~ print(dir(result))
	   
	return resultado
if __name__ == "__main__":
	buscar_en_wiktionary(palabra)

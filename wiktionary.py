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
engine = Wiktionary(license=None, throttle=1.0, language="es") # Enter your license key.
sch=engine.search('violin')
print('\n obj:',sch)
print('\n dir:',dir(sch))
if sch != None:
 print('\n txt:',sch.plaintext)
 print('\n title',sch.title)
 print('\n cat',sch.categories)
 print('\n sec',sch.sections)
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

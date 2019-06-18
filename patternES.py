from pattern.es import verbs, conjugate, INFINITIVE, parse, parsetree,tokenize,tag
from pattern.search import search

string='acentuar'
palabra =string
tokenize(string, punctuation=".,;:!?()[]{}`''\"@#$^&*+-|=~_", replace={})
bb = tag(string, tokenize=True, encoding='utf-8')[0][1]

print(string)
print('tag:',bb)

print('Pattern.es dice que es')
#Common part-of-speech tags are NN (noun), VB (verb), JJ (adjective), RB (adverb) and IN (preposition).
tokenize(palabra, punctuation=".,;:!?()[]{}`''\"@#$^&*+-|=~_", replace={})
tipo = tag(palabra, tokenize=True, encoding='utf-8')[0][1]
print('Tipo:',tipo)
if tipo == 'NN':
	print('SUSTANTIVO')
if tipo == 'VB':
	print('Verbo')
if tipo == 'JJ':
	print('ADJETIVO')
if tipo == 'RB':
	print('Adverbio')
if tipo == 'IN':
	print('Preposición')

print()
#Common part-of-speech tags are NN (noun), VB (verb), JJ (adjective), RB (adverb) and IN (preposition).
for word, pos in tag('Egctñl veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja.'):
	print(word,pos, end=' | ')
print()
print()

from pattern.en import wordlist

#print(wordlist.PROFANITY)


from pattern.en import wordnet
import random

seguir = ''
while (seguir==''):
	word = random.choice(wordlist.PROFANITY)
	print()
	print('--------------')
	print ('Palabra:',word)
	s = wordnet.synsets(word)
	print()
	print()
	print ('sets:', s)
	for i in range(len(s)):
		print()
		print ('Definition',s[i],':', s[i].gloss)
		print('synonims: ',s[i].synonyms)
	seguir=input()
#import pattern.es
#print (dir(pattern.es))

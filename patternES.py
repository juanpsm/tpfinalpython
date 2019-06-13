from pattern.es import verbs, conjugate, INFINITIVE, parse, parsetree,tokenize,tag
from pattern.search import search

string='baba'

tokenize(string, punctuation=".,;:!?()[]{}`''\"@#$^&*+-|=~_", replace={})
bb = tag(string, tokenize=True, encoding='utf-8')[0][1]

print(string)
print('tag:',bb)

print()
#Common part-of-speech tags are NN (noun), VB (verb), JJ (adjective), RB (adverb) and IN (preposition).
for word, pos in tag('El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja.'):
	print(word,pos, end=' | ')
print()
print()

from pattern.en import wordlist
 
#print(wordlist.PROFANITY)


from pattern.en import wordnet
import random

while (input()==''):
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

import pattern.es
print (dir(pattern.es))

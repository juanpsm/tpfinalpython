from pattern.es import verbs, conjugate, INFINITIVE, parse, parsetree,tokenize,tag
from pattern.search import search

string='papa'

tokenize(string, punctuation=".,;:!?()[]{}`''\"@#$^&*+-|=~_", replace={})
bb = tag(string, tokenize=True, encoding='utf-8')[0][1]
print(string)

print('tag:',bb)
pos = tag(string, tokenize=True, encoding='utf-8')[0][1]
print('pos:',pos)
#Common part-of-speech tags are NN (noun), VB (verb), JJ (adjective), RB (adverb) and IN (preposition).
for word, pos in tag('I feel *happy*!'):
	if pos == "JJ": # Retrieve all adjectives.
		print(word)

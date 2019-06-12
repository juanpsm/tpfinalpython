import PySimpleGUI as sg
import random
import string
from pattern.web import Wiktionary
from pattern.es import verbs, conjugate, INFINITIVE, parse, parsetree, tokenize,tag
from pattern.search import search

def analizarpalabra(palabra,cat):
	print(palabra)
	print(cat)
	engine = Wiktionary(license=None, throttle=1.0, language="es") # Enter your license key.
	sch=engine.search(palabra)
	
	print('Wiktionary dice que')
	if sch != None:
		if('ES:Sustantivos' in sch.categories):
			print('es sustantivo!')
		if('ES:Adjetivos' in sch.categories):
			print('es Adjetivo!')
		if('ES:Verbos' in sch.categories):
			print('es verbo!')
	else:
		print('no se encuentra en wiktionary')

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
layout = [
			[sg.Text('Instrucciones de configuracion')],
			[sg.Text('Palabra:')],
			[sg.Radio('Adjetivo', "RADIOp",key='esAdj'),
			 sg.Radio('Verbo', "RADIOp",key='esVer'),
			 sg.Radio('Sustantivo', "RADIOp",key='esSus')],
			[sg.Input(key='_IN_')],
			[sg.Button('Agregar',key='_ADD_')],
			[sg.Text('Ayudas:')],
			[sg.Radio('Sin ayuda', "RADIOA", size=(10,1)),
			 sg.Radio('Definiciones', "RADIOA"),
			 sg.Radio('Mostrar palabras', "RADIOA")],
			 
			[sg.Text('Orientacion')],
			[sg.Radio('Horizontal', "RADIOH", size=(10,1)),
			 sg.Radio('Vertical', "RADIOH")],
			
			[sg.Text('Cantidad de Palabras')],
			[sg.Text('Adjetivo'),sg.Input(do_not_clear=True, key='_CANT_ADJ_')],
			[sg.Text('Verbo'),sg.Input(do_not_clear=True, key='_CANT_VER_')],
			[sg.Text('Sustantivo'),sg.Input(do_not_clear=True, key='_CANT_SUS_')],
			
			[sg.Text('Mayus')],
			[sg.Radio('Mayúscula', "RADIOn", size=(10,1)),
			 sg.Radio('Minúscula', "RADIOn")],
			 
   			[sg.Text('Fuente')],
   			[sg.InputCombo(('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'), key='_FONT_')],
			[sg.Text('Oficina')],
			[sg.Button('Cerrar')]
			]
window = sg.Window('CONFIG GUI').Layout(layout)
window.Finalize()

while True:                 # Event Loop  
	event, values = window.Read()  
	#print(event, val)
	if event is None or event == 'Cerrar':  
		break
	if event == '_ADD_':
		print('values',values)
		cat={'esAdj':values['esAdj'],'esVer':values['esVer'],'esSus':values['esSus']}
		analizarpalabra(values['_IN_'],cat)

window.Close()

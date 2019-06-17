import PySimpleGUI as sg
import random
import string
import json
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
			[sg.Radio('Sustantivo', "RADIOp",default = True,key='esSus'),
			 sg.Radio('Adjetivo', "RADIOp",key='esAdj'),
			 sg.Radio('Verbo', "RADIOp",key='esVer')],
			 
			[sg.Input(key='_IN_')],
			[sg.Button('Agregar',key='_ADD_')],
			[sg.Text('Ayudas:')],
			[sg.Radio('Sin ayuda', "RADIOA",default = True, key= 'sin', size=(10,1)),
			 sg.Radio('Definiciones', "RADIOA", key='defin'),
			 sg.Radio('Mostrar palabras', "RADIOA", key='pal')],
			 
			[sg.Text('Orientacion:')],
			[sg.Radio('Horizontal', "RADIOH",default = True, key='hor', size=(10,1)),
			 sg.Radio('Vertical', "RADIOH", key='ver'), sg.Radio('Mixto', "RADIOH", key='mix')],
			
			[sg.Text('Cantidad de Palabras')],
			[sg.Text('Adjetivo'),sg.Input(do_not_clear=True, key='_CANT_ADJ_')],
			[sg.Text('Verbo'),sg.Input(do_not_clear=True, key='_CANT_VER_')],
			[sg.Text('Sustantivo'),sg.Input(do_not_clear=True, key='_CANT_SUS_')],
			
			[sg.Text('Mayus')],
			[sg.Radio('Mayúscula', "RADIOn",default = True, key='mayus', size=(10,1)),
			 sg.Radio('Minúscula', "RADIOn", key='minus')],
			 
   			[sg.Text('Fuente')],
   			[sg.InputCombo(('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'), key='_FONT_')],
			[sg.Text('Oficina')],
			[sg.Button('Aceptar', key='_ACEPTAR_'),sg.Button('Cerrar')]
			]
window = sg.Window('CONFIG GUI').Layout(layout)
window.Finalize()

config={}
palabras={}
while True:                 # Event Loop  
	event, values = window.Read()  
	#print(event, val)
	if event is None or event == 'Cerrar':  
		break
	if event == '_ADD_':
		print('values',values)
		cat={'esAdj':values['esAdj'],'esVer':values['esVer'],'esSus':values['esSus']}
		analizarpalabra(values['_IN_'],cat)
		palabras[values['_IN_']]={'tipo': 'adj' if values['esAdj']==True else 'verb' if values['esVer']==True else 'sust', 'def':''}
		#print(palabras)
	if event == '_ACEPTAR_':
		config['palabras']=palabras	
		config['ayuda']= "sin ayuda" if values['sin']==True else "definiciones" if values['defin']==True else "palabras" 
		config['orientacion'] = "horizontal" if values['hor']==True else "vertical" if values['ver']==True else "mixto"
		config['mayuscula'] = True if values['mayus']==True else False
		config['fuente'] = values['_FONT_']
		for key in config:
			print(key, '=',config[key])
		break	
window.Close()
with open('configuracion.json', 'w') as f:
	json.dump(config, f)



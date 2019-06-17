import PySimpleGUI as sg
import random
import string
import json
from pattern.web import Wiktionary
from pattern.es import verbs, conjugate, INFINITIVE, parse, parsetree, tokenize,tag
from pattern.search import search
import os

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

def configuracion():
	config_dicc={}
	

	nombre_archivo = 'configuracion.json'
	existe = os.path.isfile(nombre_archivo)
	if existe:
		with open(nombre_archivo, 'r') as f:
			config_dicc = json.load(f)
		print('Configuracion guardada:')
		print(json.dumps(config_dicc, sort_keys=True, indent=4))
		palabras_dicc = config_dicc['palabras']
	else:
		config_dicc['palabras'] = []
		palabras_dicc = {}
		print('no existe archivo de configuracion')
	palabras_lista = list(palabras_dicc.keys())
	
	# ------ Menu Definition ------ #      
# ~ menu_def = [['&File', ['&Open', '!&Save', '---', 'Properties', 'E&xit'  ]],      
            # ~ ['!&Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],      
            # ~ ['&Help', '&About...'],]    
	#layout = [[sg.Menu(menu_def)]]
	menu = ['Menu', ['Definicion::_MENU_', 'Eliminar::_MENU_']]
	print(config_dicc['palabras'])
	layout = [
			[sg.Text('Instrucciones de configuracion')],
			[sg.Text('Palabra:')],
			[sg.Radio('Sustantivo', "RADIOp",default = True,key='_esSus_'),
			 sg.Radio('Adjetivo', "RADIOp",key='_esAdj_'),
			 sg.Radio('Verbo', "RADIOp",key='_esVer_')],
			 
			[sg.Input(key='_IN_', do_not_clear=False)],
			[sg.Button('Agregar', bind_return_key=True, key='_ADD_')],
			
			[sg.Listbox(values=palabras_lista, default_values=None, enable_events=True, size=(90,6),
									key='_LISTA_', tooltip=None, right_click_menu= menu, visible=True)],
			
			[sg.Text('Ayudas:')],
			[sg.Radio('Sin ayuda', "RADIOA", key= 'sin', size=(10,1)),
			 sg.Radio('Definiciones', "RADIOA", key='defin'),
			 sg.Radio('Mostrar palabras', "RADIOA", default = True, key='pal')],
			
			[sg.Text('Orientacion:')],
			[sg.Radio('Horizontal', "RADIOH",default = True, key='hor', size=(10,1)),
			 sg.Radio('Vertical', "RADIOH", key='ver'), sg.Radio('Mixto', "RADIOH", key='mix')],
			
			[sg.Text('Mayus')],
			[sg.Radio('Mayúscula', "RADIOn", key='mayus', size=(10,1)),
			 sg.Radio('Minúscula', "RADIOn", key='minus')],
			
			[sg.Text('Fuente')],
			[sg.InputCombo(('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'), key='_FONT_')],
			
			[sg.Text('Oficina')],
			[sg.Button('Guardar configuracion', key='_ACEPTAR_', disabled = True),sg.Button('Cerrar')]
			]
	window = sg.Window('CONFIGURACION').Layout(layout)

	print(config_dicc)

	while True:                 # Event Loop  
		event, val = window.Read()  
		print('EVENTO :',event,'\n----\n VAL = ',val,'\n-----\n')
		# ~ print(window.FindElement('_LISTA_').GetListValues())
		if event is None or event == 'Cerrar':  
			break
		if event == '_ADD_':
			categoria = 'adj' if val['_esAdj_'] else 'verb' if val['_esVer_'] else 'sust'
			definicion = ''
			#######################analizarpalabra(val['_IN_'],cat)
			
			palabras_dicc[ val['_IN_'] ] = {'tipo': categoria,
										'def': definicion}
			
			palabras_lista = window.FindElement('_LISTA_').GetListValues()
			palabras_lista.append(val['_IN_'])

			window.FindElement('_LISTA_').Update(values = palabras_lista)
			
		if event == 'Definicion::_MENU_':
			print('def = ',val['_LISTA_'])
			
			
		if event == 'Eliminar::_MENU_':
			del palabras_dicc[val['_LISTA_'][0]]# El Listbox guarda en val una lista con un unico elemento que es el que esta seleccionado en ese momento.
			palabras_lista = window.FindElement('_LISTA_').GetListValues()
			palabras_lista.remove(val['_LISTA_'][0])
			window.FindElement('_LISTA_').Update(values = palabras_lista)
			
		if event == '_ACEPTAR_':
			config_dicc['palabras'] = palabras_dicc
			config_dicc['ayuda'] = "sin ayuda" if val['sin'] else "definiciones" if val['defin'] else "palabras" 
			config_dicc['orientacion'] = "horizontal" if val['hor'] else "vertical" if val['ver'] else "mixto"
			config_dicc['mayuscula'] = val['mayus']
			config_dicc['fuente'] = val['_FONT_']
			for key in config_dicc:
				print(key, '=',config_dicc[key])
			break
	print(val['mayus'])
	# ~ if ():
		# ~ window.FindElement('_ACEPTAR_').Update(disabled = False)
	window.Close()
	with open(nombre_archivo, 'w') as f:
		json.dump(config_dicc, f)


# ~ cantv,cantadj,cantsust,total= cantidad_pal(verbos,adjetivos,sustantivos)
	# ~ if values['sin ayuda'] == True:
		# ~ column1 = [
				# ~ [sg.T('Total de palabras a buscar palabras a buscar: ' + str(total), justification='center')],
				# ~ [sg.T('Verbos: '+ str(cantv)),
				# ~ sg.T('Adjetivos: '+ str(cantadj)),
				# ~ sg.T('Sustantivos: '+ str(cantsust))]
				# ~ ]
		# ~ layout.append(([sg.Column(column1, background_color='#77BA99')]))		
	# ~ elif values[' definiciones'] == True:
		# ~ column1 = [
			# ~ [sg.Text('ayuda: palabras a buscar. ', background_color='#77BA99', justification='center')],
            # ~ [sg.T(verbos[j])for j in range(cantv)],
            # ~ [sg.T(adjetivos[j])for j in range(cantadj)],
            # ~ [sg.T(sustantivos[j])for j in range(cantsust)]
            # ~ ]
		# ~ layout.append(([sg.Column(column1, background_color='#F7F3EC')]))    
	# ~ elif values['mostrar palabras'] == True:
		# ~ column1 = [
			# ~ [sg.Text('ayuda: palabras a buscar. ', background_color='#77BA99', justification='center')],
            # ~ [sg.T(verbos[j])for j in range(cantv)],
            # ~ [sg.T(adjetivos[j])for j in range(cantadj)],
            # ~ [sg.T(sustantivos[j])for j in range(cantsust)]
            # ~ ]
		# ~ layout.append(([sg.Column(column1, background_color='#F7F3EC')]))

if __name__ == "__main__":
	configuracion()


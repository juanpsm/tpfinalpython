# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import random
import string
import json
import os
import datetime
from pprint import pprint
from collections import defaultdict
from buscar_en_wiktionary import buscar_en_wiktionary

nombre_archivo_config = 'configuracion.json'
nombre_archivo_reporte = 'reporte_de_errores.txt'
MAX = 10
def reporte(r,error):
	"""pone en archivo de texto un reporte de los errores encontrados en la ejecucion de la sopa de letras"""
	""" recibe un numero de error y en base a el informa que tipo de error es"""
	hora = datetime.datetime.now()
	hora = str(hora)[:-10]
	
	if error == 1:
		texto = '[{}] {}: Wiktionario la clasificó como "{}" y pattern como "{}".\n'.format(hora,r['palabra'],r['clasificacion_wiktionario'],r['clasificacion_pattern'])
	
	elif error ==2:
		texto = '[{}] El termino "{}": no se encontró en ningun motor de busqueda.\n'.format(hora,r['palabra'])

	print('Error {}:{}'.format(error,texto))
	
	existe = os.path.isfile(nombre_archivo_reporte)
	if existe:
		f = open(nombre_archivo_reporte, 'a', encoding = 'utf-8')
	else:
		f = open(nombre_archivo_reporte, 'w', encoding = 'utf-8')
		print('Se ha creado un reporte de errores en',nombre_archivo_reporte)
	f.write(texto)
	f.close()
	

def analizarpalabra(palabra,cat):
	#recibo categoria pero en la consigna no la piden, tengo que extraerla de los motores.
	#Si funciona esto bien, si no nos queadremos con nuestro metodo de ponerla manualmente.
	resultado = buscar_en_wiktionary(palabra)
	# resultado tiene los campos:
	# 'palabra' [str] la que busqué
	# 'clasif_wik' [str] si se encontro en wiktionario
	# 'clasif_patt' [str] si se encontro en pattern
	# 'definicion' [str] si se encontro en wiktionario
	# los campos que no se pudieron recuperar tendran None
	clasificacion_definitiva = resultado['clasificacion_pattern']
	definicion = resultado['definicion']
	
	if resultado['clasificacion_wiktionario'] != resultado['clasificacion_pattern'] and resultado['clasificacion_wiktionario'] != 'MIXTA':
		
		clasificacion_definitiva = resultado['clasificacion_wiktionario']

		if resultado['clasificacion_wiktionario'] == '_Ninguna_': # y como son distintas se supone que pattern dio distinto de None
			# aca el problema es que pattern siempre da NN por DEFECTO, pero bueno si seguimos la consigna..
			# EDIT: ahora anda!!
			clasificacion_definitiva = resultado['clasificacion_pattern']
			
			ingreso = [	[sg.T('No se encontro la palabra en Wiktionario.\nDefínala:\n')],
						[sg.Radio('Sustantivo', "RADIOp",default = True,key='_esSus_'), 
						sg.Radio('Adjetivo', "RADIOp",key='_esAdj_'),
						sg.Radio('Verbo', "RADIOp",key='_esVer_')],
						[sg.Input(key = 'def')],
						[sg.Submit(key = 'submit'),sg.Cancel(key = 'cancel')]
						]
			window2 = sg.Window('Definicion ').Layout(ingreso)
			button,values2=window2.Read()
			if button == 'cancel':
				clasificacion_definitiva = '_cancelada_'
				definicion = '_cancelada_'
			if button == 'submit':
				definicion = values2['def']
				clasificacion_definitiva = 'adj' if values2['_esAdj_'] else 'verb' if values2['_esVer_'] else 'sust'
			window2.Close()
			#definicion = input('No se encontro la palabra en Wiktionario.\nDefínala:\n') #Aca habría que hacer un popup
		print('Reportando Error 1...')
		reporte(resultado, 1)
		
	elif resultado['clasificacion_pattern'] == '_Ninguna_': # Las dos None
		print('Reportando Error 2...')
		reporte(resultado,2)
		#no incluir palabra
		clasificacion_definitiva = '_no_aceptada_'
		definicion = '_no_aceptada_'
	
	return clasificacion_definitiva, definicion
	
def cargar_configuracion():
	"""Abre archivo json con la configuración cargada anteriormente.
	si el archivo de configuracion no fue cargado previamente informa que no existe el mismo,
	inicializa las estructuras vacías para poder cargarle nuevas en el futuro.


	Retorna: (config_dicc, palabras_dicc, palabras_clas)
	
	"""
	existe = os.path.isfile(nombre_archivo_config)
	if existe:
		with open(nombre_archivo_config, 'r', encoding = 'utf-8') as f:
			config_dicc = json.load(f)
		# ~ print('Configuracion cargada:')
		# ~ print(json.dumps(config_dicc, sort_keys=True, indent=4, ensure_ascii = False))
		palabras_dicc = config_dicc['palabras']
		
		palabras_clas = config_dicc['palabras_clas']
		
	else:
		config_dicc = {}
		config_dicc['palabras'] = {}
		config_dicc['palabras_clas'] = {'sust':[],'verb':[],'adj':[]}
		palabras_dicc = {}
		palabras_clas = {'sust':[],'verb':[],'adj':[]}
		config_dicc['max_sust'] = 0
		config_dicc['max_verb'] = 0
		config_dicc['max_adj'] = 0
		
		print('No existe archivo de configuración')
	print( 'wqerffffffff->', config_dicc['orientacion'] )
	return config_dicc,palabras_dicc,palabras_clas
	
def obtener_lista_palabras(config_dicc):
	'''Este metodo es para elegir aleatoriamente palabras, respentando las cantidades 
	máximas definidas para cada tipo.'''

	lista_s = config_dicc['palabras_clas']['sust']
	lista_v = config_dicc['palabras_clas']['verb']
	lista_a = config_dicc['palabras_clas']['adj']
	
	cant = min ( len(lista_s), config_dicc['max_sust'] ) # tambien puedo comprobarlo antes y que max nunca tenga algo mayor que el largo de la lista
	palabras_rand = random.sample(lista_s, cant)
	
	cant = min ( len(lista_v), config_dicc['max_verb'] )
	palabras_rand.extend(random.sample(lista_v, cant))
	
	cant = min ( len(lista_a), config_dicc['max_adj'] )
	palabras_rand.extend(random.sample(lista_a, cant))
	
	return palabras_rand
	
def colores():
	## Esto habrá que setearlo luego con la raspberry
	sg.ChangeLookAndFeel('Reddit')
	## Puedo setear los Colores de la interfaz manualmente
	sg.SetOptions(
	icon = 'bee.ico',
	text_color='black',
	input_text_color='black',
	background_color='#EFF0D1', #cremita
	text_element_background_color='#EFF0D1',
	element_background_color='#EFF0D1',
	scrollbar_color=None,
	input_elements_background_color='#EFF0D1', #lila
	progress_meter_color = ('green', 'blue'),
	button_color = ('#262730','#5adbff') # celeste
	)
	
	## o automaticamente con 
	# ~ sg.ListOfLookAndFeelValues()
	#['SystemDefault', 'Reddit', 'Topanga', 'GreenTan', 'Dark', 'LightGreen', 'Dark2', 'Black', 'Tan', 'TanBlue',
	# 'DarkTanBlue', 'DarkAmber', 'DarkBlue', 'Reds', 'Green', 'BluePurple', 'Purple', 'BlueMono', 'GreenMono',
	# 'BrownBlue', 'BrightColors', 'NeutralBlue', 'Kayak', 'SandyBeach', 'TealMono']
	#Temas "FRIOS":[]
	
	# ~ sg.ChangeLookAndFeel('TealMono')
	
	return ('#262730','#EFF0D1') #·nego y crema
	
def configuracion():
	"""recibe de cargar_configuracion() la configuracion elegida por el usuario para la sopa de letras"""
	
	
	color_fondo = colores()
	color_sel = ('#EFF0D1', '#D33F49')
	orientacion = 'dirs_1' #por defecto
	
	config_dicc, palabras_dicc, palabras_clas = cargar_configuracion()

	palabras_lista = list(palabras_dicc.keys()) ## esto lovoy a usar apra popular el listbox
	
	TOTAL_PALABRAS_A_USAR = config_dicc['max_sust']+config_dicc['max_verb']+config_dicc['max_adj']
	
	print('Configuración cargada:')
	pprint (config_dicc)

	menu = ['Menu', ['Definicion::_MENU_',
					 'Eliminar::_MENU_'
					]
			]
	# print(config_dicc['palabras'])
	layout = [
		[sg.Text('Ingrese palabras la lista para ser usadas por la sopa de letras:')],

		[sg.Text('Instrucciones de configuración')],
		[sg.Frame(title='Ingrese palabras',
			layout = [	[sg.Input(key = '_IN_', do_not_clear = False)],
						[sg.Button('Agregar', bind_return_key = True, key = '_ADD_')],
						[sg.Listbox(values = palabras_lista, enable_events = True, size = (15,6),
									key = '_LISTA_', tooltip = 'gato', right_click_menu = menu)]
					])
		],
		## para implementar una lista por cada tipo
		# ~ sg.Listbox(values=[], default_values=None, enable_events=True, size=(15,6),
					# ~ key='_LISTA_V_', tooltip=None, right_click_menu= menu, visible=True),
		# ~ sg.Listbox(values=palabras_lista, default_values=None, enable_events=True, size=(15,6),
					# ~ key='_LISTA_A_', tooltip=None, right_click_menu= menu, visible=True)],
		[sg.Frame(title = 'Cantidad máxima de cada tipo a utilizar en la Sopa:', 
		## hago una lista de numeros de cero al minimo entre la cantidad de palabras existentes
		## y la cantidad maxima para que no se haga muy grande la grilla.
			layout = [	[sg.Column([	[sg.Text('Sustantivos:', pad=((0,),2) )],
										[sg.Combo( list( range( 0, 1 + min( MAX, len(config_dicc['palabras_clas']['sust']) ))),
							 				key = '_CANT_S_', default_value = config_dicc['max_sust'], size = (2,1), pad=((20,),1), change_submits = True)]
						 			], pad=((0,),2) ),	
				 		 sg.Column([	[sg.Text('Verbos:', pad=((0,),2) )],
						  				[
										  sg.Combo( list( range( 0, 1 + min( MAX, len(config_dicc['palabras_clas']['verb'])))),
										  key = '_CANT_V_', default_value = config_dicc['max_verb'], size = (2,1), change_submits = True, disabled = True)]
				 					], pad=((0,),2) ),
						 sg.Column([	[sg.Text('Adjetivos:', pad=((0,),2) )],
										[
											sg.Combo( list( range( 0, 1 + min( MAX, len(config_dicc['palabras_clas']['adj'])))),
					 						key = '_CANT_A_', default_value = config_dicc['max_adj'], size = (2,1), change_submits = True, disabled = True)]
									], pad=((0,),2) ),
				 		sg.Frame(title = 'Total:',
				 			layout = [	[sg.T(' '*3), sg.Text(TOTAL_PALABRAS_A_USAR, key='_TOTAL_')]
				 					 ], pad=((0,),2) )
						]
					])
		],
		[sg.Frame(title= 'Ayudas',
			layout = [	[sg.Radio('Sin ayuda', "RADIOA", key= 'sin', size=(10,1)),
						 sg.Radio('Definiciones', "RADIOA", key='defin'),
						 sg.Radio('Mostrar palabras', "RADIOA", default = True, key='pal')
						]
					])
		],
		[sg.Frame(title = 'Orientacion', 
			layout = [	[sg.Button('', image_filename='dirs_1.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_1', button_color=color_sel if config_dicc['orientacion']=='dirs_1' else color_fondo),
						 sg.Button('', image_filename='dirs_2.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_2', button_color=color_sel if config_dicc['orientacion']=='dirs_2' else color_fondo),
						 sg.Button('', image_filename='dirs_3.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_3', button_color=color_sel if config_dicc['orientacion']=='dirs_3' else color_fondo),
						 sg.Button('', image_filename='dirs_4.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_4', button_color=color_sel if config_dicc['orientacion']=='dirs_4' else color_fondo),
						 sg.Button('', image_filename='dirs_8.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_8', button_color=color_sel if config_dicc['orientacion']=='dirs_8' else color_fondo),
						]
			])
		],		 
		[sg.Frame(title = 'Mayúscula/Minúscula',
			layout = [	[sg.Radio('Mayúscula', "RADIOn", key='mayus', default = True, size=(10,1)),
						 sg.Radio('Minúscula', "RADIOn", key='minus')
						]
			]),
		 sg.Frame(title = 'Fuente',
			layout = [	[sg.Combo(	('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'),
								default_value='Comic',
								key='_FONT_')
						]
			])
		],
		[sg.Frame(title = 'Oficina',
			layout = [	[sg.Text('15')]
			]),
		 sg.Button('Guardar configuración', key='_ACEPTAR_', pad = ((150,5),1), disabled = False),
		 sg.Button('Cerrar')]
	]

	window = sg.Window('CONFIGURACIÓN').Layout(layout)

	while True:                 # Event Loop  
		# pprint (config_dicc)
		event, val = window.Read()  
		# print('EVENTO :',event,'\n----\n VAL = ',val,'\n-----\n')
		# print(window.FindElement('_LISTA_').GetListValues())
		if event is None or event == 'Cerrar':  
			break
			
		if event == '_ADD_':
			palabra = val['_IN_']  #Guardo lo que puso en el imput
			categoria = '' # inicializo
			definicion = ''
			
			if palabra != '': # descarto vacías
				if palabra in palabras_dicc:
					print('Ya se encuentra esa palabra en la lista.')
				else:# si es no vacia y no esta en la lista, la analizo
					
					categoria, definicion = analizarpalabra(palabra,categoria)
					# devolvera no aceptada si no la encuentra en ningun lado o cancelada si la encuentra pero el usuariocancela a la hora de 
					# agregar la definicion.
					if definicion == '_no_aceptada_': 
						sg.Popup('No consideramos que "'+palabra+'" sea una palabra')
					
					elif definicion != '_cancelada_': # la agrego en las estructuras
						palabras_dicc[palabra] = {'tipo': categoria,'def': definicion}
						palabras_clas[categoria].append(palabra) # ojo inicializar siempre antes los diccionarios
						
						palabras_lista = window.FindElement('_LISTA_').GetListValues()
						palabras_lista.append(palabra)  # aca cargo y agrego a la lista, pordría agregar directamente porque ya definí la lista en la importacion.
						window.FindElement('_LISTA_').Update(values = palabras_lista)
		
		if event == 'Definicion::_MENU_':
			try: # aca hay problemas cuando no hay nada seleccionado, se puede resolver seteando un valor por defecto, aunque eso traeria problemas la primera vez que se carga, se puede resolver con exepciones
				texto = 'Definición de "'+val['_LISTA_'][0]+'":\n'
				texto += 'La palabra es un '+palabras_dicc[ val['_LISTA_'][0] ]['tipo']+'.\n'
				texto += palabras_dicc[ val['_LISTA_'][0] ]['def']
				sg.Popup(texto)
			except(KeyError):
				print(val['_LISTA_'][0])
			except(IndexError):
				print(val['_LISTA_'])
			
		if event == 'Eliminar::_MENU_':
			if val['_LISTA_'] != []: # otra forma de resolver el tema de la listbox sin seleccionar
				palabra = val['_LISTA_'][0]# El Listbox guarda en val una lista con un unico elemento que es el que esta seleccionado en ese momento.
				#elimino de ambdas estructuras:
				palabras_clas[palabras_dicc[palabra]['tipo']].remove(palabra)
				del palabras_dicc[palabra]
				
				palabras_lista = window.FindElement('_LISTA_').GetListValues()
				palabras_lista.remove(palabra)
				window.FindElement('_LISTA_').Update(values = palabras_lista)
				print('Se eliminó',palabra)
		
		if event in ('dirs_1','dirs_2','dirs_3','dirs_4','dirs_8'):

			window.Element(event).Update( button_color = color_sel ) # pinto este boton como seleccionado
			lista_dirs = ['dirs_1','dirs_2','dirs_3','dirs_4','dirs_8']
			lista_dirs.remove(event)
			for x in lista_dirs:  # pinto todos menos el actual del color del fondo
				window.Element(x).Update(button_color = color_fondo)
			
			orientacion = event
		
		lista_cant = ['_CANT_S_','_CANT_V_','_CANT_A_']
		if event in lista_cant:
			if event == '_CANT_S_':  # voy seteando el tope del siguiente segun MAX - actual, lo habilito y lo seteo en cero.
				window.Element('_CANT_V_').Update(values = list( range( 0, 1 + MAX - int(val[event]) ) ) , disabled = False, set_to_index = 0 )
			if event == '_CANT_V_':
				window.Element('_CANT_A_').Update(values = list( range( 0, 1 + MAX - int(val[event]) - int(val['_CANT_S_']) ) ) , disabled = False, set_to_index = 0 )
			TOTAL_PALABRAS_A_USAR = int(val['_CANT_S_']) + int(val['_CANT_V_']) + int(val['_CANT_A_'])
			window.Element('_TOTAL_').Update(value = TOTAL_PALABRAS_A_USAR )
				
		##LLeno diccionario
		config_dicc['palabras'] = palabras_dicc
		config_dicc['palabras_clas'] = palabras_clas
		config_dicc['ayuda'] = "sin ayuda" if val['sin'] else "definiciones" if val['defin'] else "palabras" 
		config_dicc['orientacion'] = orientacion
		config_dicc['mayuscula'] = val['mayus']
		config_dicc['fuente'] = val['_FONT_']
		config_dicc['max_sust'] = int(val['_CANT_S_'])
		config_dicc['max_verb'] = int(val['_CANT_V_'])
		config_dicc['max_adj'] = int(val['_CANT_A_'])
		
		if event == '_ACEPTAR_':
			if TOTAL_PALABRAS_A_USAR == 0:
				sg.PopupError('La cantidad de palabras\n no puede ser cero')
			else:
				with open(nombre_archivo_config, 'w', encoding = 'utf-8') as f:
					json.dump(config_dicc, f, ensure_ascii = False)
				print('Configuración guardada:\n')
				pprint (config_dicc)
		
		if event == '_LISTA_':
			print ('Seleccionado: ',val['_LISTA_'])
			
	window.Close()

if __name__ == "__main__":
	configuracion()



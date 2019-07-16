# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import random
import string
import json
import os
import time
import datetime

from pprint import pprint
from collections import defaultdict
from buscar_en_wiktionary import buscar_en_wiktionary
from creador_registro_test import crear_registro


listaColores= {'rojo': ('#EFF0D1','#f05959'),'violeta':('#262730','#c382ff'),'verde':('#262730','green3'),'amarillo':('#262730','yellow2'),'azul':('#262730','#1282cc')}

nombre_archivo_config = 'configuracion.json'
nombre_archivo_reporte = 'reporte_de_errores.txt'
nombre_archivo_registro = 'registros_temp_hum.json'
## con MAX seteamos el numero maximo de palabras a usar en total entre sust verb y adj.
MAX = 10
def reporte( res, error, clas, defi ):
	"""pone en archivo de texto un reporte de los errores encontrados en la ejecucion de la sopa de letras"""
	""" recibe un numero de error y en base a el informa que tipo de error es"""
	hora = datetime.datetime.now()
	hora = str(hora)[:-10]
	 
	if error == 0:
		texto = '''[{}] {}: Wiktionario la clasificó como "{}" y pattern como "{}". 
		El usuario la clasificó como "{}" y definió: "{}".\n'''
		texto = texto.format(hora, res['palabra'], res['clasificacion_wiktionario'], res['clasificacion_pattern'], clas, defi)
	
	if error == 1:
		texto = '[{}] {}: Wiktionario la clasificó como "{}" y pattern como "{}".\n'
		texto = texto.format(hora,res['palabra'],res['clasificacion_wiktionario'],res['clasificacion_pattern'])
	
	elif error ==2:
		texto = '[{}] El termino "{}": no se encontró en ningun motor de busqueda.\n'.format(hora,res['palabra'])

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
	resultado = buscar_en_wiktionary(palabra)
	# resultado tiene los campos:
	# 'palabra' [str] la que busqué
	# 'clasificacion_pattern' [str] si se encontro en wiktionario
	# 'clasificacion_wiktionario' [str] si se encontro en pattern
	# 'definicion' [str] si se encontro en wiktionario
	# los campos que no se pudieron recuperar tendran None
	clasificacion_definitiva = resultado['clasificacion_pattern']
	definicion = resultado['definicion']
	
	if ( (resultado['clasificacion_wiktionario'] != resultado['clasificacion_pattern'] 
		  and resultado['clasificacion_wiktionario'] != 'MIXTA')
		 or resultado['definicion'] == ''):
		
		clasificacion_definitiva = resultado['clasificacion_wiktionario']

		if (resultado['clasificacion_wiktionario'] == '_Ninguna_'		## no la encontró
			or resultado['clasificacion_wiktionario'] == '_no_sabe_'	## existe, pero filtra mal las categorías por ej "ES:Sustantivos"
			or resultado['definicion'] == ''):								## existe, pero parseó mal la definicion por no encontrar los <dt>1</dt>
			# y como son distintas se supone que pattern dio distinto de _Ninguna_
			clasificacion_definitiva = resultado['clasificacion_pattern']
			
			ingreso = [	[sg.T('Falló la búsqueda de "'+palabra+'" en Wiktionario.\nDefínala:\n')],
						[sg.Radio('Sustantivo', "RADIOp",default = True,key='_esSus_'), 
							sg.Radio('Adjetivo', "RADIOp",key='_esAdj_'),
							sg.Radio('Verbo', "RADIOp",key='_esVer_')],
						[sg.Input(default_text = resultado['definicion'], key = 'def')],
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
			## Reporto error con la info que proporcionó el usuario
			reporte(resultado, 0,clasificacion_definitiva,definicion)
		
		else: ## Reporto que las claificaciones difieren pero sin ingreso por parte del usuario
			print('Reportando Error 1...') 
			reporte(resultado, 1,'','')
		
	elif resultado['clasificacion_pattern'] == '_Ninguna_': # Las dos None ya que no son distintas
		print('Reportando Error 2...')
		reporte(resultado,2,'','')
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
		palabras_dicc = config_dicc['palabras']
		
		palabras_clas = config_dicc['palabras_clas']
		
	else:
		config_dicc = {}
		config_dicc['palabras'] = {}
		config_dicc['palabras_clas'] = {'sust':[],'verb':[],'adj':[]}
		config_dicc['orientacion'] = None
		palabras_dicc = {}
		palabras_clas = {'sust':[],'verb':[],'adj':[]}
		config_dicc['max_sust'] = 0
		config_dicc['max_verb'] = 0
		config_dicc['max_adj'] = 0
		config_dicc['color_pincel'] = { 'sust': '#69cfd8',
		 								'verb': '#5ce4a0',
										'adj':  '#e0619a'}
		config_dicc['oficina'] = '8'
		print('No existe archivo de configuración')
	#print('Cargo en cargar_configuracion()',config_dicc['orientacion'])
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
	
def cargar_json_registro(of):
	existe = os.path.isfile(nombre_archivo_registro)
	if not existe:
		print('No existe archivo de registro, se usara uno de prueba')
		crear_registro(16,5)
	
	with open(nombre_archivo_registro, 'r', encoding = 'utf-8') as f:
		reg_dicc = json.load(f)
	
	try:
		temp = reg_dicc[of][-1:][0]['temp'] #accede al ultimo registro de esa oficina
		print(temp)
	except KeyError:
		print('No existe dato de esa oficina, se inventará')
		return 34
	
	return int(temp)

def colores(config_dicc):
	'''Setea parametros de Pysimplegui sobre todo colores de los elementos de las ventanas. 
	Devuelve una tupla con un color de texto y fondo para usar luego en botones'''
	sg.ChangeLookAndFeel('Reddit')
	
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
	temas_clima={	"Frio":['GreenTan','LightGreen','DarkBlue','BluePurple','BlueMono','BrownBlue','TealMono'],
					"Neutro":['Reddit','Tan','TanBlue','Purple','GreenMono','NeutralBlue'],
					"Calido":['DarkAmber','Reds','Green','BrightColors','Kayak','SandyBeach'],
					"Oscuro":['Topanga','Dark','Dark2','Black','DarkTanBlue']
				}
	
	temp = cargar_json_registro(config_dicc['oficina'])
	hora = int(time.strftime("%H", time.localtime(time.time())))
	if temp < 15 :
		tema = random.choice(temas_clima['Frio'])
		if hora > 18:
			tema = random.choice(temas_clima['Oscuro'])
	elif temp < 25:
		tema = random.choice(temas_clima['Neutro'])
		if hora > 20:
			tema = random.choice(temas_clima['Oscuro'])
	else:
		tema = random.choice(temas_clima['Calido'])
		if hora > 21:
			tema = random.choice(temas_clima['Oscuro'])
	
	sg.ChangeLookAndFeel(tema)
	
	return ('#262730','#EFF0D1') #·negro y crema
	
def son_colores_parecidos(color1,color2):
	'''Usa la librería colormath para determinar si un par de colores es parecido y devuelve verdadero en ese caso'''
	from colormath.color_objects import AdobeRGBColor, LabColor, XYZColor
	from colormath.color_conversions import convert_color
	from colormath.color_diff import delta_e_cie1976

	try:
		color1 = AdobeRGBColor.new_from_rgb_hex(color1)
		color2 = AdobeRGBColor.new_from_rgb_hex(color2)
		delta_e = delta_e_cie1976(convert_color(color1,LabColor), convert_color(color2,LabColor))
		print(delta_e)
		#print(abs(delta_e)<50)
		return abs(delta_e)<50

	except ValueError:
		print('Elige un color')
		return False

def configuracion():
	# crea lista auxiliar de colores para los combo de seleccion de color de pincel.
	lista_Combo_colores = list(listaColores.keys())
	"""recibe de cargar_configuracion() la configuracion elegida por el usuario para la sopa de letras"""
	
	config_dicc, palabras_dicc, palabras_clas = cargar_configuracion()
	
	color_fondo = colores(config_dicc)
	color_sel = ('#EFF0D1', '#D33F49')
	orientacion = 'dirs_0' #por defecto
	
	palabras_lista = list(palabras_dicc.keys()) ## lista para el listbox
	
	TOTAL_PALABRAS_A_USAR = config_dicc['max_sust']+config_dicc['max_verb']+config_dicc['max_adj']
	
	print('Cargo en configuracion()',config_dicc['orientacion'])

	menu = ['Menu', [' ',
					 'Definicion::_MENU_',
					 'Editar',
					 ' ',
					 '---',
					 'Eliminar::_MENU_'
					]
			]
			
	agregar_palabra_layout = [	[sg.Input(key = '_IN_', do_not_clear = False, focus = True, background_color = '#DB91D6')],
			[sg.Button('Agregar', bind_return_key = True, key = '_ADD_')],
			[sg.Listbox(values = palabras_lista, enable_events = True, size = (15,6),
						key = '_LISTA_', tooltip = 'Click para seleccionar', right_click_menu = menu),
			 sg.Multiline('',size=(None, None), pad = None, font = None, right_click_menu=None,
						auto_size_text=None, key = '_OUT_',do_not_clear = True)
			 ]]

	
	cantidad_palabras_layout = [
		[sg.Column(	[	[sg.Text(k[0], pad=((0,),2) )],
						[sg.Combo( list( range( 0, 1 + min( MAX, len(config_dicc['palabras_clas'][k[1]]) ))),
				 			key = k[2], default_value = config_dicc['max_'+k[1]], size = (2,1), pad=((20,),1), enable_events = True)]
			 		], pad=((0,),2) )
					for k in (('Sustantivos','sust','_CANT_S_'),('Verbos','verb','_CANT_V_'),('Adjetivo','adj','_CANT_A_'))
		]
	]
	cantidad_palabras_layout[0].append(sg.Frame(title = 'Total:',
	 											layout = [	[sg.Text(TOTAL_PALABRAS_A_USAR, key='_TOTAL_')]
	 		 				 					], pad=((20,0),2) )	)

	## frame de seleccion de color de pincel.
	 
	colores_layout = [	[sg.Column(	[	
							[sg.Text(k[0]+':', pad=((0,),2) )],
							[sg.Combo(lista_Combo_colores, key = '_combo_'+k[1], default_value = k[2], enable_events = True)],
							
							[sg.In(default_text='', key = 'color_'+k[1], size = (7, 1), enable_events = True, visible = False)], # este in tiene que ir si o si para que ande el evento del color chooser, como pasa con el FileBrowse
							[sg.ColorChooserButton('', button_color=('red',config_dicc['color_pincel'][k[1]]), 
														target='color_'+k[1], size=(4,1), border_width=2,
														key='boton_color_'+k[1])]
							]) for k in (('Sustantivos','sust','amarillo'),('Verbos','verb','rojo'),('Adjetivo','adj','verde'))
						],
						[sg.Text('', size = (50,1), font=('default', 10, 'bold'), text_color='#D33F49', 
									 pad=((10,0),(5,10)), key = '_error_color_')]
					 ]
			
	layout_ayudas = [	[sg.Radio('Sin ayuda', "RADIOA", key= 'sin', size=(10,1)),
				 sg.Radio('Definiciones', "RADIOA", key='defin'),
				 sg.Radio('Mostrar palabras', "RADIOA", default = True, key='pal')]]
				  
	layout_orientacion = [	[sg.Button('', image_filename='dirs_'+str(i)+'.png', image_size=(60, 60), image_subsample=6, border_width=0,
							key='dirs_'+str(i), button_color=color_sel if config_dicc['orientacion']=='dirs_'+str(i) else color_fondo)
				 for i in (0,1,2,3,4,8)]]
				 
	layout_mayuscula = [	[sg.Radio('Mayúscula', "RADIOn", key='mayus', default = True, size=(10,1)),
				 sg.Radio('Minúscula', "RADIOn", key='minus')]]
				 
	layout_fuente = [	[sg.Combo(	('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'),
						default_value='Comic',
						key='_FONT_')]]
						
	layout_oficina = [	[sg.Input(default_text=config_dicc['oficina'], size=(3,1), key = '_OF_', do_not_clear = True, background_color = '#DB91D6'),
						 sg.Text('Temp = '+str(cargar_json_registro(config_dicc['oficina']))+'ºC')
						 ]
					 ]
			
	layout= [
		[sg.Text('Ingrese palabras la lista para ser usadas por la sopa de letras:')],
		[sg.Text('Instrucciones de configuración')],
		[sg.Frame('Ingrese palabras',agregar_palabra_layout)],
		[sg.Frame('Cantidad máxima de cada tipo a utilizar en la Sopa:',cantidad_palabras_layout)], 
		[sg.Frame('Seleccion de colores: ',colores_layout)],
		[sg.Frame('Ayudas',layout_ayudas)],
		[sg.Frame('Orientacion',layout_orientacion)],
		[sg.Frame('Mayúscula/Minúscula',layout_mayuscula),sg.Frame('Fuente',layout_fuente)],
		[sg.Frame('Oficina',layout_oficina),sg.Button('Guardar configuración', key='_ACEPTAR_', pad = ((150,5),1), disabled = False),sg.Button('Cerrar' , key= '_CERRAR_',disabled = False)]
		] 

	window = sg.Window('CONFIGURACIÓN').Layout(layout)
	window.Finalize()

	for x in ('V','A'):
		window.FindElement('_CANT_'+x+'_').Update(disabled = True)
	col = {}
	for x in ('sust','verb','adj'):
		window.FindElement('color_'+x).Update(value = config_dicc['color_pincel'][x])
		col['color_'+x] = config_dicc['color_pincel'][x]
	 
	while True:                 # Event Loop  
		event, val = window.Read()  
		if event is None or event == '_CERRAR_': 
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
					
					# devolvera '_no_aceptada_'' si no la encuentra en ningun lado o '_cancelada_' si la encuentra pero el usuario
					# cancela a la hora de agregar la definicion. Tambien puede no saber clasificarla por no encontrar 
					# "ES:Sustantivo", etc, en las categorías, entonces devolverá '_no_sabe_' como categoría
					if definicion == '_no_aceptada_': 
						window.SetAlpha(0.5)
						sg.Popup('No consideramos que "'+palabra+'" sea una palabra', keep_on_top=True)
						window.Reappear() 
					
					elif definicion != '_cancelada_' and categoria != '_no_sabe_' : # la agrego en las estructuras
						palabras_dicc[palabra] = {'tipo': categoria,'def': definicion}
						palabras_clas[categoria].append(palabra) # ojo inicializar siempre antes los diccionarios
						
						palabras_lista = window.FindElement('_LISTA_').GetListValues()
						palabras_lista.append(palabra)  # aca cargo y agrego a la lista, pordría agregar directamente porque ya definí la lista en la importacion.
						window.FindElement('_LISTA_').Update(values = palabras_lista)
		
		if event == '_LISTA_':
			try: 
				window.Element('_OUT_').Update(disabled = False)
				texto = '--> "' + val['_LISTA_'][0] + '":\n'
				texto += 'Clasificación : ' + palabras_dicc[ val['_LISTA_'][0] ]['tipo']+'.\n'
				texto += '\n  ' + palabras_dicc[ val['_LISTA_'][0] ]['def']
				window.Element('_OUT_').Update(value = texto)
				window.Element('_OUT_').Update(disabled = True)
			except(KeyError):
				print(val['_LISTA_'][0])
			except(IndexError):
				print(val['_LISTA_'])
				
		if event == 'Definicion::_MENU_':
			try: 
				texto = '--> "' + val['_LISTA_'][0] + '":\n'
				texto += 'Clasificación : ' + palabras_dicc[ val['_LISTA_'][0] ]['tipo']+'.\n'
				texto += '\n  ' + palabras_dicc[ val['_LISTA_'][0] ]['def']
			
				window.SetAlpha(0.5)
				sg.Popup(texto, keep_on_top=True)
				window.Reappear() ##igual que poner el alpha en 1
			except(KeyError):
				print(val['_LISTA_'][0])
			except(IndexError):
				print(val['_LISTA_'])
			
		if event == 'Eliminar::_MENU_':
			if val['_LISTA_'] != []: 
				palabra = val['_LISTA_'][0]# El Listbox guarda en val una lista con un unico elemento que es el que esta seleccionado en ese momento.
				#elimino de ambdas estructuras:
				palabras_clas[palabras_dicc[palabra]['tipo']].remove(palabra)
				del palabras_dicc[palabra]
				
				palabras_lista = window.FindElement('_LISTA_').GetListValues()
				palabras_lista.remove(palabra)
				window.FindElement('_LISTA_').Update(values = palabras_lista)
				print('Se eliminó',palabra)
		
		if event in ('dirs_0','dirs_1','dirs_2','dirs_3','dirs_4','dirs_8'):

			window.Element(event).Update( button_color = color_sel ) # pinto este boton como seleccionado
			lista_dirs = ['dirs_0','dirs_1','dirs_2','dirs_3','dirs_4','dirs_8']
			lista_dirs.remove(event)
			for x in lista_dirs:  # pinto todos menos el actual del color del fondo
				window.Element(x).Update(button_color = color_fondo)
			
			orientacion = event
		##configuracion de colores de pinceles
		#if hay colores repetidos para distintos tipos de palabras deshabilita la opcion de guardar.
		# chekea en cada vuelta que sean distintas. cuando son todas distintas vuelve a habilitar la opcion de guardar.
		if event in ['comboSust','comboAdj','comboVerb']:	
			if val['comboVerb'] == val['comboAdj'] or val['comboVerb'] == val['comboSust']or val['comboSust'] == val['comboAdj']:
				sg.Popup('No se pueden elejir colores repetidos para distintos tipos de palabaras')
				window.FindElement('_ACEPTAR_').Update(disabled = True)
				window.FindElement('_CERRAR_').Update(disabled = True)
			if val['comboSust'] != val['comboVerb'] and val['comboVerb'] != val['comboAdj'] and val['comboAdj'] != val['comboSust'] :
					window.FindElement('_ACEPTAR_').Update(disabled = False)
					window.FindElement('_CERRAR_').Update(disabled = False)
		
		evento_colores = ['color_'+j for j in ('sust','verb','adj')]
		if event in evento_colores:
			window.FindElement('boton_'+event).Update(button_color = (color_fondo[0],val[event]))
			print('Colores elegidos:',val['color_sust'],val['color_verb'],val['color_adj'])

			if val[event]=="None":
				
				col[event] = config_dicc['color_pincel'][event[6:]]
			else:
				col[event] = val[event]
				error_color = False
				
				if son_colores_parecidos(val['color_sust'],col['color_verb']):
					error_color += True
					window.Element('_error_color_').Update(value='¡Error! Color de sustantivo y verbo muy parecido')
				
				if son_colores_parecidos(col['color_sust'],col['color_adj']):
					error_color += True
					window.Element('_error_color_').Update(value='¡Error! Color de sustantivo y adjetivo muy parecido')
				
				if son_colores_parecidos(col['color_verb'],col['color_adj']):
					error_color += True
					window.Element('_error_color_').Update(value='¡Error! Color de verbo y adjetivo muy parecido')
				
				if error_color:
					window.Element('_error_color_').Update(visible= True)
					window.FindElement('_ACEPTAR_').Update(disabled = True)
				
				else:
					window.Element('_error_color_').Update(value='')
					window.Element('_error_color_').Update(visible= False)
					window.FindElement('_ACEPTAR_').Update(disabled = False)


		lista_cant = ['_CANT_S_','_CANT_V_','_CANT_A_']
		if event in lista_cant:
			if event == '_CANT_S_':  # voy seteando el tope del siguiente segun MAX - actual, lo habilito y lo seteo en cero.
				window.Element('_CANT_V_').Update(values = list( range( 0, 1 + MAX - int(val[event]) ) ) , disabled = False, set_to_index = 0 )
			if event == '_CANT_V_':
				window.Element('_CANT_A_').Update(values = list( range( 0, 1 + MAX - int(val[event]) - int(val['_CANT_S_']) ) ) , disabled = False, set_to_index = 0 )
			TOTAL_PALABRAS_A_USAR = int(val['_CANT_S_']) + int(val['_CANT_V_']) + int(val['_CANT_A_'])
			window.Element('_TOTAL_').Update(value = TOTAL_PALABRAS_A_USAR )
				
		##LLeno diccionario
		try:
			config_dicc['palabras'] = palabras_dicc
			config_dicc['palabras_clas'] = palabras_clas
			config_dicc['ayuda'] = "sin ayuda" if val['sin'] else "definiciones" if val['defin'] else "palabras" 
			config_dicc['orientacion'] = orientacion
			config_dicc['mayuscula'] = val['mayus']
			config_dicc['fuente'] = val['_FONT_']
			config_dicc['max_sust'] = int(val['_CANT_S_'])
			config_dicc['max_verb'] = int(val['_CANT_V_'])
			config_dicc['max_adj'] = int(val['_CANT_A_'])
			config_dicc['oficina'] = val['_OF_']
			#config_dicc['color_pincel'] = {'sust': listaColores[val['comboSust']],
			# 								'verb': listaColores[val['comboVerb']],
			# 								'adj':  listaColores[val['comboAdj']]}
			
			config_dicc['color_pincel'] = {x : val['color_'+x] for x in ('sust','verb','adj')}

			#print('VALORES')
			#print(config_dicc)	 
		except ValueError:
			window.SetAlpha(0.5)
			sg.Popup('Debe seleccionar cantidades!!', keep_on_top=True)
			window.Reappear()
			
			
		if event == '_ACEPTAR_':
			if TOTAL_PALABRAS_A_USAR == 0:
				window.SetAlpha(0.5)
				sg.PopupError('La cantidad de palabras\n no puede ser cero.', keep_on_top=True)
				window.Reappear()
			if val['_OF_'] == None or val['_OF_'] == '':
				window.SetAlpha(0.5)
				sg.PopupError('Debe ingresar el \n numero de oficina.', keep_on_top=True)
				window.Reappear()
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



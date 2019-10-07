# -*- coding: utf-8 -*-
import PySimpleGUI as sg
import random
import string
import json
import os
import time
import datetime
import tkinter
from tkinter.colorchooser import askcolor
from pprint import pprint
from collections import defaultdict
from buscar_en_wiktionary import buscar_en_wiktionary
from creador_registro_test import crear_registro

CREDITS = '''
Sopa de Letras
v alpha.0.1

Trabajo Final para Seminario Opción Python
	Facultad de Informática
		UNLP

Alumnos:

	Matías Agustin Cabral
	Bruno Sbrancia
	Juan Pablo Sanchez Magariños
'''
HOWTO = '''
Instrucciones para la configuración:
	Ingrese palabras para ser usadas en la sopa de letras, en caso que  no se encuentre
	 la misma en ciertas bases de datos, se le pedirá una definición.
	Puede eliminar palabras de la lista haciendo primero click y luego click derecho.
	Debe elegir la cantidad de palabras de cada tipo que quiere que se usen. El sistema
	 elegirá palabras al azar de entre las que se encuentren en la lista, respetando 
	 las cantidades indicadas.
	Puede cambiar los colores con los que el alumno marcará las palabras en la Sopa de
	 Letras.
	Para agregar dificultad puede elegir el tipo de Ayudas:
		- Sin ayuda, solo indicara la cantidad de palabras que debe el alumno buscar.
		- Definiciones, mostrará una lista con definiciones de las palabras que se
		 encuentran en la Sopa.
		- Mostrar palabras, muestra la lista directamente de todas las palabras que hay
		 en la misma.
	La Orientación indica las distintas formas de disponer las palabras como indican
	 las flechas. Poniendo el mouse sobre las mismas le dará una breve descripción al
	 respecto.
	Por último puede elegir la fuente y la capitalización de las letras.
	El campo oficina podrá elegirlo si se dispone de un archivo con las temperaturas de
	 las aulas tomado por una raspberry Pi. A partir del mismo se designarán los colores
	 de las ventanas.
'''

nombre_archivo_config = 'configuracion.json'
nombre_archivo_reporte = 'reporte_de_errores.txt'
nombre_archivo_registro = 'registros_temp_hum.json'
## con MAX seteamos el numero máximo de palabras a usar en total entre sust verb y adj.
MAX = 10
def reporte( res, error, clas, defi ):
	"""pone en archivo de texto un reporte de los errores encontrados en la ejecución de la sopa de letras"""
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
		texto = '[{}] El termino "{}": no se encontró en ningún motor de busqueda.\n'.format(hora,res['palabra'])

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
			window2 = sg.Window('Definición ').Layout(ingreso)
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
	
def cargar_json_registro():
	'''Carga los datos de temperatura y humedad de las oficinas en un diccionario que retorna'''
	existe = os.path.isfile(nombre_archivo_registro)
	if not existe:
		print('No existe archivo de registro, se usara uno de prueba')
		crear_registro(16,5) # crea un archivo en la ruta ante especificada, de 16 oficinas con 5 registros cada una.
	
	with open(nombre_archivo_registro, 'r', encoding = 'utf-8') as f:
		reg_dicc = json.load(f)
	
	return reg_dicc
	
def temperatura_reciente(of):
	'''Devuelve el dato de temperatura del último elemento de la lista de registros de la oficina especificada.'''
	reg_dicc = cargar_json_registro()
	
	try:
		temp = reg_dicc[of][-1:][0]['temp'] # accede al ultimo registro de esa oficina

	except KeyError:
		print('No existe dato de esa oficina, se inventará')
		return random.randint(-10,50)
	
	return int(temp)
	
def cargar_configuracion():
	"""Abre archivo json con la configuración cargada anteriormente.
	si no existe el mismo, inicializa las estructuras vacías para poder cargarlas en el futuro.

	Retorna: (config_dicc, palabras_dicc, palabras_clas)
	
	"""
	existe = os.path.isfile(nombre_archivo_config)
	if existe:
		print('Configuración cargada desde',os.path.abspath(nombre_archivo_config))
		with open(nombre_archivo_config, 'r', encoding = 'utf-8') as f:
			config_dicc = json.load(f)
		palabras_dicc = config_dicc['palabras']
		
		palabras_clas = config_dicc['palabras_clas']
		
	else:
		print('No existe archivo de configuración, se creará uno por defecto.')
		config_dicc = {}
		config_dicc['palabras'] = {}
		config_dicc['palabras_clas'] = {'sust':[],'verb':[],'adj':[]}
		config_dicc['orientacion'] = 'dirs_0'
		palabras_dicc = {}
		palabras_clas = {'sust':[],'verb':[],'adj':[]}
		config_dicc['fuente'] = 'Fixedsys'
		config_dicc['max_sust'] = 0
		config_dicc['max_verb'] = 0
		config_dicc['max_adj'] = 0
		config_dicc['color_pincel'] = { 'sust': '#69cfd8',
		 								'verb': '#5ce4a0',
										'adj':  '#e0619a'}
		config_dicc['oficina'] = random.choice(list(cargar_json_registro().keys()))
	return config_dicc,palabras_dicc,palabras_clas
	
def obtener_lista_palabras(config_dicc):
	'''Este método es para elegir aleatoriamente palabras, respetando las cantidades 
	máximas definidas para cada tipo.'''

	lista_s = config_dicc['palabras_clas']['sust']
	lista_v = config_dicc['palabras_clas']['verb']
	lista_a = config_dicc['palabras_clas']['adj']
	
	cant = min ( len(lista_s), config_dicc['max_sust'] ) # también puedo comprobarlo antes y que max nunca tenga algo mayor que el largo de la lista
	palabras_rand = random.sample(lista_s, cant)
	
	cant = min ( len(lista_v), config_dicc['max_verb'] )
	palabras_rand.extend(random.sample(lista_v, cant))
	
	cant = min ( len(lista_a), config_dicc['max_adj'] )
	palabras_rand.extend(random.sample(lista_a, cant))
	
	return palabras_rand

def colores(config_dicc):
	'''Setea parametros de Pysimplegui sobre todo colores de los elementos de las ventanas. 
	Devuelve una tupla con un color de texto y fondo para usar luego en botones'''
	sg.ChangeLookAndFeel('Reddit')
	
	sg.SetOptions(
	icon = 'img/bee.ico',
	text_color='black',
	input_text_color='black',
	background_color='#EFF0D1', #cremita
	)
	BLUES = ("#082567", "#0A37A3", "#00345B")
	PURPLES = ("#480656", "#4F2398", "#380474")
	GREENS = ("#01826B", "#40A860", "#96D2AB", "#00A949", "#003532")
	YELLOWS = ("#F3FB62", "#F0F595")
	TANS = ("#FFF9D5", "#F4EFCF", "#DDD8BA")
	NICE_BUTTON_COLORS = ((GREENS[3], TANS[0]),
						('#000000', '#FFFFFF'),
						('#FFFFFF', '#000000'),
						(YELLOWS[0], PURPLES[1]),
						(YELLOWS[0], GREENS[3]),
						(YELLOWS[0], BLUES[2]))
	DEFAULT_PROGRESS_BAR_COLOR= (GREENS[0], '#D0D0D0')
	temas = {'Calido':	{'BACKGROUND': '#a7ad7f','TEXT': 'black','INPUT': '#e6d3a8','SCROLL': '#e6d3a8','TEXT_INPUT': 'black','BUTTON': ('white', '#5d907d')},
			'Frio':		{'BACKGROUND': '#A5CADD','TEXT': '#6E266E','INPUT': '#E0F5FF','SCROLL': '#E0F5FF','TEXT_INPUT': 'black','BUTTON': ('white', '#303952')},
			'Neutro':	{'BACKGROUND': '#92aa9d','TEXT': 'black', 'INPUT': '#fcfff6', 'SCROLL': '#fcfff6', 'TEXT_INPUT': 'black', 'BUTTON': ('black', '#d0dbbd')},
			'Oscuro':	{'BACKGROUND': 'gray25','TEXT': 'white','INPUT': 'gray30','SCROLL': 'gray44','TEXT_INPUT': 'white','BUTTON': ('white', '#004F00')}
			}
	temas_clima={	"Frio":['GreenTan','LightGreen','DarkBlue','BluePurple','BlueMono','BrownBlue','TealMono'],
					"Neutro":['Reddit','Tan','TanBlue','Purple','GreenMono','NeutralBlue'],
					"Calido":['DarkAmber','Reds','Green','BrightColors','Kayak','SandyBeach'],
					"Oscuro":['Topanga','Dark','Dark2','Black','DarkTanBlue']}
	
	temp = temperatura_reciente(config_dicc['oficina'])
	hora = int(time.strftime("%H", time.localtime(time.time())))
	if temp < 15 :
		tema = 'Frio'
		if hora > 18:
			tema = 'Oscuro'
	elif temp < 25:
		tema = 'Neutro'
		if hora > 20:
			tema = 'Oscuro'
	else:
		tema = 'Calido'
		if hora > 21:
			tema = 'Oscuro'
	sg.SetOptions(background_color=temas[tema]['BACKGROUND'],
				text_element_background_color=temas[tema]['BACKGROUND'],
				element_background_color=temas[tema]['BACKGROUND'],
				text_color=temas[tema]['TEXT'],
				input_elements_background_color=temas[tema]['INPUT'],
				button_color=temas[tema]['BUTTON'],
				progress_meter_color=DEFAULT_PROGRESS_BAR_COLOR,
				border_width=1,
				slider_border_width=0,
				progress_meter_border_depth=0,
				scrollbar_color=(temas[tema]['SCROLL']),
				input_text_color=temas[tema]['TEXT_INPUT'],
				element_text_color=temas[tema]['TEXT'])

	colores_celdas = {	None:	('#EFF0D1','#854e0b'), #blanco y marron
					'adj':	('#262730',config_dicc['color_pincel']['adj']),
					'verb':	('#262730',config_dicc['color_pincel']['verb']),
					'sust':	('#262730',config_dicc['color_pincel']['sust']),
					'marcada': ('#EFF0D1',temas[tema]['INPUT']),
					'Erroneas':('#262730','#f4f4f4'),
					'MIXTO':('#262730','#3e8271'),
					'default':temas[tema]['BUTTON'], #negro y celeste
					'fondo':('#262730',temas[tema]['BACKGROUND']), #·negro y crema
					'splash':('#262730','#EFF0D1')}
	return colores_celdas
	
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

def disable(window):
	window.TKroot.attributes('-disabled', 1)
	window.SetAlpha(0.75)

def enable(window):
	window.Reappear() ##igual que poner el alpha en 1
	window.BringToFront()
	window.TKroot.attributes('-disabled', 0)

def main():
	
	config_dicc, palabras_dicc, palabras_clas = cargar_configuracion()
	
	colores_celdas = colores(config_dicc)
	
	orientacion = config_dicc['orientacion'] #por defecto
	
	palabras_lista = list(palabras_dicc.keys()) ## lista para el listbox
	
	TOTAL_PALABRAS_A_USAR = config_dicc['max_sust']+config_dicc['max_verb']+config_dicc['max_adj']

	menu = ['Menu', [' ',
					 'Definicion::_MENU_',
					 'Editar',
					 ' ',
					 '---',
					 'Eliminar::_MENU_'
					]
			]
			
	agregar_palabra_layout = [	[	sg.Input(key = '_IN_', do_not_clear = False, focus = True, background_color = '#DB91D6'),
									sg.Button('Agregar', bind_return_key = True, key = '_ADD_')],
								[	sg.Listbox(values = palabras_lista, enable_events = True, size = (15,6),
												key = '_LISTA_', tooltip = 'Click para seleccionar', right_click_menu = menu),
			 						sg.Multiline('',size=(40, 6), pad = None, font = None, right_click_menu=None,
													auto_size_text=True, key = '_OUT_',do_not_clear = True)]
							]
	
	cantidad_palabras_layout = [
		[sg.Column(	[	[sg.Text(k[0], pad=((0,),2) )],
						[sg.Combo( list( range( 0, 1 + min( MAX, len(config_dicc['palabras_clas'][k[1]]) ))),
				 			key = k[2], default_value = config_dicc['max_'+k[1]], size = (2,1), pad=((20,),1), enable_events = True)]
			 		], pad=((0,),2) )
					for k in (('Sustantivos','sust','_CANT_S_'),('Verbos','verb','_CANT_V_'),('Adjetivos','adj','_CANT_A_'))
		]
	]
	cantidad_palabras_layout[0].append(sg.Frame(title = 'Total:',
	 											layout = [	[sg.Text(TOTAL_PALABRAS_A_USAR, key='_TOTAL_')]
	 		 				 					], pad=((20,0),2) )	)

	## frame de seleccion de color de pincel.
	 
	colores_layout = [	[sg.Column(	[	
							[sg.Text(k[0]+':', pad=((0,),2) )],

							[sg.Button('', button_color=('red',config_dicc['color_pincel'][k[1]]), 
														size=(6,3), border_width=5, pad=((25,25),(5,0)),
														key='color_'+k[1])]
							]) for k in (('Sustantivos','sust','amarillo'),('Verbos','verb','rojo'),('Adjetivos','adj','verde'))
						],
						[sg.Text('', size=(52,1), font=('default', 10, 'bold'), text_color='#D33F49', 
									 pad=((10,0),(5,10)), key = '_error_color_')]
					 ]
			
	layout_ayudas = [	[sg.Radio('Sin ayuda', "RADIOA", key= 'sin', size=(10,1)),
				 sg.Radio('Definiciones', "RADIOA", key='defin'),
				 sg.Radio('Mostrar palabras', "RADIOA", default = True, key='pal')]]
				  
	layout_orientacion = [	[sg.Button	('',	image_filename = 'img/dirs_'+str(i[0])+'.png', image_size = (60, 60), image_subsample = 6,
												border_width=0, tooltip=i[1], key='dirs_'+str(i[0]), 
												button_color=colores_celdas['marcada'] if config_dicc['orientacion']=='dirs_'+str(i) else colores_celdas['fondo']
										) for i in (	(0,'Sólo horizontal de izquierda a derecha'),
				 										(1,'Sólo vertical de arriba hacia abajo'),
														(2,'Horizontal de izquierda a derecha y vertical de arriba hacia abajo'),
														(3,'Horizontal de izquierda a derecha, vertical de arriba hacia abajo y diagonal hacia abajo y derecha'),
														(4,'Horizontal y vertical en ambos sentidos cada uno'),
														(8,'Horizontal, vertical y diagonal en ambos sentidos')
													)
								]
							]
				 
	layout_mayuscula = [	[sg.Radio('Mayúscula', "RADIOn", key='mayus', default = True, size=(10,1)),
				 sg.Radio('Minúscula', "RADIOn", key='minus')]]
				 
	layout_fuente = [	[sg.Combo(	('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'),
						default_value = config_dicc['fuente'],
						key = '_FONT_')]]
						
	layout_oficina = [	[
						# La oficina la podemos agregar a mano o con un combo
						#sg.Input(default_text=config_dicc['oficina'], size=(3,1), do_not_clear = True, background_color = '#DB91D6', key = '_OF_'),
						 sg.Combo(values = list(cargar_json_registro().keys()), default_value = config_dicc['oficina'], enable_events = True, key = '_OF_'),
						 sg.Text('Temp = '+str(temperatura_reciente(config_dicc['oficina']))+'ºC', key='_TEMP_')
						 ]
					 ]
	
	menu_princ = [	['&Archivo',	['&Cargar...::Menu', 
									'&Guardar...::Menu', 
									'---',
									'E&xit::Menu']],
					['&Ayuda',		['Instrucciones::Menu',
									'Acerca de...::Menu']]
				]
	
	# Para sacar la resolucion de pantalla hay que crear una ventana, se cierra rapido asi que practicamente no se ve.
	window0 = sg.Window('dummy',alpha_channel=0).Layout([[sg.Text('prueba')]])
	window0.ReadNonBlocking() #para que no se quee esperando interaccion
	x_max,y_max = window0.GetScreenDimensions()
	window0.Close()
	print('Resolución:',x_max,'x',y_max)
	
	# Control de layout según alto de pantalla
	if y_max > 800:
		layout_principal = [
			[sg.Menu(menu_princ)],
			[sg.Frame('Ingrese palabras: ',agregar_palabra_layout)],
			[sg.Frame('Cantidad máxima de cada tipo de palabra:',cantidad_palabras_layout)], 
			[sg.Frame('Selección de colores: ',colores_layout)],
			[sg.Frame('Ayudas',layout_ayudas)],
			[sg.Frame('Orientación',layout_orientacion)],
			[sg.Frame('Mayúscula/Minúscula',layout_mayuscula),sg.Frame('Fuente',layout_fuente), sg.Frame('Oficina',layout_oficina)],
			[sg.Button('Guardar configuración', key='_ACEPTAR_', pad = ((350,5),(10,5)), disabled = False),
			 sg.Button('Cerrar' , key= '_CERRAR_', pad = ((5,5),(10,5)), disabled = False)] 
		]
	else:
		layout_principal = [
			[sg.Menu(menu_princ)],
			[sg.Frame('Ingrese palabras: ',agregar_palabra_layout), sg.Frame('Selección de colores: ',colores_layout)],
			[sg.Frame('Cantidad máxima de cada tipo de palabra:',cantidad_palabras_layout),sg.Frame('Orientacion',layout_orientacion)], 
			[sg.Frame('Ayudas',layout_ayudas),sg.Frame('Mayúscula/Minúscula',layout_mayuscula),sg.Frame('Fuente',layout_fuente),sg.Frame('Oficina',layout_oficina)],
			[sg.Button('Guardar configuración', key='_ACEPTAR_', pad = ((750,5),(10,5)), disabled = False),
			 sg.Button('Cerrar' , key= '_CERRAR_', pad = ((5,5),(10,5)), disabled = False)] 
		]

	window = sg.Window('CONFIGURACIÓN').Layout(layout_principal)
	window.Finalize()

	for x in ('V','A'):
		window.FindElement('_CANT_'+x+'_').Update(disabled = True)
	
	# Estructura auxiliar para guardar los colores de "pincel"
	col = {}
	for x in ('sust','verb','adj'):
		col['color_'+x] = config_dicc['color_pincel'][x]
	 
	while True:                 # Event Loop  
		event, val = window.Read()  
		if event is None or event == '_CERRAR_' or event =='Exit::Menu':
			break

		if event in ('Instrucciones::Menu','Acerca de...::Menu'):
			disable(window)
			if event == 'Instrucciones::Menu':
				sg.Popup(HOWTO,font = 'System', keep_on_top=True)
			if event == 'Acerca de...::Menu':
				sg.Popup(CREDITS,font = 'System', keep_on_top=True)
			enable(window)
		
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
						disable(window)
						sg.Popup('No consideramos que "'+palabra+'" sea una palabra', keep_on_top=True)
						enable(window)
					
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
			
				disable(window)
				sg.Popup(texto, keep_on_top=True)
				enable(window)

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

			window.Element(event).Update( button_color = colores_celdas['marcada'] ) # pinto este boton como seleccionado
			lista_dirs = ['dirs_0','dirs_1','dirs_2','dirs_3','dirs_4','dirs_8']
			lista_dirs.remove(event)
			for x in lista_dirs:  # pinto todos menos el actual del color del fondo
				window.Element(x).Update(button_color = ( '#000', window.BackgroundColor) )
			
			orientacion = event

		evento_colores = ['color_'+j for j in ('sust','verb','adj')]
		if event in evento_colores:

			disable(window)

			color_elegido = tkinter.colorchooser.askcolor() 
			print('color_elegido =',color_elegido)
			color_elegido = color_elegido[1]
			try:
				window.FindElement(event).Update(button_color = ('red',color_elegido))
				#print('Colores elegidos (val):',val['color_sust'],val['color_verb'],val['color_adj'])

				col[event] = color_elegido
				print('Colores elegidos (col):',col['color_sust'],col['color_verb'],col['color_adj'])
				error_color = False
					
				print('Delta entre color_sust y color_verb:',end=' ')
				if son_colores_parecidos(col['color_sust'],col['color_verb']):
					error_color += True
					window.Element('_error_color_').Update(value='¡Error! Color de sustantivo y verbo muy parecido.')
				print('Delta entre color_sust y color_adj:',end=' ')
				if son_colores_parecidos(col['color_sust'],col['color_adj']):
					error_color += True
					window.Element('_error_color_').Update(value='¡Error! Color de sustantivo y adjetivo muy parecido.')
				print('Delta entre color_verb y color_adj:',end=' ')
				if son_colores_parecidos(col['color_verb'],col['color_adj']):
					error_color += True
					window.Element('_error_color_').Update(value='¡Error! Color de verbo y adjetivo muy parecido.')
				print()
				if error_color:
					window.Element('_error_color_').Update()
					window.Element('_error_color_').Update(visible= True)
					window.FindElement('_ACEPTAR_').Update(disabled = True)
				
				else:
					window.Element('_error_color_').Update(value='')
					window.Element('_error_color_').Update(visible= False)
					window.FindElement('_ACEPTAR_').Update(disabled = False)
			except:
				col[event] = config_dicc['color_pincel'][event[6:]] #Si se cancela la ventana, quedaba (none,none) y daba error, por eso cargo el color que estaba en config.
			
			enable(window)
		
		lista_cant = ['_CANT_S_','_CANT_V_','_CANT_A_']
		if event in lista_cant:
			if event == '_CANT_S_':  # voy seteando el tope del siguiente segun MAX - actual, lo habilito y lo seteo en cero.
				window.Element('_CANT_V_').Update(values = list( range( 0, 1 + MAX - int(val[event]) ) ) , disabled = False, set_to_index = 0 )
			if event == '_CANT_V_':
				window.Element('_CANT_A_').Update(values = list( range( 0, 1 + MAX - int(val[event]) - int(val['_CANT_S_']) ) ) , disabled = False, set_to_index = 0 )
			TOTAL_PALABRAS_A_USAR = int(val['_CANT_S_']) + int(val['_CANT_V_']) + int(val['_CANT_A_'])
			window.Element('_TOTAL_').Update(value = TOTAL_PALABRAS_A_USAR )
		
		if event == '_OF_':
			window.Element('_TEMP_').Update(value = 'Temp = '+str(temperatura_reciente(val['_OF_']))+'ºC')
		
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
			config_dicc['color_pincel'] = {x : col['color_'+x] for x in ('sust','verb','adj')}

			#print('VALORES')
			#print(config_dicc)	 
		except ValueError:
			disable(window)
			sg.Popup('Debe seleccionar cantidades!!', keep_on_top=True)
			enable(window)
				
		if event == '_ACEPTAR_':
			
			if TOTAL_PALABRAS_A_USAR == 0:
				disable(window)
				sg.PopupError('La cantidad de palabras\n no puede ser cero.', keep_on_top=True)
				enable(window)
			else:
				with open(nombre_archivo_config, 'w', encoding = 'utf-8') as f:
					json.dump(config_dicc, f, ensure_ascii = False)
				print('Configuración guardada:\n')
				pprint (config_dicc)
		
		if event == '_LISTA_':
			print ('Seleccionado: ',val['_LISTA_'])
	window.Close()

if __name__ == "__main__":
	main()



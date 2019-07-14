# -*- coding: utf-8 -*-
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
Sopa de Letras:

Primero seleccionar color segun el tipo de
palabra que va a buscar.
Marque los casilleros de la palabras, 
clickeando las letras de la grilla.

Podrá seleccionar el tipo de ayuda en el 
apartado Configuración.

El juego finaliza una vez que todas las 
letras de todas las palabras esten marcadas
con el color correspondiente.

Si una letra pertenece a más de una 
palabra (intersección), podrá marcarla
con cualquier color.
'''
import PySimpleGUI as sg
import random
import math
import time
from playsound import playsound
import sys

from grilla import crear_grilla

import config

def dibujar():
	config_dicc, palabras_dicc, _ = config.cargar_configuracion()
	palabras_lista = config.obtener_lista_palabras(config_dicc)
	fuente = config_dicc['fuente']
	color_fondo = config.colores()
	#Colores marcas
	color_celda_marcada = ('#EFF0D1','#854e0b') #blanco y marron
	color_marca = {None:('#EFF0D1','#854e0b'), #blanco y marron
					'adj':(config_dicc['color_pincel']['ADJ']),
					'verb':(config_dicc['color_pincel']['VERB']),
					'sust':(config_dicc['color_pincel']['SUST']),
					'Erroneas':('#262730','#f4f4f4'),
					'MIXTO':('#262730','#3e8271')}
	color_celda_default = ('#262730','#5adbff') #negro y celeste

	#celda mal marcada('#262730','#f4f4f4')
	
	
	# ~ print('Cargo en dibujar()',config_dicc['orientacion'])
	print('Creo lista de palabras random en dibujar()')
	print('palabras_lista =',palabras_lista)
	
	## Defino el ancho de la grilla como el mayor entre la cantidad de palabras o la palabra mas larga
	ANCHO = max(len(max(palabras_lista, key=len)),len(palabras_lista)) # key = len hace que sea por cantidad de char y no alfabeticamente
	## O solo la palabra más larga
	#ANCHO = len(max(palabras_lista, key=len))
	## Y siquieropuede ser cuadrada
	ALTO = ANCHO
	
	
	## Crear la matriz de elementos y llenarla con las letras
	matriz = crear_grilla(palabras_lista)
	
	
	def ayuda(palabras_lista,palabras_dicc,config_dicc):
		"""depende de lo recibido en la configuracion de ayuda modifica el layout  para que informe lo correspondiente a cada caso"""
		""" ayuda_layout lista creada para agregarlo al frame al layout de la sopa"""
		# cantv, cantadj, cantsust = cantidad_pal(palabras_dicc)
		ayuda_layout=[]
		if config_dicc['ayuda'] == 'sin ayuda':
			column1 = [
				[sg.T('Total de palabras a buscar: ' + str(len(palabras_lista)), justification='center')],
				[sg.T('Sustantivos: '+ 	str(config_dicc['max_sust']))],
				[sg.T('Verbos: '+ 		str(config_dicc['max_verb']))],
				[sg.T('Adjetivos: '+ 	str(config_dicc['max_adj']))]
			]
			ayuda_layout = [
							[sg.Column(column1)]
							]
		# si es definiciones agrega al layout un numero para la palabra y su descripcion.	
		# 'palabra num-'+str(j) : asigna un numero a la palabra para mostrar en layout.
		#  palabras_dicc[palabras_lista[j]]['def'] : accese a la descripcion de la palabra a la que referencia el numero para informar.
		# para referenciado por numero toma la posicion en la lista de palabras.
		elif config_dicc['ayuda'] == 'definiciones':
			column1 = [
				[sg.T ('-'+str(j)+': '+palabras_dicc[palabras_lista[j]]['def'],auto_size_text = True)]for j in range(len(palabras_lista))
				]
			ayuda_layout = [ 
							[sg.T('Definiciones: ')],
							[sg.Column(column1)]
							]
		elif config_dicc['ayuda'] == 'palabras':
			column1 = [                   ## agrego que el color aparezca en modo fácil, buscar el tipo en el dicc de colores, el segundo elemento porque es una tupla (texto, fondo)
				[sg.T(palabras_lista[j], background_color = color_marca[ palabras_dicc[palabras_lista[j]]['tipo']][1]
				)] for j in range(len(palabras_lista))
				]
			ayuda_layout = [
							[sg.T('Palabras a buscar :')],
							[sg.Column(column1)]]
		return ayuda_layout
	
	ayuda_layout = ayuda(palabras_lista,palabras_dicc,config_dicc)
	print('ANCHO:',ANCHO,'Alto:',ALTO)
	menu_princ = [	['&Archivo', ['&Cargar...::Menu', '&Guardar...::Menu', '---', '!Configuracion::Menu', 'E&xit'  ]],    
					['&Ayuda', ['Como jugar?::Menu','Acerca de...::Menu']]
				 ]
	sopa_layout = [	[sg.Button(matriz.celdas[j][i]['letra'],
					 size=(4,2),
					 pad=(0,0),
					 font=fuente,
					 key = str(j)+'_'+str(i)) for i in range(ANCHO)	] for j in range(ALTO)
				 ]
	size_pincel=(7, 2)
	pincel_layout = [
				[sg.Text('Adj', size=size_pincel, auto_size_text=False, enable_events=True,
				 relief='raised', text_color=color_marca['adj'][0], background_color=color_marca['adj'][1], justification='center', key='adj', tooltip='Elegir para marcar Adjetivos'),
				 sg.Text('Verb', size=size_pincel, auto_size_text=False, enable_events=True,
				 relief='raised', text_color=color_marca['verb'][0], background_color=color_marca['verb'][1], justification='center', key='verb', tooltip='Elegir para marcar Verbos'),
				 sg.Text('Sust', size=size_pincel, auto_size_text=False, enable_events=True,
				 relief='raised', text_color=color_marca['sust'][0], background_color=color_marca['sust'][1], justification='center', key='sust', tooltip='Elegir para marcar Sustantivos'),
				 ]
				]
	Errores_layout =[ [sg.T('--------------------------------------------------')],
					[ sg.T('Al presiona boton COMPROBAR VICTORIA:  ')],
					[ sg.T('# Si las letras cambian a color blanco:\n'
					'   °fueron marcadas con una categoria incorrecta')],
					[ sg.T('# Si no muestra mensaje de victoria :\n '
					'   °pueden quedar letras por marcar. \n'
					'    °Hay una palabra marcada incorrectamente.')]]
	#Layout principal.
	layout = [
				[sg.Menu(menu_princ)],
				[sg.Frame('Seleccionar color: ', pincel_layout),sg.Button('  Comprobar Victoria', key = 'comprobar victoria',tooltip= 'Marca con blanco las marcadasz erroneamente.')],
				[sg.Frame('', sopa_layout, font='System', title_color='blue'),
					sg.Frame('Ayudas: ',[	[sg.Text('Direcciones:', pad = ((20,0),0) )],
											[sg.Button(image_filename = config_dicc['orientacion']+'.png', 
														image_size=(80, 80), image_subsample=4, border_width=0,
														pad = ((30,0),(10,30)), button_color = color_fondo),
											sg.Column(ayuda_layout)],
											[sg.Column(Errores_layout)]
											
										]
							)
				]
			]

	layout.append([sg.Button('Cerrar')])
	window = sg.Window('Sopa de Letras').Layout(layout)
	
	start_time = time.time()
	def comprobar_victoria(layout,matriz):
		"""si seleccionamos boton comprobar victorias marca en blanco todas las letras que hayan sido presionadas erroneamente."""
		"""recorre toda la matriz comprobando que las celdas marcadas sean correctas"""
		for j in range(ANCHO):
					for i in range(ALTO):
						if matriz.celdas[j][i]['marcada'] == True:
							if matriz.celdas[j][i]['tipo'] in ('adj','verb','sust'):
								if matriz.celdas[j][i]['color'] != color_marca[matriz.celdas[j][i]['tipo']]:
									window.FindElement(str(j)+'_'+str(i)).Update(button_color = color_marca['Erroneas'])
									matriz.celdas[j][i]['color']= (color_marca['Erroneas'])
									window.Refresh()
							else:
								window.FindElement(str(j)+'_'+str(i)).Update(button_color = color_marca['Erroneas'])
								matriz.celdas[j][i]['color']= (color_marca['Erroneas'])
								
	def Win_Condition(matriz,win):
		"""primera parte: si la celda presionada esta marcada la desmarca y le asigna color Default. Sino la marca y le asigna color de celda marcada."""
		"""segunda parte: comprueba victoria atravez de un AND. si encuentra una celda que este marcada erroneamente arrastra el False."""
		for i in range(ANCHO):
			for j in range(ALTO):
				if (matriz.celdas[j][i]['key'] == event ):
					if matriz.celdas[j][i]['marcada']:
						matriz.celdas[j][i]['marcada'] = False
						color_celda = color_celda_default
					else:
						matriz.celdas[j][i]['marcada'] = True
						color_celda = color_celda_marcada
					matriz.celdas[j][i]['color'] = color_celda
					window.FindElement(event).Update(button_color = color_celda)
				
				if matriz.celdas[j][i]['tipo'] != None:
					if matriz.celdas[j][i]['tipo'] == 'MIXTO':
						if not(matriz.celdas[j][i]['marcada']):
							win *= False
						else:
							win *= True
					else:
						if matriz.celdas[j][i]['color'] != color_marca[matriz.celdas[j][i]['tipo']]: #no pudimos extraer el color de pysimplegui por eso le agregamos una key 'color' a la matriz
							win *= False
						else:
							win *= True
				else:
					if (matriz.celdas[j][i]['marcada']):
						win *= False
					else:
						win *= True
		return win	
	
	def Mensaje_Victoria():
			print('\nGanaste!')
					
			x_max,y_max = window.GetScreenDimensions()
			for rep in range(5):
				margen = 150
				x_0, y_0 =  random.randrange(x_max-margen-50), random.randrange(y_max-margen-50)
				# ~ x_0, y_0 = 555,450
				sign = random.choice([-1,1])
				v_x = sign*random.randrange(1,50)
				
				v_y = -1*random.randrange(10,30)
				# ~ v_x, v_y = 10,10
				g = 5
				t = 0
				rebote = 0
				x,y=x_0,y_0
				
				while rebote < 3 and t < 500:
					x = x + v_x
					v_y = v_y + g
					y = y + v_y
					
					rand_col = ['#'+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
									for i in range(4)]
					# ~ print(rand_col)## ['#C7980A', '#F4651F', '#82D8A7', '#CC3A05', '#575E76', '#156943', '#0BD055', '#ACD338']
					sg.Popup(' W I N N E R ',
							button_color = (rand_col[0],rand_col[1]),					# Color of buttons (text_color, background_color)
							background_color = rand_col[2],				# Color of background
							text_color = rand_col[3], 					# Color of text
							# ~ button_type = 'POPUP_BUTTONS_NO_BUTTONS',
							auto_close = True,					# If True window will automatically close
							auto_close_duration = 5,			# Number of seconds for autoclose
							non_blocking = True,					# If True returns immediately
							line_width = 50,						# Width of lines in characters
							font = 'Fixedsys' ,							# Font to use for characters
							no_titlebar = False,					# If True no titlebar will be shown
							grab_anywhere = False,					# If True can move window by grabbing anywhere
							keep_on_top = True,					# If True window will be on top of other windows
							location = (x,y)					# (x,y) coordinates to show the window
							)
					if x < 5:
						v_x = -1 * v_x
					if y < 5: 
						v_y = -1 * v_y
					if x > x_max-margen:
						v_x = -1 * v_x
					if y > y_max-margen:
						rebote +=1
						v_y = -1 * v_y
					t+=1
				
			elapsed_time = time.time() - start_time
			elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
			playsound('mlg-airhorn.mp3')
			sg.Popup('¡¡GANASTE!!\nTiempo: '+elapsed_time, font = 'Fixedsys', keep_on_top=True)				
	
	while True:				 # Event Loop
		event, val = window.Read()
		
		if event is None or event == 'Cerrar':
			break
			
		if event == 'Guardar...::Menu':
			filename = 'savegame.sav'
			print('Guardo en ',filename)
			window.SaveToDisk(filename)
			
		if event == 'Cargar...::Menu':
			filename = 'savegame.sav'
			print('Cargar ',filename)
			window.LoadFromDisk(filename)
			
		if event == 'Como jugar?::Menu':
			window.SetAlpha(0.5)
			sg.Popup(HOWTO,font = 'System', keep_on_top=True)
			window.Reappear() 
		
		if event == 'Acerca de...::Menu':
			window.SetAlpha(0.5)
			sg.Popup(CREDITS,font = 'System', keep_on_top=True)
			window.Reappear() 
			
		if event == 'comprobar victoria':
			comprobar_victoria(layout,matriz)
			
		if event in ('adj','verb','sust'):  # Si toco el pincel
			color_celda_marcada = color_marca[event]
			for element in ('adj','verb','sust'):
				window.FindElement(element).Update(value = element)
			window.FindElement(event).Update(value ='* '+event.upper()+' *')
					
		win = True
		win = Win_Condition(matriz,win)
		if win == True and event == 'comprobar victoria':
			Mensaje_Victoria()

	window.Close()

if __name__ == "__main__":
	if config.cargar_configuracion()[2] != []:
		dibujar()

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
import config
import sopa
import PySimpleGUI as sg

def existe_archivo_de_configuracion():
	''' Para ver si existe la configuración me fijo si la función devuelve el elemento vacío que es cuando lo inicializa'''
	_,_,res = config.cargar_configuracion()
	cond = res != []
	return cond

color_fondo = config.colores(config.cargar_configuracion()[0])['splash']
sg.SetOptions(	background_color = color_fondo[1],
				text_element_background_color=color_fondo[1],
				element_background_color=color_fondo[1],
				text_color=color_fondo[0]
				)
menu_princ = [	['&Opciones', ['Configuración::Menu', 'Exit::Menu'  ]],    
				['&Ayuda', '&Acerca de...::Menu']
			]
layout = [
			[sg.Menu(menu_princ, key='Menu' )],
			[sg.Text('Sopa de Letras', font = ('Fixedsys',25), pad = (90,8),justification = 'center')],
			[sg.Button('',image_filename='img/jugar.png', image_size =(450, 210), image_subsample=1, border_width=0, 
				key='_jugar_', pad = (55,(8,55)), button_color = color_fondo)]
		]

window = sg.Window('Sopa de Letras en PySimpleGUI').Layout(layout)

while True:				 # Event Loop
	event, val = window.Read()
	print('Event:', event, ',   Val:', val)
	if event is None or event in ('Cerrar','Exit::Menu'):
		break

	elif event == 'Acerca de...::Menu':
		sg.Popup(CREDITS,font = 'System')

	elif event == 'Configuración::Menu':
		window.Hide() 
		config.main()
		# menu_princ[0][1][0] = '!Configuración::Menu' # esto era para desactivarlo y que se pueda abrir solo una vez
		# window.Element('Menu').Update(menu_princ)
		# window.Refresh()
		window.UnHide()
	
	elif event == '_jugar_':
		if existe_archivo_de_configuracion():
			window.Hide()
			sopa.dibujar()
			window.UnHide()
		else:
			sg.Popup('Primero debes configurar el juego!\n Ve a Opciones -> Configuración')



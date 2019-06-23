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
	_,_,res = config.cargar_configuracion()
	cond = res != []
	# ~ print(cond)
	return cond

color_fondo = config.colores()

menu_princ = [	['&Opciones', ['Configuracion::Menu', 'Exit::Menu'  ]],    
				['&Ayuda', '&Acerca de...::Menu']
			]
layout = [
			[sg.Menu(menu_princ, key='Menu' )],
			[sg.Text('Sopa de Letras', font = ('Fixedsys',25), pad = (90,8),justification = 'center')],
			[sg.Button('',image_filename='jugar.png', image_size =(450, 210), image_subsample=1, border_width=0, 
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

	elif event == 'Configuracion::Menu':
		window.Hide() ## Aca hay un error cuando llamo por segunda vez a configuracion(), un problema de tkinter parece...
		# ~ try:
			# ~ config.configuracion()
		# ~ except _tkinter.TclError:
			# ~ print('error duplicado')
		# ~ except NameError:
			# ~ print('error nombre',NameError)
		# ~ except:
			# ~ print('?')
		## no sirven las excepciones
		config.configuracion()
		
		## por ahora lo solucionamos editando el menu para deshabilitar la opciond de config
		menu_princ = [	['&Opciones', ['!Configuracion::Menu', 'Exit::Menu'  ]],    
						['&Ayuda', '&Acerca de...::Menu']
					 ]
		window.Element('Menu').Update(menu_princ)
		
		window.Refresh()
		window.UnHide()
	
	elif event == '_jugar_':
		if existe_archivo_de_configuracion():
			window.Hide()
			sopa.dibujar()
			window.UnHide()
		else:
			sg.Popup('Primero debes configurar el juego!\n Ve a Opciones -> Configuración')
#splash art, menues



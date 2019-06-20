import config
import grilla
import sopa
import PySimpleGUI as sg

def existe_archivo_de_configuracion():
	_,res,_ = config.cargar_configuracion()
	return res != []

# ~ ## Colores interfaz
sg.SetOptions(
background_color='#EFF0D1',
text_element_background_color='#EFF0D1',
element_background_color='#EFF0D1',
scrollbar_color=None,
input_elements_background_color='#D7C0D0', #lila
progress_meter_color = ('green', 'blue'),
button_color = ('#262730','#77BA99')
)

menu_princ = [['&Opciones', ['Configuracion', 'Exit::Menu'  ]],    
				['&Ayuda', '&Acerca de...']
			]
layout = [
			[sg.Menu(menu_princ)],
			[sg.Text('Sopa de Letras', font = ('Fixedsys',25), pad = (90,8),justification = 'center')],
			[sg.Button('',image_filename='jugar.png', image_size=(450, 210), image_subsample=1, border_width=0, 
				key='_jugar_', pad = (55,(8,55)), button_color=('#262730','#EFF0D1'))]
		]

window = sg.Window('Sopa de Letras en PySimpleGUI').Layout(layout)

while True:				 # Event Loop
	event, val = window.Read()
	#print(event, val)
	if event is None or event in ('Cerrar','Exit::Menu'):
		break
	if event == 'Configuracion':
		window.Hide()
		config.configuracion()
		window.UnHide()
	if event == '_jugar_':
		if existe_archivo_de_configuracion():
			window.Hide()
			sopa.dibujar()
			window.UnHide()
		else:
			sg.Popup('Primero debes configurar el juego!\n Ve a Opciones -> Configuración')
#splash art, menues



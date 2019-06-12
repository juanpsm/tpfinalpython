import PySimpleGUI as sg
import random
import string

color_celda_marcada = ('#EFF0D1','#D33F49') #blanco y rojo
color_marca = {'adj':('#262730','purple1'), 'verb':('#262730','green3'), 'sust':('#262730','yellow2')}
color_celda_default = ('#262730','#77BA99') #negro y verde


ANCHO = 7
ALTO = 8

sg.SetOptions(
background_color='#EFF0D1',
text_element_background_color='#EFF0D1',
element_background_color='#EFF0D1',
scrollbar_color=None,
input_elements_background_color='#D7C0D0', #lila
progress_meter_color = ('green', 'blue'),
button_color=color_celda_default
)
FUENTES=['Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica']
fuente = FUENTES[3]
fila=[str(i) for i in range(ANCHO)]
#print(fila)
matriz=[
		[{'key':str(j)+'_'+str(i),'marcada':False,'letra':random.choice(string.ascii_uppercase)} for i in range(ANCHO)]
		for j in range(ALTO)
]
matriz.append('end')
print(matriz)
sopa_layout = [
			[sg.Button(matriz[j][i]['letra'],
			 size=(4,2),
			 pad=(5,5),
			 font=fuente,
			 key = str(j)+'_'+str(i)) for i in range(ANCHO)]
		for j in range(ALTO)
		 ]
		 # ~ ,sg.Button('Verb',button_color='green3'),sg.Button('Sust',button_color='yellow2')
		 # ~ flat, groove, raised, ridge, solid, or sunken
size_pincel=(7, 1)
pincel_layout = [
			[sg.Text('Adj', size=size_pincel, auto_size_text=False, enable_events=True,
			 relief='raised', text_color=color_marca['adj'][0], background_color=color_marca['adj'][1], justification='center', key='adj', tooltip='Elegir para marcar Adjetivos'),
			 sg.Text('Verb', size=size_pincel, auto_size_text=False, enable_events=True,
			 relief='raised', text_color=color_marca['verb'][0], background_color=color_marca['verb'][1], justification='center', key='verb', tooltip='Elegir para marcar Verbos'),
			 sg.Text('Sust', size=size_pincel, auto_size_text=False, enable_events=True,
			 relief='raised', text_color=color_marca['sust'][0], background_color=color_marca['sust'][1], justification='center', key='sust', tooltip='Elegir para marcar Sustantivos'),
			 ]
			]
layout = [
			[sg.Frame('elegir tipo', pincel_layout)],
			[sg.Frame('', sopa_layout, font='Any 12', title_color='blue')]
		]

layout.append([sg.Button('Cerrar')])
window = sg.Window('TEMP GUI').Layout(layout)


while True:				 # Event Loop
	event, val = window.Read()
	#print(event, val)
	if event is None or event == 'Cerrar':
		break
	if event in ('adj','verb','sust'):
		color_celda_marcada = color_marca[event]
		for element in ('adj','verb','sust'):
			window.FindElement(element).Update(value = element)
		window.FindElement(event).Update(value ='* '+event.upper()+' *')
	# ~ if any([event in matriz[j] for j in range(ALTO)]):
	for i in range(ANCHO):
		for j in range(ALTO):
			if (matriz[j][i]['key'] == event ):
				if matriz[j][i]['marcada']:
					matriz[j][i]['marcada'] = False
					color_celda=color_celda_default
				else:
					matriz[j][i]['marcada'] = True
					color_celda = color_celda_marcada
				#print(matriz)
				window.FindElement(event).Update(button_color = color_celda)
	window.Refresh()

window.Close()

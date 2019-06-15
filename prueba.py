import PySimpleGUI as sg
import random
import string

color_celda_marcada = ('#EFF0D1','#D33F49') #blanco y rojo
color_marca = {None:('#EFF0D1','#D33F49'),
				'adj':('#262730','purple1'), 'verb':('#262730','green3'), 'sust':('#262730','yellow2'),
				'MIXTO':('#262730','#3e8271')}
color_celda_default = ('#262730','#77BA99') #negro y verde

import grilla



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



palabras_docente = {'careta':{'tipo':'adj','def':''},'sucio':{'tipo':'adj','def':''},'apestoso':{'tipo':'adj','def':''},
					'correr':{'tipo':'verb','def':''},'economizar':{'tipo':'verb','def':''},'cancherear':{'tipo':'verb','def':''},
					'rayuela':{'tipo':'sust','def':''},'perro':{'tipo':'sust','def':''},'gato':{'tipo':'sust','def':''}}
separadas = []
palabras = list(palabras_docente.keys())
sg.Popup(sorted(separadas))		
#ANCHO = max(len(max(palabras, key=len)),2*len(palabras))
ANCHO = len(max(palabras, key=len))
ALTO = ANCHO
print('ANCHO:',ANCHO,'Alto:',ALTO)
matriz = grilla.crear_grilla(palabras)
print('0 1 =',matriz.celdas[0][1])
def cantidad_palabras(matriz,separadas):
	for fila in range(ANCHO):
		for columna in range(ALTO):
			if matriz.celdas[fila][columna]['tipo'] in ['adj','sust','verb']:
				separadas.append(matriz.celdas[fila][columna]['letra'])
cantidad_palabras(matriz,separadas)				
# ~ matriz=[
		# ~ [{'key':str(j)+'_'+str(i),'marcada':False,'letra':g.celdas[i][j]} for i in range(ANCHO)]
		# ~ for j in range(ALTO)
# ~ ]

grilla.print_resultado(matriz)
sopa_layout = [
			[sg.Button(matriz.celdas[j][i]['letra'],
			 size=(1,1),
			 pad=(0,0),
			 font=fuente,
			 key = str(j)+'_'+str(i)) for i in range(ANCHO)]
		for j in range(ALTO)
		 ]
		 # ~ ,sg.Button('Verb',button_color='green3'),sg.Button('Sust',button_color='yellow2')
		 # ~ flat, groove, raised, ridge, solid, or sunken
size_pincel=(8, 1)
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
palwin = []
ganaste = False
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
			if (matriz.celdas[j][i]['key'] == event ):
				if matriz.celdas[j][i]['marcada']:
					matriz.celdas[j][i]['marcada'] = False
					color_celda = color_celda_default
					matriz.celdas[j][i]['color'] = color_celda
					window.FindElement(event).Update(button_color = color_celda)
				else:
					matriz.celdas[j][i]['marcada'] = True
					color_celda = color_celda_marcada
					matriz.celdas[j][i]['color'] = color_celda
					window.FindElement(event).Update(button_color = color_celda)
					if matriz.celdas[j][i]['color'] != color_marca[matriz.celdas[j][i]['tipo']]:
						print(str(j)+'_'+str(i), end=' > ')
						print(matriz.celdas[j][i]['tipo'])
					elif matriz.celdas[j][i]['tipo'] == 'MIXTO':
						print('es mixto')
						palwin.append(matriz.celdas[j][i]['letra'])
						palwin.append(matriz.celdas[j][i]['letra'])
						window.FindElement(str(j)+'_'+str(i)).Update(button_color = color_marca['MIXTO'])
					elif matriz.celdas[j][i]['tipo'] in ('adj','sust','verb'):
						palwin.append(matriz.celdas[j][i]['letra'])
					print('una letra mas')
				#print(matriz.celdas)
	for i in range(ANCHO):
		for j in range(ALTO):
			if matriz.celdas[j][i]['marcada']:
				# ~ print(str(j)+'_'+str(i), end=' > ')
				# ~ print(matriz.celdas[j][i]['color'])
				
				# ~ print(matriz.celdas[j][i]['tipo'])
				print()
				# ~ print(dir(window.FindElement(str(j)+'_'+str(i))))
	print(sorted(palwin))
	print(sorted(separadas))		
	if sorted(palwin) == sorted(separadas):
		ganaste = True
	if ganaste ==  True :
		 sg.Popup('GANASTE')
	print()
	window.Refresh()

window.Close()

import PySimpleGUI as sg
import random
import string
import json

color_celda_marcada = ('#EFF0D1','#D33F49') #blanco y rojo
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

def config():
	layout = [[ sg.T('menu configuracion:')],
	[sg.Frame ( layout = [

	[sg.Radio('Sin ayuda', 'Radio2'),
	sg.Radio('definiciones','Radio2'),
	sg.Radio('solo palabras','Radio2')]],
	title='ayudas', relief=sg.RELIEF_SUNKEN)],

	[sg.Frame (layout = [

	[sg.Radio('verbo', "RADIO1",default = True,key = 'verbo'),
	sg.Radio('sustantivo', 'RADIO1',key = 'sustantivo'),
	sg.Radio('adjetivo', 'RADIO1',key = 'adjetivo')],

	[sg.InputText((),key = 'input')],
	[sg.ReadButton('boton')]],
	title = 'tipo de palabra')],
	[sg.ReadButton('terminar')]
	]
	window = sg.Window('ventana').Layout(layout)
	verbos = []
	sustantivos = []
	adjetivos = []
	while True:
		event, values = window.Read()
		if event == 'terminar':
			break
		if values['verbo'] == True:
					verbos.append(values['input'])
		elif values['sustantivo'] == True:
				sustantivos.append(values['input'])
		elif values['adjetivo'] == True:
				adjetivos.append(values['input'])
	#sg.Popup(verbos)
	#sg.Popup(adjetivos)
	#sg.Popup(sustantivos)
	archiv = {}
	archiv['verbos'] = []
	for x in verbos:
		print('variable')
		print(x)
		archiv['verbos'].append(x)
	print (archiv)
	archiv['sustantivos'] = []
	for x in sustantivos:
		archiv['sustantivos'].append(x)
	archiv['adjetivos'] = []
	for x in adjetivos:
		archiv['adjetivos'].append(x)
	archivo = sg.PopupGetFile('filename to open', no_window=True, file_types=(("json Files","*.json"),))
	with open(archivo, "w") as f:
		json.dump(archiv,f, sort_keys=True, indent=4)
	return verbos,adjetivos,sustantivos

verbos,adjetivos,sustantivos = config()

fila=[str(i) for i in range(ANCHO)]
#print(fila)
matriz=[
		[{'key':str(j)+'_'+str(i),'marcada':False,'letra': random.choice(string.ascii_uppercase) }for i in range(ANCHO)]
		for j in range(ALTO)
]
matriz.append('end')
print(matriz)
layout = [
			[sg.Button(matriz[j][i]['letra'], size=(4,2), pad=(5,5), key = str(j)+'_'+str(i)) for i in range(ANCHO)]
		for j in range(ALTO)
		 ]
layout.append([sg.Button('Cerrar')])
window = sg.Window('TEMP GUI').Layout(layout)
window.Finalize()

while True:                 # Event Loop
	event, val = window.Read()
	#print(event, val)
	if event is None or event == 'Cerrar':
		break
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
def agregar(palabra,fila,columna):
	print(palabra)
	for j in palabra:
			pas = str(fila)+'_'+str(columna)
			sg.Popup(pas)
			window.FindElement(str(fila)+'_'+str(columna)).Update(j)
			columna = columna +1
def palabras(verbos):
	for x in verbos:
		posicion_inicial = random.randint(0,ALTO)
		rango = ANCHO-len(x)
		posicion_inicial = ANCHO-len(x)
		columna = random.randint(0,rango)
		agregar(x,posicion_inicial,columna)
sg.Popup('inicio de proceso')
palabras(verbos)
print('layout')
window = sg.Window('TEMP GUI').Layout(layout)
window.Read()
window.Close()

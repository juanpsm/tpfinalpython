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
def cantidad_pal(verbos,adjetivos,sustantivos):
			total= 0
			cantv = 0
			cantadj = 0
			cantsust = 0
			for x in verbos:
				total = total +1
				cantv = cantv + 1
			for x in adjetivos:
					total = total +1
					cantadj = cantadj + 1
			for x in sustantivos:
				total = total +1
				cantsust = cantsust + 1
			return cantv,cantadj,cantsust,total	
verbos,adjetivos,sustantivos,values = config()	

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

def ayuda(layout,values):
	cantv,cantadj,cantsust,total= cantidad_pal(verbos,adjetivos,sustantivos)
	if values['sin ayuda'] == True:
		column1 = [
				[sg.T('Total de palabras a buscar palabras a buscar: ' + str(total), justification='center')],
				[sg.T('Verbos: '+ str(cantv)),
				sg.T('Adjetivos: '+ str(cantadj)),
				sg.T('Sustantivos: '+ str(cantsust))]
				]
		layout.append(([sg.Column(column1, background_color='#77BA99')]))		
	elif values[' definiciones'] == True:
		column1 = [
			[sg.Text('ayuda: palabras a buscar. ', background_color='#77BA99', justification='center')],
            [sg.T(verbos[j])for j in range(cantv)],
            [sg.T(adjetivos[j])for j in range(cantadj)],
            [sg.T(sustantivos[j])for j in range(cantsust)]
            ]
		layout.append(([sg.Column(column1, background_color='#F7F3EC')]))    
	elif values['mostrar palabras'] == True:
		column1 = [
			[sg.Text('ayuda: palabras a buscar. ', background_color='#77BA99', justification='center')],
            [sg.T(verbos[j])for j in range(cantv)],
            [sg.T(adjetivos[j])for j in range(cantadj)],
            [sg.T(sustantivos[j])for j in range(cantsust)]
            ]
		layout.append(([sg.Column(column1, background_color='#F7F3EC')]))
ayuda(layout,values)

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
def esp_libre(palabra, fila, columna):
	marcada = 0
	for x in palabra:
		if matriz[fila][columna]['marcada'] == True:
			marcada = marcada +1
	if marcada > 0:			
		return False
	else: 
		return True		
def agregar(palabra,fila,columna):
	print(palabra)
	for j in palabra:
			pas = str(fila)+'_'+str(columna)
			sg.Popup(pas)
			window.FindElement(str(fila)+'_'+str(columna)).Update(j.upper())
			columna = columna +1
def palabras(verbos):
	for x in verbos:
		alto = ALTO-1
		posicion_inicial = random.randint(0,alto)
		rango = ANCHO-len(x)
		print('ancho'+str(ANCHO))
		print('tam_pal:' + str(len(x)))
		print(rango)
		posicion_inicial = ANCHO-len(x)
		columna = random.randint(0,rango)
		marcadas = esp_libre(x,posicion_inicial,columna)
		#marcadas vuelve con false o true, si alguna casilla en la key'marcado'  == true entonces se devuelve false y significa que en esa fila no se puede trabajar.
		sg.Popup(marcadas)
		print(columna)
		acceso = 0
		while marcadas == False:
			#si marcadas es false buscamos otra fila para trabajar y preguntamos si en esta si se puede agregar la palabra.
			posicion_inicial = random.randint(0,alto)
			marcadas = esp_libre(x,posicion_inicial,columna)
			#sg.Popup(marcadas) es variable para control. para saber que devuelve la func y si hace otro acceso a la misma o no. 
			sg.Popup(marcadas)
			acceso = acceso+1
			print('accesos' + str(acceso))
		agregar(x,posicion_inicial,columna) 
sg.Popup('inicio de proceso')
palabras(verbos)
print('layout')
window = sg.Window('TEMP GUI').Layout(layout)
window.Read()
window.Close()

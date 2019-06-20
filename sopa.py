import PySimpleGUI as sg
import random

import grilla as g
import config


def dibujar():

	## Esto habrá que setearlo luego con la raspberry

	#Colores marcas
	color_celda_marcada = ('#EFF0D1','#D33F49') #blanco y rojo
	color_marca = {None:('#EFF0D1','#D33F49'), #blanco y rojo
					'adj':('#262730','purple1'),
					'verb':('#262730','green3'),
					'sust':('#262730','yellow2'),
					'MIXTO':('#262730','#3e8271')}
	color_celda_default = ('#262730','#77BA99') #negro y verde

	## Colores interfaz
	sg.SetOptions(
	background_color='#EFF0D1',
	text_element_background_color='#EFF0D1',
	element_background_color='#EFF0D1',
	scrollbar_color=None,
	input_elements_background_color='#D7C0D0', #lila
	progress_meter_color = ('green', 'blue'),
	button_color=color_celda_default
	)

	## Configuracion manual
	# ~ FUENTES=['Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica']
	# ~ fuente = FUENTES[3]

	# ~ palabras_dicc = {'careta':{'tipo':'adj','def':''},'sucio':{'tipo':'adj','def':''},'apestoso':{'tipo':'adj','def':''},
						# ~ 'correr':{'tipo':'verb','def':''},'economizar':{'tipo':'verb','def':''},'cancherear':{'tipo':'verb','def':''},
						# ~ 'rayuela':{'tipo':'sust','def':''},'perro':{'tipo':'sust','def':''},'gato':{'tipo':'sust','def':''}}
	# ~ matriz=[
			# ~ [{'key':str(j)+'_'+str(i),'marcada':False,'letra':g.celdas[i][j]} for i in range(ANCHO)]
			# ~ for j in range(ALTO)
	# ~ ]


	
	config_dicc, palabras_dicc, palabras_lista = config.cargar_configuracion()
	fuente = config_dicc['fuente']
	
	matriz = g.crear_grilla(palabras_lista)
	ANCHO = max(len(max(palabras_lista, key=len)),len(palabras_lista))
	#ANCHO = len(max(palabras_lista, key=len))
	ALTO = ANCHO
	
	def cantidad_pal(palabras_dicc):
			"""recibe diccionario con todos los datos de las palabras y devuelve la cantidad de palabras por cada tipo"""
			cantv = 0
			cantadj = 0
			cantsust = 0
			for x in palabras_dicc:
				if palabras_dicc[x]['tipo'] == 'verb':
					cantv = cantv+1
				elif palabras_dicc[x]['tipo'] == 'sust':
					cantsust = cantsust+1
				elif palabras_dicc[x]['tipo'] == 'adj':	
					cantadj = cantadj +1 
			return cantv,cantadj,cantsust
			
	def ayuda(palabras_lista,palabras_dicc,config_dicc):
		"""depende de lo recibido en la configuracion de ayuda modifica el layout  para que informe lo correspondiente a cada caso"""
		""" ayuda_layout lista creada para agregarlo al frame al layout de la sopa"""
		cantv,cantadj,cantsust = cantidad_pal(palabras_dicc)
		ayuda_layout=[]
		if config_dicc['ayuda'] == 'sin ayuda':
			column1 = [
				[sg.T('Total de palabras a buscar palabras a buscar: ' + str(len(palabras_lista)), justification='center')],
				[sg.T('Verbos: '+ str(cantv)),
				sg.T('Adjetivos: '+ str(cantadj)),
				sg.T('Sustantivos: '+ str(cantsust))]
				]
			ayuda_layout = [
							[sg.Column(column1, background_color='#F7F3EC')]]
		# si es definiciones agrega al layout un numero para la palabra y su descripcion.	
		# 'palabra num-'+str(j) : asigna un numero a la palabra para mostrar en layout.
		#  palabras_dicc[palabras_lista[j]]['def'] : accese a la descripcion de la palabra a la que referencia el numero para informar.
		# para referenciado por numero toma la posicion en la lista de palabras.
		elif config_dicc['ayuda'] == 'definiciones':
			column1 = [
				[sg.T ('palabra num-'+str(j)+' :'+palabras_dicc[palabras_lista[j]]['def'])]for j in range(len(palabras_lista))]
			ayuda_layout = [ [sg.T('Definiciones: ')],
							[sg.Column(column1, background_color='#F7F3EC')]]
		elif config_dicc['ayuda'] == 'palabras':
			column1 = [
				[sg.T(palabras_lista[j]) for j in range(len(palabras_lista))]
				]
			ayuda_layout = [
							[sg.T('Palabras a buscar :')],
							[sg.Column(column1, background_color='#F7F3EC')]]
		return ayuda_layout
	
	ayuda_layout = ayuda(palabras_lista,palabras_dicc,config_dicc)
	
	print('ANCHO:',ANCHO,'Alto:',ALTO)

	#g.print_resultado(matriz)
	
	# ------ Menu Definition ------ #      
# ~ menu_def = [['&File', ['&Open', '!&Save', '---', 'Properties', 'E&xit'  ]],      
            # ~ ['!&Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],      
            # ~ ['&Help', '&About...'],]    
	#layout = [[sg.Menu(menu_def)]]
	menu_princ = [['&File', ['&Open', '!&Save', '---', 'Properties', 'E&xit'  ]],
				['!&Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],      
				['&Help', '&About...']]
	sopa_layout = [
				[sg.Button(matriz.celdas[j][i]['letra'],
				 size=(3,1),
				 pad=(0,0),
				 font=fuente,
				 key = str(j)+'_'+str(i)) for i in range(ANCHO)]
			for j in range(ALTO)
			 ]

	# Botones para seleccionar que tipo de palabra marcar
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
				[sg.Menu(menu_princ)],
				[sg.Frame('', pincel_layout)],
				[sg.Frame('', sopa_layout, font='Any 12', title_color='blue')],
				[sg.Frame('',ayuda_layout)]
			]

	layout.append([sg.Button('Cerrar')])
	window = sg.Window('Sopa de Letras').Layout(layout)
	

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
					else:
						matriz.celdas[j][i]['marcada'] = True
						color_celda = color_celda_marcada
					#print(matriz.celdas)
					matriz.celdas[j][i]['color'] = color_celda
					window.FindElement(event).Update(button_color = color_celda)
					
		## Luego de cada movimiento reviso todas las celdas para ver si ya gané. Claramente se puede juntar con los for de arriba
		win = True #despues lo voy a juntar con "and" asi que con que haya uno falso me lo vuelve todo falso
		for i in range(ANCHO):
			for j in range(ALTO):
				
				if matriz.celdas[j][i]['tipo'] != None:
					if matriz.celdas[j][i]['tipo'] == 'MIXTO':
						if not(matriz.celdas[j][i]['marcada']):
							##print('Marcar',str(j)+'_'+str(i),'con cualquier color', end=' > ')
							#print('win =',win,'lo pongo en',end=' ')
							win *= False
							#print(win)
						else:
							win *= True
					else:
						if matriz.celdas[j][i]['color'] != color_marca[matriz.celdas[j][i]['tipo']]: #no pudimos extraer el color de pysimplegui por eso le agregamos una key 'color' a la matriz
							#print('Marcar',str(j)+'_'+str(i),'con color',matriz.celdas[j][i]['tipo'], end=' > ')
							#print('win =',win,'lo pongo en',end=' ')
							win *= False
							#print(win)
						else:
							win *= True
				else:
					if (matriz.celdas[j][i]['marcada']):
						#print(str(j)+'_'+str(i),'esa marcada y deberia no estarlo', end=' > ')
						#print('win =',win,'lo pongo en',end=' ')
						win *= False
						#print(win)
					else:
						win *= True

		print('\n WIN =',win)
		if win: sg.Popup('GANASTE')
		print('---------------------------------------')
		window.Refresh()

	window.Close()

#MOSTRAR LAS AYUDAS
# ~ cantv,cantadj,cantsust,total= cantidad_pal(verbos,adjetivos,sustantivos)
	# ~ if values['sin ayuda'] == True:
		# ~ column1 = [
				# ~ [sg.T('Total de palabras a buscar: ' + str(total), justification='center')],
				# ~ [sg.T('Verbos: '+ str(cantv)),
				# ~ sg.T('Adjetivos: '+ str(cantadj)),
				# ~ sg.T('Sustantivos: '+ str(cantsust))]
				# ~ ]
		# ~ layout.append(([sg.Column(column1, background_color='#77BA99')]))		
	# ~ elif values[' definiciones'] == True:
		# ~ column1 = [
			# ~ [sg.Text('ayuda: palabras a buscar. ', background_color='#77BA99', justification='center')],
            # ~ [sg.T(verbos[j])for j in range(cantv)],
            # ~ [sg.T(adjetivos[j])for j in range(cantadj)],
            # ~ [sg.T(sustantivos[j])for j in range(cantsust)]
            # ~ ]
		# ~ layout.append(([sg.Column(column1, background_color='#F7F3EC')]))    
	# ~ elif values['mostrar palabras'] == True:
		# ~ column1 = [
			# ~ [sg.Text('ayuda: palabras a buscar. ', background_color='#77BA99', justification='center')],
            # ~ [sg.T(verbos[j])for j in range(cantv)],
            # ~ [sg.T(adjetivos[j])for j in range(cantadj)],
            # ~ [sg.T(sustantivos[j])for j in range(cantsust)]
            # ~ ]
		# ~ layout.append(([sg.Column(column1, background_color='#F7F3EC')]))
if __name__ == "__main__":
	dibujar()

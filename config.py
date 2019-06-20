import PySimpleGUI as sg
import random
import string
import json
import os
import datetime
from pprint import pprint
from buscar_en_wiktionary import buscar_en_wiktionary

nombre_archivo_config = 'configuracion.json'
nombre_archivo_reporte = 'reporte_de_errores.txt'

def reporte(r,error):
	"""pone en archivo de texto un reporte de los errores encontrados en la ejecucion de la sopa de letras"""
	""" recibe un numero de error y en base a el informa que tipo de error es"""
	hora = datetime.datetime.now()
	hora = str(hora)[:-10]
	
	if error == 1:
		texto = '[{}] {}: Wiktionario la clasificó como "{}" y pattern como "{}".\n'.format(hora,r['palabra'],r['clasificacion_wiktionario'],r['clasificacion_pattern'])
	
	elif error ==2:
		texto = '[{}] El termino "{}": no se encontró en ningun motor de busqueda.\n'.format(hora,r['palabra'])

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
	#recibo categoria pero en la consigna no la piden, tengo que extraerla de los motores.
	#Si funciona esto bien, si no nos queadremos con nuestro metodo de ponerla manualmente.
	resultado = buscar_en_wiktionary(palabra)
	# resultado tiene los campos:
	# 'palabra' [str] la que busqué
	# 'clasif_wik' [str] si se encontro en wiktionario
	# 'clasif_patt' [str] si se encontro en pattern
	# 'definicion' [str] si se encontro en wiktionario
	# los campos que no se pudieron recuperar tendran None
	clasificacion_definitiva = resultado['clasificacion_pattern']
	definicion = resultado['definicion']
	
	if resultado['clasificacion_wiktionario'] != resultado['clasificacion_pattern'] and resultado['clasificacion_wiktionario'] != 'MIXTA':
		print('Reportando Error 1...')
		reporte(resultado, 1)
		clasificacion_definitiva = resultado['clasificacion_wiktionario']

		if resultado['clasificacion_wiktionario'] == '_Ninguna_': # y como son distintas se supone que pattern dio distinto de None
			# aca el problema es que pattern siempre da NN por DEFECTO, pero bueno si seguimos la consigna..
			# EDIT: ahora anda!!
			clasificacion_definitiva = resultado['clasificacion_pattern']
			
			ingreso = [	[sg.T('No se encontro la palabra en Wiktionario.\nDefínala:\n')],
						[sg.Radio('Sustantivo', "RADIOp",default = True,key='_esSus_'), 
						sg.Radio('Adjetivo', "RADIOp",key='_esAdj_'),
						sg.Radio('Verbo', "RADIOp",key='_esVer_')],
						[sg.Input(key = 'def')],
						[sg.Submit(key = 'submit')]
						]
			window2 = sg.Window('Definicion ').Layout(ingreso)
			button,values2=window2.Read()
			if button == 'submit':
				definicion = values2['def']
				clasificacion_definitiva = 'adj' if values2['_esAdj_'] else 'verb' if values2['_esVer_'] else 'sust'
				window2.Close()
			#definicion = input('No se encontro la palabra en Wiktionario.\nDefínala:\n') #Aca habría que hacer un popup
	elif resultado['clasificacion_pattern'] == '_Ninguna_': # Las dos None
		print('Reportando Error 2...')
		reporte(resultado,2)
		#no incluir palabra
		clasificacion_definitiva = '_no_aceptada_'
		definicion = '_no_aceptada_'
	
	return clasificacion_definitiva, definicion
	
def cargar_configuracion():
	"""abre archivo json con la configuracion cargada anteriormente"""
	"""si el archivo de configuracion no fue cargado previamente informa que no existe el mismo
	y devuelve todas las variables vacias necesarias para cargar datos nuevos"""
	existe = os.path.isfile(nombre_archivo_config)
	if existe:
		with open(nombre_archivo_config, 'r', encoding = 'utf-8') as f:
			config_dicc = json.load(f)
		# ~ print('Configuracion guardada:')
		# ~ print(json.dumps(config_dicc, sort_keys=True, indent=4, ensure_ascii = False))
		palabras_dicc = config_dicc['palabras']
	else:
		config_dicc = {}
		config_dicc['palabras'] = []
		palabras_dicc = {}
		print('no existe archivo de configuracion')
	palabras_lista = list(palabras_dicc.keys())
	return config_dicc,palabras_dicc,palabras_lista
	
def configuracion():
	"""recibe de cargar_configuracion() la configuracion elegida por el usuario para la sopa de letras"""
	
	color_boton_por_defecto = ('black','white')
	orientacion = 'dirs_1' #por defecto
	
	config_dicc, palabras_dicc, palabras_lista = cargar_configuracion()
	pprint (palabras_dicc)

	menu = ['Menu', ['Definicion::_MENU_', 'Eliminar::_MENU_']]
	# print(config_dicc['palabras'])
	layout = [
			[sg.Text('nuevo texto')],
			[sg.Text('Instrucciones de configuracion')],
			[sg.Text('Palabra:')],
			# ~ [sg.Radio('Sustantivo', "RADIOp",default = True,key='_esSus_'),  ### Finalmente al andar lo de pattern no es necesario especificar el tipo de palabra
			 # ~ sg.Radio('Adjetivo', "RADIOp",key='_esAdj_'),
			 # ~ sg.Radio('Verbo', "RADIOp",key='_esVer_')],
			 
			[sg.Input(key='_IN_', do_not_clear=False)],
			[sg.Button('Agregar', bind_return_key=True, key='_ADD_')],
			
			[sg.Listbox(values=palabras_lista, default_values=None, enable_events=True, size=(40,6),
									key='_LISTA_', tooltip=None, right_click_menu= menu, visible=True)],
			[sg.Text('Cantidad de palabras con las que hacer la sopa :')],
			[sg.Text('sust'),sg.Input(size = (2,1), key='_CANT_S_'),
			 sg.Text('verb'),sg.Input(size = (2,1), key='_CANT_V_'),
			 sg.Text('adj'),sg.Input(size = (2,1), key='_CANT_A_')],
			
			[sg.Text('Ayudas:')],
			[sg.Radio('Sin ayuda', "RADIOA", key= 'sin', size=(10,1)),
			 sg.Radio('Definiciones', "RADIOA", key='defin'),
			 sg.Radio('Mostrar palabras', "RADIOA", default = True, key='pal')],
			
			[sg.Text('Orientacion:')],
			[sg.Button('',image_filename='dirs_1.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_1', button_color=color_boton_por_defecto),
			 sg.Button('',image_filename='dirs_2.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_2', button_color=sg.TRANSPARENT_BUTTON),
			 sg.Button('',image_filename='dirs_3.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_3', button_color=sg.TRANSPARENT_BUTTON),
			 sg.Button('',image_filename='dirs_4.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_4', button_color=sg.TRANSPARENT_BUTTON),
			 sg.Button('',image_filename='dirs_8.png', image_size=(60, 60), image_subsample=9, border_width=0, key='dirs_8', button_color=sg.TRANSPARENT_BUTTON),
			 ],
			 
			
			[sg.Text('Mayus')],
			[sg.Radio('Mayúscula', "RADIOn", key='mayus', size=(10,1)),
			 sg.Radio('Minúscula', "RADIOn", default = True, key='minus')],
			
			[sg.Text('Fuente')],
			[sg.InputCombo(('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'), key='_FONT_')],
			
			[sg.Text('Oficina')],
			[sg.Button('Guardar configuracion', key='_ACEPTAR_', disabled = False),sg.Button('Cerrar')]
			]
	window = sg.Window('CONFIGURACION').Layout(layout)

	while True:                 # Event Loop  
		
		event, val = window.Read()  
		# ~ print('EVENTO :',event,'\n----\n VAL = ',val,'\n-----\n')
		# ~ print(window.FindElement('_LISTA_').GetListValues())
		if event is None or event == 'Cerrar':  
			break
			
		if event == '_ADD_':
			palabra = val['_IN_']
			categoria = '' # 'adj' if val['_esAdj_'] else 'verb' if val['_esVer_'] else 'sust'
			definicion = ''
			
			
			
			if palabra != '':
				if palabra in palabras_dicc:
					print('Ya se encuentra esa palabra en la lista.')
				else:# si es no vacia y no esta en la lista, la analizo
					
					categoria, definicion = analizarpalabra(palabra,categoria)
					
					if definicion == '_no_aceptada_': 
						sg.Popup('No consideramos que '+palabra+' sea una palabra')
					
					else: # la agrego
						palabras_dicc[palabra] = {'tipo': categoria,'def': definicion}
						palabras_lista = window.FindElement('_LISTA_').GetListValues()
						palabras_lista.append(palabra)  #aca cargo y agrego a la lista, pordría agregar directamente porque ya definí la lista en la importacion.
						window.FindElement('_LISTA_').Update(values = palabras_lista)
		
		if event == 'Definicion::_MENU_':
			try: # aca hay problemas cuando no hay nada seleccionado, se puede resolver seteando un valor por defecto, aunque eso traeria problemas la primera vez que se carga, se puede resolver con exepciones
				texto = 'Definición de "'+val['_LISTA_'][0]+'":\n'
				texto += 'La palabra es un '+palabras_dicc[ val['_LISTA_'][0] ]['tipo']+'.\n'
				texto += palabras_dicc[ val['_LISTA_'][0] ]['def']
				sg.Popup(texto)
			except(KeyError):
				print(val['_LISTA_'][0])
			except(IndexError):
				print(val['_LISTA_'])
			
		if event == 'Eliminar::_MENU_':
			if val['_LISTA_'] != []: # otra forma de resolver el tema de la listbox sin seleccionar
				del palabras_dicc[val['_LISTA_'][0]]# El Listbox guarda en val una lista con un unico elemento que es el que esta seleccionado en ese momento.
				palabras_lista = window.FindElement('_LISTA_').GetListValues()
				palabras_lista.remove(val['_LISTA_'][0])
				window.FindElement('_LISTA_').Update(values = palabras_lista)
		
		if event in ('dirs_1','dirs_2','dirs_3','dirs_4','dirs_8'):

			window.Element(event).Update(button_color=('#EFF0D1', '#262730'))
			lista_dirs = ['dirs_1','dirs_2','dirs_3','dirs_4','dirs_8']
			lista_dirs.remove(event)
			for x in lista_dirs:
				window.Element(x).Update(button_color = color_boton_por_defecto)
			
			orientacion = event
			
		if event == '_ACEPTAR_':
			config_dicc['palabras'] = palabras_dicc
			config_dicc['ayuda'] = "sin ayuda" if val['sin'] else "definiciones" if val['defin'] else "palabras" 
			config_dicc['orientacion'] = orientacion
			config_dicc['mayuscula'] = val['mayus']
			config_dicc['fuente'] = val['_FONT_']
			for key in config_dicc:
				print(key, '=',config_dicc[key])
			break
		
		if event == '_LISTA_':
			print (val['_LISTA_'])
		# ~ if event in ('mayus','minus'): #quizas sirve para no ingresar info erronea
		# los radio si no tienen valor por defecto son False
			# ~ print('mayus =', val['mayus'])
			# ~ window.FindElement('_ACEPTAR_').Update(disabled = False)
	window.Close()
	with open(nombre_archivo_config, 'w', encoding = 'utf-8') as f:
		json.dump(config_dicc, f, ensure_ascii = False)

if __name__ == "__main__":
	configuracion()



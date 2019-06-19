import PySimpleGUI as sg
import random
import string
import json
import os
import datetime
from buscar_en_wiktionary import buscar_en_wiktionary

nombre_archivo_config = 'configuracion.json'
nombre_archivo_reporte = 'reporte_de_errores.txt'

def reporte(r,error):
	hora = datetime.datetime.now()
	hora = str(hora)[:-10]
	
	if error == 1:
		texto = '[{}]{}: Wiktionario la clasificó como "{}"y pattern como "{}".'.format(hora,r['palabra'],r['clasificacion_wiktionario'],r['clasificacion_pattern'])
	
	elif error ==2:
		texto = '[{}] El termino "{}": no se encontró en ningun motor de busqueda.'.format(hora,r['palabra'])

	print('Error {}:{}'.format(error,texto))
	
	existe = os.path.isfile(nombre_archivo_reporte)
	if existe:
		f = open(nombre_archivo_reporte, 'a')
	else:
		f = open(nombre_archivo_reporte, 'w')
		print('Se ha creado un reporte de errores en',nombre_archivo)
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
			definicion = input('No se encontro la palabra en Wiktionario.\nDefínala:\n') #Aca habría que hacer un popup
	elif resultado['clasificacion_pattern'] == '_Ninguna_': # Las dos None
		print('Reportando Error 2...')
		reporte(resultado,2)
		#no incluir palabra
		clasificacion_definitiva = '_no_aceptada_'
		definicion = '_no_aceptada_'
	# ~ definicion = 'Esto es una def de prueba, cuando ande quitar eta linea'###############################
	
	return clasificacion_definitiva, definicion
	
def cargar_configuracion():
	existe = os.path.isfile(nombre_archivo_config)
	if existe:
		with open(nombre_archivo_config, 'r') as f:
			config_dicc = json.load(f)
		# ~ print('Configuracion guardada:')
		# ~ print(json.dumps(config_dicc, sort_keys=True, indent=4))
		palabras_dicc = config_dicc['palabras']
	else:
		config_dicc = {}
		config_dicc['palabras'] = []
		palabras_dicc = {}
		print('no existe archivo de configuracion')
	palabras_lista = list(palabras_dicc.keys())
	return config_dicc,palabras_dicc,palabras_lista
	
def configuracion():
	config_dicc, palabras_dicc, palabras_lista = cargar_configuracion()
	print (palabras_dicc)

	menu = ['Menu', ['Definicion::_MENU_', 'Eliminar::_MENU_']]
	# ~ menu_adj = ['Menu', ['Definicion::_MENU_', 'Eliminar::_MENU_']]
	# ~ menu_verb = ['Menu', ['Definicion::_MENU_', 'Eliminar::_MENU_']]
	# print(config_dicc['palabras'])
	layout = [
			 [sg.Frame( layout = [[sg.Radio('Sustantivo', "RADIOp",default = True,key='_esSus_'),
								 sg.Radio('Adjetivo', "RADIOp",key='_esAdj_'),
								sg.Radio('Verbo', "RADIOp",key='_esVer_')],
					 
			[sg.Input(key='_IN_', do_not_clear=False)],
			[sg.Button('Agregar', bind_return_key=True, key='_ADD_')],
			
			[sg.Listbox(values=palabras_lista, default_values=None, enable_events=True, size=(43,6),
									key='_LISTA_', tooltip=None, right_click_menu= menu, visible=True)]],
			 # ~ sg.Listbox(values=palabras_lista, default_values=None, enable_events=True, size=(12,6),
									# ~ key='_LISTA_', tooltip=None, right_click_menu= menu_adj, visible=True),
			 # ~ sg.Listbox(values=palabras_lista, default_values=None, enable_events=True, size=(12,6),
									# ~ key='_LISTA_', tooltip=None, right_click_menu= menu_verb, visible=True)]],
								  title= 'Insertar Palabra')],
									
									
			[sg.Frame( layout = [[sg.Text('Sustantivos'),sg.Input(size = (2,1), key='_CANT_S_'),
								  sg.Text('Adjetivos'),sg.Input(size = (2,1), key='_CANT_A_'),
								  sg.Text('Verbos'),sg.Input(size = (2,1), key='_CANT_V_')]],
								 title= 'Cantidad de palabras con las que hacer la sopa')],
			
			[sg.Frame( layout = [[sg.Radio('Sin ayuda', "RADIOA", key= 'sin', size=(10,1)),
								  sg.Radio('Definiciones', "RADIOA", key='defin'),
								  sg.Radio('Mostrar palabras', "RADIOA", default = True, key='pal')]],
								  title= 'Ayudas')],
			
			[sg.Frame( layout = [[sg.Radio('Horizontal', "RADIOH",default = True, key='hor', size=(10,1)),
								  sg.Radio('Vertical', "RADIOH", key='ver'), sg.Radio('Mixto', "RADIOH", key='mix')]],
								  title= 'Orientación')],
			
			[sg.Frame( layout = [[sg.Radio('Mayúscula', "RADIOn", key='mayus', size=(10,1)),
							      sg.Radio('Minúscula', "RADIOn", default = True, key='minus')]],
								  title= 'Mayúscula/Minúscula')],
			
			[sg.Frame( layout = [[sg.InputCombo(('Arial','Courier','Comic','Fixedsys','Times','Verdana','Helvetica'), key='_FONT_')]],
								  title= 'Fuente')],
			
			# ~ [sg.Text('Oficina')],
			[sg.Button('Guardar Configuracion', key='_ACEPTAR_', disabled = False),sg.Button('Cerrar')]
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
			categoria = 'adj' if val['_esAdj_'] else 'verb' if val['_esVer_'] else 'sust'
			definicion = ''
			
			_, definicion = analizarpalabra(palabra,categoria) #tiro la categoria que me da a _ porque todavia no anda
			
			if palabra != '' and definicion != '_no_aceptada_': # no la agrego si es vacía o no tiene definicion
				palabras_dicc[palabra] = {'tipo': categoria,'def': definicion}
				palabras_lista = window.FindElement('_LISTA_').GetListValues()
				palabras_lista.append(palabra)  #aca cargo y agrego a la lista, pordría agregar directamente porque ya defini la lista en la importacion.
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
			
		if event == '_ACEPTAR_':
			config_dicc['palabras'] = palabras_dicc
			config_dicc['ayuda'] = "sin ayuda" if val['sin'] else "definiciones" if val['defin'] else "palabras" 
			config_dicc['orientacion'] = "horizontal" if val['hor'] else "vertical" if val['ver'] else "mixto"
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
	with open(nombre_archivo_config, 'w') as f:
		json.dump(config_dicc, f)

if __name__ == "__main__":
	configuracion()


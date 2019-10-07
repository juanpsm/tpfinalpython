# -*- coding: utf-8 -*-
#
# Algoritmo inspirado en:
#
# https://rosettacode.org/wiki/Word_search#Python
#
from random import shuffle, randint
import config
import string
import random

config_dicc,palabras_dicc,_ = config.cargar_configuracion()
#diccionario con direcciones para la orientacion de las palabras en sopa.
dirs = [[1, 0], [0, 1], [1, 1], [1, -1], [-1, 0], [0, -1], [-1, -1], [-1, 1]]
n_filas =  10
n_columnas = n_filas
tam_grilla = n_filas * n_columnas
min_pal = 10
char_vacío = '*'


class Grilla:
	def __init__(self):
		self.n_intentos = 0
		self.celdas = [[{'key':str(j)+'_'+str(i),'tipo': None, 'marcada':False,'color':None, 'letra':char_vacío} for i in range(n_columnas)] for j in range(n_filas)]
		self.soluciones = []

def modifglob(palabras):
	global config_dicc
	global palabras_dicc
	config_dicc,palabras_dicc,_ = config.cargar_configuracion()
	global dirs
	print ('Dirs', dirs)
	print( 'config_dicc ->', config_dicc['orientacion'] )
	if config_dicc['orientacion'] == 'dirs_0':
		dirs = [[1,0]]
	if config_dicc['orientacion'] == 'dirs_1':
		dirs = [[0,1]]
	elif config_dicc['orientacion'] == 'dirs_2':
		dirs = [[1, 0], [0, 1]]
	elif config_dicc['orientacion'] == 'dirs_3':
		dirs = [[1, 0], [0, 1], [1, 1]]
	elif config_dicc['orientacion'] == 'dirs_4':
		dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
	elif config_dicc['orientacion'] == 'dirs_8':
		dirs = [[1, 0], [0, 1], [1, 1], [1, -1], [-1, 0], [0, -1], [-1, -1], [-1, 1]]
	global n_filas
	n_filas =  max(len(max(palabras, key=len)),len(palabras))
	global n_columnas
	n_columnas = n_filas
	global tam_grilla
	tam_grilla = n_filas * n_columnas
	global min_pal
	min_pal = len(palabras)

def clasificar_palabra(pal):
	return palabras_dicc[pal]['tipo']

def probar_pos(grilla, pal, direccion, pos):
	f = pos // n_columnas
	c = pos % n_columnas
	largo_pal = len(pal)

	# chequea bordes
	if (dirs[direccion][0] == 1 and (largo_pal + c) > n_columnas) or \
	   (dirs[direccion][0] == -1 and (largo_pal - 1) > c) or \
	   (dirs[direccion][1] == 1 and (largo_pal + f) > n_filas) or \
	   (dirs[direccion][1] == -1 and (largo_pal - 1) > f):
		return 0

	f_ = f
	c_ = c
	i = 0
	superp = 0

	# chequea celdas
	while i < largo_pal:
		if grilla.celdas[f_][c_]['letra'] != char_vacío and grilla.celdas[f_][c_]['letra'] != pal[i]:
			return 0 # si no es vacía y la letra que esta no coincide con la que voy a poner, no es valida la posicion.
		c_ += dirs[direccion][0] # mientras no pasa lo de arriba, continuamos moviendonos en la direccion dada.
		f_ += dirs[direccion][1]
		i += 1

	f_ = f
	c_ = c
	i = 0
	# si todo esto fue bien, quiere decir que puedo poner la palabra
	while i < largo_pal:
		if grilla.celdas[f_][c_]['letra'] == pal[i]: # Si la casilla donde voy a ubicarmetiene la letra que quiero ubicar
			superp += 1  # cuento letras superpuestas
			grilla.celdas[f_][c_]['tipo'] = 'MIXTO' # El casillero pordrá ser pintado con mas de un color
		else:
			if config_dicc['mayuscula']:
				grilla.celdas[f_][c_]['letra'] = pal[i].upper()
			else:
				grilla.celdas[f_][c_]['letra'] = pal[i]	
			grilla.celdas[f_][c_]['tipo'] = clasificar_palabra(pal)
		if i < largo_pal - 1:
			c_ += dirs[direccion][0]
			f_ += dirs[direccion][1]

		i += 1

	letras_puestas = largo_pal - superp
	if letras_puestas > 0:
		grilla.soluciones.append("{0:<10} ({1},{2})({3},{4})".format(pal, c, f, c_, f_))

	return letras_puestas

def probar_palabra(grilla, pal):
	rand_dir = randint(0, len(dirs))
	rand_pos = randint(0, tam_grilla)
	for d in range(0, len(dirs)):
		d = (d + rand_dir) % len(dirs)
		for pos in range(0, tam_grilla):
			pos = (pos + rand_pos) % tam_grilla
			letras_puestas = probar_pos(grilla, pal, d, pos)
			if letras_puestas > 0:
				return letras_puestas

	return 0

def crear_grilla(palabras):
	print('Recibo palabras en crear_grilla()',palabras)
	config_dicc, _, _ = config.cargar_configuracion()
	if config_dicc != {}:
		print('Cargo en crear_grilla()',config_dicc['orientacion'])
	#print('antes de modifglob(), dirs =',dirs)
	modifglob(palabras)
	#print('luego de modifglob(), dirs =',dirs)
	grilla = None
	nun_intentos = 0

	print('Filas:',n_filas,'Col:',n_columnas,'Tam:',tam_grilla,'len:',min_pal)

	while nun_intentos < 10000:
		nun_intentos += 1
		shuffle(palabras)
		grilla = Grilla()
		celdas_llenas = 0
		for pal in palabras:
			celdas_llenas += probar_palabra(grilla, pal)
		if len(grilla.soluciones) == len(palabras):
			grilla.n_intentos = nun_intentos
			
			#por ultimo lleno los casilleros vacios
			for i in range(n_columnas):
				for j in range(n_filas):
					
					if grilla.celdas[j][i]['letra'] == char_vacío:
						grilla.celdas[j][i]['letra'] = random.choice(string.ascii_lowercase)
						
					if config_dicc['mayuscula']:
						grilla.celdas[j][i]['letra'] = grilla.celdas[j][i]['letra'].upper()
					else:
						grilla.celdas[j][i]['letra'] = grilla.celdas[j][i]['letra'].lower()
						
			return grilla
		else:
			print('No se pudo crear, reintentos =',nun_intentos)

	return grilla

def print_resultado(grilla):
	if grilla is None or grilla.n_intentos == 0:
		print("No fue posible producir la grilla")
		return
	
	print(grilla.celdas)
	
	size = len(grilla.soluciones)

	print("Intentos: {0}".format(grilla.n_intentos))
	print("Nummero de palabras: {0}".format(size))

	print("\n      0  1  2  3  4  5  6  7  8  9\n")
	for r in range(0, n_filas):
		print(" {0}   ".format(r), end='')
		for c in range(0, n_columnas):
			print(" %c " % grilla.celdas[r][c]['letra'], end='')
		print()
	print()

	for i in range(0, size - 1, 2):
		print("{0}   {1}".format(grilla.soluciones[i], grilla.soluciones[i+1]))

	if size % 2 == 1:
		print(grilla.soluciones[size - 1])


if __name__ == "__main__":
	config_dicc, palabras_dicc, _ = config.cargar_configuracion()

	palabras = config.obtener_lista_palabras(config_dicc)
	if palabras != []:
		print(palabras)
		print_resultado(crear_grilla(palabras))

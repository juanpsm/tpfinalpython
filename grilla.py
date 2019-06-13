import re
from random import shuffle, randint

vector_config = {'mayus':False}
palabras_docente = {'careta':{'tipo':'adj','def':''},'sucio':{'tipo':'adj','def':''},'apestoso':{'tipo':'adj','def':''},
					'correr':{'tipo':'verb','def':''},'economizar':{'tipo':'verb','def':''},'cancherear':{'tipo':'verb','def':''},
					'rayuela':{'tipo':'sus','def':''},'perro':{'tipo':'sus','def':''},'gato':{'tipo':'sus','def':''}}

palabras = list(palabras_docente.keys())
print (max(palabras, key=len))
#dirs = [[1, 0], [0, 1], [1, 1], [1, -1], [-1, 0], [0, -1], [-1, -1], [-1, 1]]
dirs = [[1,0]]
n_filas =  max(len(max(palabras, key=len)),2*len(palabras))
n_columnas = n_filas
tam_grilla = n_filas * n_columnas
min_pal = len(palabras)
char_vacío = '*'


class Grilla:
	def __init__(self):
		self.n_intentos = 0
		self.celdas = [[{'key':str(j)+'_'+str(i),'tipo': None, 'marcada':False, 'letra':char_vacío} for i in range(n_columnas)] for j in range(n_filas)]
		self.soluciones = []

def clasificar_palabra(pal):
	return palabras_docente[pal]['tipo']

def leer_palabras(filename):

	palabras = []
	with open(filename, "r") as file:
		for linea in file:
			if vector_config['mayus']:
				s = linea.strip().upper()
			else:
				s = linea.strip().lower()
			palabras.append(s)
	return palabras

def poner_msg(grilla, msg):
    msg = re.sub(r'[^A-Z]', "", msg.upper())

    msg_len = len(msg)
    if 0 < msg_len < tam_grilla:
        gap_size = tam_grilla // msg_len

        for i in range(0, msg_len):
            pos = i * gap_size + randint(0, gap_size)
            grilla.celdas[pos // n_columnas][pos % n_columnas]['letra'] = msg[i]

        return msg_len

    return 0

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
		if grilla.celdas[f_][c_]['letra'] == pal[i]:
			superp += 1  # cuento letras superpuestas
		else:
			grilla.celdas[f_][c_]['letra'] = pal[i]
		grilla.celdas[f_][c_]['marcada'] = True
		grilla.celdas[f_][c_]['tipo'] = clasificar_palabra(pal)

		if i < largo_pal - 1:
			c_ += dirs[direccion][0]
			f_ += dirs[direccion][1]

		i += 1

	letras_puestas = largo_pal - superp
	if letras_puestas > 0:
		print('solucion ->',"{0:<10} ({1},{2})({3},{4})".format(pal, c, f, c_, f_))
		grilla.soluciones.append("{0:<10} ({1},{2})({3},{4})".format(pal, c, f, c_, f_))

	return letras_puestas


def probar_palabra(grilla, pal):
	rand_dir = randint(0, len(dirs))
	rand_pos = randint(0, tam_grilla)
	print('probar en :','dir',rand_dir,'pos',rand_pos)
	for d in range(0, len(dirs)):
		d = (d + rand_dir) % len(dirs)

		for pos in range(0, tam_grilla):
			pos = (pos + rand_pos) % tam_grilla

			letras_puestas = probar_pos(grilla, pal, d, pos)
			if letras_puestas > 0:
				print('letraspuestas:',letras_puestas)
				return letras_puestas

	return 0


def crear_grilla_llena(palabras, msg = ''):
	grilla = None
	nun_intentos = 0

	while nun_intentos < 100:
		nun_intentos += 1
		shuffle(palabras)

		grilla = Grilla()
		msg_len = poner_msg(grilla, msg)
		target = tam_grilla - msg_len

		celdas_llenas = 0
		for pal in palabras:
			celdas_llenas += probar_palabra(grilla, pal)
			if celdas_llenas == target:
				if len(grilla.soluciones) >= min_pal:
					grilla.n_intentos = nun_intentos
					return grilla
				else:
					break # grid is full but we didn't pack enough words, start over

	return grilla


def crear_grilla(palabras):
	grilla = None
	nun_intentos = 0

	print(n_filas,n_columnas,tam_grilla,min_pal)
	while nun_intentos < 100:
		nun_intentos += 1
		shuffle(palabras)
		print('pal shufle',palabras)
		
		grilla = Grilla()

		celdas_llenas = 0
		for pal in palabras:
			print('probar_palabra',pal)
			celdas_llenas += probar_palabra(grilla, pal)
			print ('len sol >>>>>>>>>>>>>>',len(grilla.soluciones))
		if len(grilla.soluciones) == len(palabras):
			grilla.n_intentos = nun_intentos
			return grilla
		else:
			print('full')
			break # grid is full but we didn't pack enough words, start over

	return grilla


def print_resultado(grilla):
	if grilla is None or grilla.n_intentos == 0:
		print("No fue posible producir la grilla")
		return

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
	# print_resultado(crear_grilla_llena(leer_palabras("unixdict.txt"),'el pequeño saltamontes'))
	palabras = list(palabras_docente.keys())
	print(palabras)
	print_resultado(crear_grilla(palabras))

import time
import random
import os
import json
from pprint import pprint
import datetime 

nombre_archivo_registro = 'registros_temp_hum.json'
def guardar_datos(of, temp, hum):
	existe = os.path.isfile(nombre_archivo_registro)
	if existe:
		with open(nombre_archivo_registro, 'r', encoding = 'utf-8') as f:
			dicc = json.load(f)
	else:
		dicc = {}
		print('Registro creado')
	
	string_time = time.strftime("%Y/%m/%d - %H:%M:%S", time.localtime(time.time()))

	try: 
		dicc[of].append({'time':string_time,'temp':temp,'hum':hum})
	except KeyError:
		dicc[of] = [{'time':string_time,'temp':temp,'hum':hum}]
	pprint(dicc)
	#print('Ultimo: ',dicc[of][-1:])

	with open(nombre_archivo_registro, 'w', encoding = 'utf-8') as f:
		json.dump(dicc, f, ensure_ascii = False)

def crear_registro(n,m):
	'''Crea m registros aleatorios de n oficinas'''
	for of in range(1,n+1):
		for _ in range(m):
			guardar_datos(str(of), random.randint(-10,50), random.randint(0,100))

if __name__ == "__main__":
	crear_registro(16,5)
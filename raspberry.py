#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from itertools import repeat
from luma.core import legacy

### MATRIZ
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT,TINY_FONT, SINCLAIR_FONT, LCD_FONT
####
#para emular
from demo_opts import get_device

class Matriz:
	def __init__(self, numero_matrices = 1, orientacion = 0, rotacion = 0, ancho = 8, alto = 8):
		self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
		self.serial = spi(port=0, device=0, gpio=noop())
		self.device = max7219(self.serial, width = ancho, height = alto, cascaded = numero_matrices, rotate = rotacion)
	def mostrar_mensaje(self, msg, delay=0.1, font=1):
		show_message(self.device, msg, fill = 'white', font = proportional(self.font[font]), scroll_delay=delay)

def iniciar_sensores():
### SENSORES
    import Adafruit_DHT
    class Temperatura:
            def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
                    # Usamos el DHT11 que es compatible con el DHT12
                    # en caso de usar el 22 Adafruit_DHT.DHT22
                    self._sensor = sensor
                    self._data_pin = pin

            def datos_sensor(self):
                    humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
                    return {'temperatura': temperatura, 'humedad': humedad}

### MIC
    import RPi.GPIO as GPIO
    class Sonido:
            def __init__(self, canal=22):
                    self._canal = canal
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(self._canal, GPIO.IN)
                    # Desactivo las warnings por tener más de un circuito en la GPIO
                    GPIO.setwarnings(False)
                    GPIO.add_event_detect(self._canal, GPIO.RISING)

            def evento_detectado(self, funcion):
                    if GPIO.event_detected(self._canal):
                            funcion()

def asd():
		#~ eyes_open = [
		#~ [[
			#~ 0x00, 0x7e, 0x81, 0xb1, 0xb1, 0x81, 0x7e, 0x00
		#~ ]],
		#~ [[
			#~ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
		#~ ]],
		#~ [[
			#~ 0x00, 0x78, 0x84, 0xb4, 0xb4, 0x84, 0x78, 0x00
		#~ ]],
		#~ [[
			#~ 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
		#~ ]],
		#~ [[
			#~ 0x00, 0x20, 0x50, 0x70, 0x70, 0x50, 0x20, 0x00
		#~ ]],
		#~ [[
			#~ 0x00, 0x20, 0x60, 0x60, 0x60, 0x60, 0x20, 0x00
		#~ ]]
	#~ ]
	
	
	#~ with canvas(device) as draw:
	#~ frame_ = 1
	#for i in range(0,5):
		#print("\\"+str(i))
		#legacy.text(draw, (0, 0), "\\"+str(i), fill="white", font=eyes_open)
		#time.sleep(frame_)
	#~ legacy.text(draw, (0, 0), "\0",font=eyes_open[0])
	#~ time.sleep(frame_) 
	#~ legacy.text(draw, (0, 0), "\0", font=eyes_open[1])
	#~ time.sleep(frame_)
	#~ legacy.text(draw, (0, 0), "\0", font=eyes_open[2])
	#~ time.sleep(frame_)
	#~ legacy.text(draw, (0, 0), "\0", font=eyes_open[3])
	#~ time.sleep(frame_)
	#~ legacy.text(draw, (0, 0), "\0", font=eyes_open[4])
	#~ time.sleep(frame_)
	#~ legacy.text(draw, (0, 0), "\0", font=eyes_open[5])
	#~ time.sleep(5)
	# draw.rectangle(device.bounding_box, outline="white", fill="black")
	
	#            for _ in repeat(None):
#                time.sleep(1)
#                msg = time.asctime()
#                msg = time.strftime("%S")
#                
#                with canvas(device) as draw:
#                    draw.rectangle(device.bounding_box, outline="white", fill="black")
#                    text(draw, (1, 0), msg, fill="white")
#            time.sleep(5)
#    pass
	v =0

def show(emu = False):
	if emu: #para emular pido el device
		device = get_device()
		datos = {'temperatura':34, 'humedad':89}
	else:
		#Inicializar la matriz: identificar puerto
		serial = spi(port = 0, device = 0, gpio = noop())
		#crear una insctancia del objeto
		device = max7219(serial, cascaded = 2, block_orientation = 0)

		#leer temperatura y humedad del sensor
		tmp = Temperatura()
		datos = tmp.datos_sensor()
		print('Temperatura = {0:0.1f°}C Humedad = {1:0.1f} %'.format(datos['temperatura'], datos['humedad']))
	
	##################   realizar las conversiones necesarias
	temp = datos['temperatura']
	hum = datos['humedad']
	
	of = input('Ingrese Nº Oficina: ')
	msg = "Oficina "+of
	print(msg)
	show_message(device, msg, fill='white', font=proportional(LCD_FONT), scroll_delay=0.05)
	
	
	msg = 'Temperatura'
	show_message(device, msg, fill='white', font=proportional(LCD_FONT), scroll_delay=0.05)
	msg = str(temp)+'º C'
	with canvas(device) as draw:
		text(draw, (1, 0), msg, fill="white")
	time.sleep(3)
	msg = 'Humedad'
	show_message(device, msg, fill='white', font=proportional(LCD_FONT), scroll_delay=0.05)
	msg = str(hum)+'%'
	with canvas(device) as draw:
		text(draw, (1, 0), msg, fill="white")
	time.sleep(3)
	
	msg = 'Bye!'
	show_message(device, msg, fill='white', font=proportional(LCD_FONT), scroll_delay=0.05)

def main():
	emu = input('Está emulando? (y or n): ').lower() in ('s','y','si','yes')
	#emu = True
	if emu:
		show(emu)
	else:
		iniciar_sensores()
		sonido = Sonido()
		while True:
			time.sleep(0.0001)
			sonido.evento_detectado(show)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass #no hacer nada

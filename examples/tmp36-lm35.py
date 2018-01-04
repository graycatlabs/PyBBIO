"""
 tmp36-lm35.py
 Alaa Agwa - 3/2014

 Example program for PyBBIO's TMP36LM35 library.
 Reads the temerature from the TMP36 or LM35 sensors from analog pin.

 This example program is in the public domain.
"""
from bbio import *
from TMP36LM35 import *

data_pin = GPIO1_15  # P8.15

sensor = TMP36LM35(data_pin)

def setup():
	pass

def loop():
	temp = sensor.readTempC()
	if (not temp):
    	# The sensor reported an error.
    	print "Error reading the sensor value"
  	else:
    	print "Temp: %0.2f C" % temp

	delay(1000)

run(setup,loop)

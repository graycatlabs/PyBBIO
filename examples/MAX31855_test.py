"""
 MAX31855_test.py 
 Alexander Hiam - 12/2012
 Updated Oct. 2015
 
 Example program for PyBBIO's MAX31855 library.
 Reads the temperature from a MAX31855 thermocouple amplifier connected
 over SPI.
 
 This example program is in the public domain.
"""

from bbio import *
from bbio.libraries.MAX31855 import MAX31855

# Open SPI bus 1:
SPI1.open()

# Using SPI1 CS0 (P9_28):
cs_pin = 0

# Create an instance of the MAX31855 class:
thermocouple = MAX31855(SPI1, cs_pin)

def setup():
  # Nothing to do here...
  pass

def loop():
  temp = thermocouple.readTempC()
  if (temp == None):
    # The MAX31855 reported an error, print it:
    if thermocouple.error == thermocouple.OPEN_CIRCUIT:
      print "Thermocouple not connected"

    elif thermocouple.error == thermocouple.SHORT_TO_GND:
      print "Thermocouple shorted to GND"

    elif thermocouple.error == thermocouple.SHORT_TO_VCC:
      print "Thermocouple shorted to VCC"

  else:
    print "Temp: {:0.2f} C".format(temp)
  delay(1000)

run(setup, loop)

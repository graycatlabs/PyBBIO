"""
 MAX31855_test.py 
 Alexander Hiam - 12/2012
 
 Example program for PyBBIO's MAX31855 library.
 Reads the temerature from the MAX31855 thermocouple
 amplifier using software SPI.
 
 This example program is in the public domain.
"""

from bbio import *
from MAX31855 import *

# Set variables for the pins connected to the ADC:
data_pin = GPIO1_15  # P8.15
clk_pin  = GPIO1_14  # P8.16
cs_pin   = GPIO0_27  # P8.17

# Create an instance of the MAX31855 class:
thermocouple = MAX31855(data_pin, clk_pin, cs_pin)

def setup():
  # Nothing to do here, the MAX31855 class sets pin modes
  pass

def loop():
  temp = thermocouple.readTempC()
  if (not temp):
    # The MAX31855 reported an error, print it:
    print thermocouple.error
  else:
    print "Temp: %0.2f C" % temp;
  delay(1000)

run(setup, loop)

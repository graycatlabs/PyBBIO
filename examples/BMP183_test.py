"""
 BMP183_test.py 
 Alexander Hiam <alex@graycat.io> 
 
 An example to demonstrate the use of the BMP183 library included 
 with PyBBIO. Interfaces with the BMP183 SPI pressure sensor to 
 measure the atmospheric pressure and ambient temperature.
 
 This example program is in the public domain.
"""

from bbio import *
# Import the BMP183 class from the BMP183 library:
from bbio.libraries.BMP183 import BMP183

# Create a new instance of the BMP183 class using SPI0 with the
# default CS0 chip select pin:
bmp = BMP183(SPI0)

def setup():
  # The BMP183 is initialized when the BMP183 class is instantiated,
  # so there's nothing to do here
  pass

def loop():
  # Get the current temperature in Celsius:
  temp = bmp.getTemp()
  # Get the current pressure in Pascals:
  pressure = bmp.getPressure()

  print "\ntemperature : %0.2f C" % temp
  print "pressure    : %i Pa" % pressure

  delay(5000)

run(setup, loop)
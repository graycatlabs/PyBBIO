"""
 HTU21D_test.py 
 Alexander Hiam <alex@graycat.io> 
 
 An example to demonstrate the use of the HTU21D library included 
 with PyBBIO. Interfaces with the HTU21D I2C relative humidity sensor.
 
 This example program is in the public domain.
"""

from bbio import *
# Import the HTU21D class from the HTU21D library:
from bbio.libraries.HTU21D import HTU21D

# Initialize I2C bus:
I2C2.open() 
# Create a new instance of the HTU21D class using the I2C2 I2C bus
htu = HTU21D(I2C2)

def setup():
  # The HTU21D is initialized when the HTU21D class is instantiated,
  # so there's nothing to do here
  pass

def loop():
  # Read the current relative humidity:
  rh = htu.getHumidity()
  # Read the current ambient temperature:
  temp = htu.getTemp()
  # Calculate the current dew point:
  dew_point = htu.calculateDewPoint(rh, temp)

  print "\nrelative humidity : %0.2f %%" % rh
  print "temperature       : %0.2f C" % temp
  print "dew point         : %0.2f C" % dew_point

  delay(2000)

run(setup, loop)
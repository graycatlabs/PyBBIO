"""
 ADXL345_test.py 
 Alexander Hiam <alex@graycat.io> 
 
 An example to demonstrate the use of the ADXL345 library included 
 with PyBBIO. Interfaces with the ADXL345 3-axis I2C or SPI accelerometer.
 
 This example program is in the public domain.
"""

from bbio import *
# Import the ADXL345 class from the ADXL345 library:
from bbio.libraries.ADXL345 import ADXL345

# To use the ADXL345 in I2C mode the SPI CS pin needs to be held high.
# To ensure CS is high, it can either be wired to 3.3V, or it can be
# wired to a GPIO pin and the pin set high:
CS_GPIO = GPIO3_17
pinMode(CS_GPIO, OUTPUT)
digitalWrite(CS_GPIO, HIGH)
# After setting CS high, wait a bit to give the ADXL345 time to boot:
delay(100)

# Initialize the I2C port the ADXL345 is attached to:
I2C2.open()
# Initialize the ADXL345:
accel = ADXL345(I2C2)

def setup():
  # The default range is +/-2 G, set to +/-8 G: 
  accel.setRange(accel.RANGE_8G)

def loop():
  x, y, z = accel.getXYZ()
  print "{:+0.2f}G  {:+0.2f}G  {:+0.2f}G".format(x, y, z)
  delay(100)

run(setup, loop)
"""
 ADS786x_test.py 
 Alexander Hiam - 12/2012
 
 Example program for PyBBIO's ADS786x library.

 This example program is in the public domain.
"""

from bbio import *
from ADS786x import *

# Set variables for the pins connected to the ADC:
data_pin = GPIO1_15  # P8.15
clk_pin  = GPIO1_14  # P8.16
cs_pin   = GPIO0_27  # P8.17

# Create an instance of the ADC class:
adc = ADS7866(data_pin, clk_pin, cs_pin)

def setup():
  # Nothing to do here, the ADS786x class sets pin modes
  pass

def loop():
  # Read the voltage and print it to the terminal:
  voltage = adc.readVolts()
  print "%0.3f V" % voltage
  delay(1000)


run(setup, loop)

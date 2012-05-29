# analog_test.py - Alexander Hiam
# Testing analogRead() 
#
# Example circuit:
#  -Connect two equal value resistors around 10k ohm in series
#   between the 3.3v supply (pin 3 on P9) and GND (pin 2 on P9) 
#   to form a voltage divider. Where the two resistors connect 
#   will be near 1.8v (confirm with a voltmeter if available).
#
#  -Connect two potentiometers so that each has one of its outer 
#   pins connected to GND and the other two the 1.8v of the 
#   voltage divider. Connect the center pin of one to AIN0 (pin 
#   39 on P9) and the other to AIN2 (pin 37 on P9). 
#
#  -Run this program and watch the output as you turn the pots.
#
# *** NOTICE *** 
# The maximum ADC input voltage is 1.8v,
# applying greater voltages will likely cause
# permanent damage to the ADC module! 
#
# This example is in the public domain
 

# Import PyBBIO library:
from bbio import *

pot1 = AIN0 # pin 39 on header P9 
pot2 = AIN2 # pin 37 on header P9 

def setup():
  # Nothing to do here
  pass

def loop():
  val1 = analogRead(pot1)
  val2 = analogRead(pot2)
  # ADC reference voltage is 1.8v, and it is a 
  # 12-bit ADC, so to get volts per step:
  volts_per_step = 1.8 / 2.0**12
  # Multiply ADC value by volts/step to get voltage:
  voltage1 = val1 * volts_per_step
  voltage2 = val2 * volts_per_step
  print " pot1 ADC value: %i - voltage: %fv" % (val1, voltage1)
  print " pot2 ADC value: %i - voltage: %fv\n" % (val2, voltage2)
  delay(500)

# Start the loop:
run(setup, loop)

# analog_test.py - Alexander Hiam
# Testing analogRead()
#
# *** NOTICE *** 
# The maximum ADC input voltage is 1.8v,
# applying greater voltages will likely cause
# permanent damage to the ADC module! 
 
# Import PyBBIO library:
from bbio import *

# Analog input pin - A0 is pin 39 on header P9 
ain = A0

# Create a setup function:
def setup():
  # Nothing to do here
  pass

# Create a main function:
def main():
  adc_value = analogRead(ain)
  # ADC reference voltage is 1.8v, and it is a 
  # 12-bit ADC, so to get volts per step:
  volts_per_step = 1.8 / 2.0**12
  # Multiply ADC value by volts/step to get voltage:
  voltage = adc_value * volts_per_step
  print "%fv" % voltage
  delay(500)

# Start the loop:
run(setup, main)

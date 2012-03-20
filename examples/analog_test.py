# analog_test.py - Alexander Hiam
# Testing analogRead()

# Import PyBBIO library:
from bbio import *

# Create a setup function:
def setup():
  # Nothing to do here
  pass

# Create a main function:
def main():
  adc_value = analogRead(VSYS)
  voltage = adc_value * (1.8/2.0**12)
  print "%f v" % voltage
  sleep(0.5)

# Start the loop:
run(setup, main)

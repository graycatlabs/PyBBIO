# available_pins.py - Alexander Hiam
# Prints all the pins available for IO expansion by their 
# names used in PyBBIO (refer to beaglebone schematic for
# header locations).
#
# This example is in the public domain

# Import PyBBIO library:
from bbio import *

# Create a setup function:
def setup():
  print "\n GPIO pins:" 
  for i in GPIO.keys(): 
    print "   %s" % i
  print "\n ADC pins:" 
  for i in ADC.keys():
    print "   %s" % i

# Create a main function:
def loop():
  # No need to keep running
  stop()

# Start the loop:
run(setup, loop)


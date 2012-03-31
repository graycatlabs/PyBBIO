# blink.py - Alexander Hiam - 2/2012
# Blinks two of the Beagleboard's on-board LEDs until CTRL-C is pressed.
#
# This example is in the public domain

# Import PyBBIO library:
from bbio import *

# Create a setup function:
def setup():
  # Set the two LEDs as outputs: 
  pinMode(USR2, OUTPUT)
  pinMode(USR3, OUTPUT)

  # Start one high and one low:
  digitalWrite(USR2, HIGH)
  digitalWrite(USR3, LOW)

# Create a main function:
def loop():
  # Toggle the two LEDs and sleep a few seconds:
  toggle(USR2)
  toggle(USR3)
  delay(500)

# Start the loop:
run(setup, loop)

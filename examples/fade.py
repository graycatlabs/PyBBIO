# fade.py - Alexander Hiam - 10/2012
# Uses pulse width modulation to fade an LED on PWM1A 
# (pin 14 on header P9). 
#
# This example is in the public domain

# Import PyBBIO library:
from bbio import *

LED = PWM1A 
brightness = 0  # Global variable to store brightness level
inc = 1         # How much to increment the brightness by
pause = 10      # Delay in ms between each step 

# Create a setup function:
def setup():
  # nothing to do here
  pass

# Create a main function:
def loop():
  global brightness, inc

  # Set the PWM duty cycle:
  analogWrite(LED, brightness)
  # Increment value:
  brightness += inc
  if ((brightness == 255) or (brightness == 0)):
    # Change increment direction:
    inc *= -1
  # Sleep a bit:
  delay(pause)

# Start the loop:
run(setup, loop)

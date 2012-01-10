# digitalRead.py - Alexander Hiam - 1/2012
# USR3 LED mirrors GPIO1_6.

import time

# Must 'import *' to get all the needed constants,
# simply importing bbio won't do:
from bbio import *

# Create a BeagleBoard instance:
bb = BeagleBone()
# Set the two LEDs as outputs:
bb.pinMode(USR3, OUTPUT)
bb.pinMode(GPIO1_6, INPUT)

# Main loop:
while(1):
  state = bb.digitalRead(GPIO1_6)
  bb.digitalWrite(USR3, state)
  # It's good to put a bit of a delay in infinite loops 
  # to keep the CPU happy:
  time.sleep(0.1)

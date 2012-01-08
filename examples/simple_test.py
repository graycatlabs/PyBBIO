# simple_test.py - Alexander Hiam - 12/2012
# Flip-flops between two of the Beagleboard's on-board LEDs for 10 seconds.

import time

# Must 'import *' to get all the needed constants,
# simply importing bbio won't do:
from bbio import *

# Create a BeagleBoard instance:
bb = BeagleBone()
# Set the two LEDs as outputs:
bb.pinMode(USR2, OUTPUT)
bb.pinMode(USR3, OUTPUT)

# Start one high and one low:
bb.digitalWrite(USR2, HIGH)
bb.digitalWrite(USR3, LOW)

# Toggle the two for a few seconds:
for i in range(20):
  bb.toggle(USR2)
  bb.toggle(USR3)
  time.sleep(0.5)

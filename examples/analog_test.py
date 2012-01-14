# analog_test.py - Alexander Hiam
# Testing analogRead()1

import time

# Must 'import *' to get all the needed constants,
# simply importing bbio won't do:
from bbio import *

# Create a BeagleBoard instance:
bb = BeagleBone()
bb._analog_init()

for i in range(20):
  print bb.analogRead(AIN7)
  time.sleep(0.5)

bb.cleanup()


from bbio import *
from RotaryEncoder import *

encoder = RotaryEncoder(1)

def setup():
  encoder.setAbsolute()
  encoder.zero()
  
def loop():
  print encoder.getPosition()
  delay(1000)
  
run(setup, loop)

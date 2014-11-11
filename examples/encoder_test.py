#!/usr/bin/env python
"""
 encoder_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the eQEP library
 for PyBBIO.

 This example program is in the public domain.
"""
from bbio import *
from bbio.libraries.RotaryEncoder import RotaryEncoder

encoder = RotaryEncoder(RotaryEncoder.EQEP2b)

def setup():
  encoder.setAbsolute()
  encoder.zero()
  
def loop():
  print "encoder position : "+encoder.getPosition()
  delay(1000)
  
run(setup, loop)

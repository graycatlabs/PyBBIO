#!/usr/bin/env python
"""
 Servo_sweep.py
 Alexander Hiam - 11/7/12

 An example use of PyBBIO's Servo library to sweep the angle 
 of a servo motor back and forth between 0 and 180 degrees.

 Based on Arduino's Servo library example:
  http://arduino.cc/en/Tutorial/Sweep

 Connect the servo's power wires to 5V (P9.8) and ground (P9.2),
 and the signal wire to PWM1A (P9.14). 


 This example is in the public domain.
"""

# First we must import PyBBIO: 
from bbio import *
# Then we can import Servo:
from Servo import *

# Create an instance of the Servo object:
servo1 = Servo(PWM1A)
# We could have left out the PWM pin here and used 
# Servo.attach(PWM1A) in setup() instead.

def setup():
  # Nothing to do here
  pass

def loop():
  for angle in range(180):  # 0-180 degrees
    servo1.write(angle)
    delay(15)

  for angle in range(180, 0, -1):  # 180-0 degrees
    servo1.write(angle)
    delay(15)

run(setup, loop)

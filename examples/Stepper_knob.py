#!/usr/bin/env python
"""
 Stepper_knob.py
 Alaa Agwa - 3/3/2014

 An example use of PyBBIO's stepper motor follows the turns of a potentiometer
 (or other sensor) on analog input 0.

 Based on Arduino's Servo library example:
  http://arduino.cc/en/Tutorial/MotorKnob



 This example is in the public domain.
"""

# First we must import PyBBIO: 
from bbio import *
# Then we can import Stepper:
from Stepper import *

stepper = Stepper(100,GPIO01_17,GPIO03_21,GPIO03_19,GPIO03_15)

def setup():
	stepper.setSpeed(30);

def loop():
	#get the sensor value
	val = analogRead(0)

	#move a number of steps equal to the change in the
	#sensor reading
	stepper.step(val - previous)

	#remember the previous value of the sensor
	previous = val

run(setup, loop)
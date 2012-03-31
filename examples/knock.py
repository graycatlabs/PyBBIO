"""
 knock.py - Alexander Hiam - 3/21/2012
 Adapted from the Ardiuno knock.pde example skecth for use
 with PyBBIO - https://github.com/alexanderhiam/PyBBIO

 Uses a Piezo element to detect knocks. If a knock is detected
 above the defined threshold one of the on-board LEDs is toggled
 and 'knock' is written to stdout.

 This is based quite directly on the Knock Sensor example 
 sketch, which can be found in the Arduino IDE examples or 
 here:
   http://www.arduino.cc/en/Tutorial/Knock

 Version history of knock.pde:   
   created 25 Mar 2007
   by David Cuartielles <http://www.0j0.org>
   modified 4 Sep 2010
   by Tom Igoe

 This example is in the public domain.
"""

from bbio import *

LED = USR3        # On-board LED
KNOCK_SENSOR = A0 # AIN0 - pin 39 on header P9
THRESHOLD = 245   # analogRead() value > THRESHOLD indicates knock


def setup():
  pinMode(LED, OUTPUT)  
  print "PyBBIO Knock Sensor"

def loop():
  value = analogRead(KNOCK_SENSOR)
  #print value
  if (value > THRESHOLD):
    toggle(LED)
    print "knock!"
  delay(100)
run(setup, loop)

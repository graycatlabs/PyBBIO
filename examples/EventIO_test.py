#!/usr/bin/env python
"""
 EventIO_test.py 
 Alexander Hiam

 An example to demonstrate the use of the EventIO library
 for PyBBIO.

 Example circuit:
  -A switch from 3.3v (P9.3) to GPIO1_7 (P8.4) with a 10k pull-down
   resistor to GND (P9.2)
 
  -A switch from 3.3v to GPIO1_3 (P8.6) with a 10k pull-down resistor.

  -A voltage divider with two equal resistors around 10k between 3.3v
   and GND to make about 1.6v   

  -A potentiometer with the two outer pins connected to the 1.6v output
   of the voltage divider and GND, and the center wiper pin connected to
   AIN0 (P9.39).

 This example program is in the public domain.
"""

# First we import PyBBIO: 
from bbio import *
# Then we can import EventIO:
from EventIO import *

sw1 = GPIO1_7
sw2 = GPIO1_3
pot = AIN0

# Create an event loop:
event_loop = EventLoop()

#--- The events to be triggered: ---
def event1():
  toggle(USR1)
  return EVENT_CONTINUE

def event2():
  toggle(USR2)
  return EVENT_CONTINUE

def event3():
  digitalWrite(USR3, HIGH)
  return EVENT_CONTINUE

def event4():
  digitalWrite(USR3, LOW)
  return EVENT_CONTINUE
#-----------------------------------

def setup():
  # This sets sw1 to trigger event1 when pressed with a debounce
  # time of 50ms:
  event_loop.add_event(DigitalTrigger(sw1, HIGH, event1, 50))

  # This sets sw2 to trigger event2 when pressed with a debounce
  # time of 270ms:
  event_loop.add_event(DigitalTrigger(sw2, HIGH, event2, 270))

  # This sets event3 to be called when the value on pot is above
  # 1820: 
  event_loop.add_event(AnalogLevel(pot, 1820, event3))

  # This sets event3 to be called when the value on pot is below
  # 1820: 
  event_loop.add_event(AnalogLevel(pot, 1820, event4, direction=-1))

  # Then start the event loop:
  event_loop.start()

def loop():
  # Because the event loop is run as a seperate process, this will
  # be executed normally.
  print "Time running: %ims" % int(millis())
  delay(3000)

run(setup, loop)
# As soon as ctrl-c is pressed the event loop process will be 
# automatically termintated and the program wil exit happily.

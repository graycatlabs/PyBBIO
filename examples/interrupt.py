# interrupt.py - Alexander Hiam - 12/2013
# Sets P9.12 as an input with a pull-up resistor and attaches a 
# falling edge interrupt. The 5th time the pin goes low the interrupt
# is detached.
#
# This example is in the public domain

from bbio import *

pin = GPIO1_28 

n_interrupts = 0

def countInterrupts():
  # This function will be called every time the pin goes low
  global n_interrupts
  n_interrupts += 1
  print "interrupt # %i" % n_interrupts
  if n_interrupts >= 5:
    print "detaching interrupt"
    detachInterrupt(pin)
    
def setup():
  pinMode(pin, INPUT, PULLUP)
  attachInterrupt(pin, countInterrupts, FALLING)
  print "falling edge interrupt attached to P9.12 (GPIO1_28)"
  
def loop():
  print "The loop continues..."
  delay(1000)
  
run(setup, loop)
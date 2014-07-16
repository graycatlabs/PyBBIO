#!/usr/bin/env python
'''
 adt7310_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the ADT7310 library
 for PyBBIO.

 This example program is in the public domain.
'''
from bbio import *
from ADT7310 import *

adt = ADT7310(0,0)
pin = GPIO1_28  
pinc = GPIO0_4

def alarm():
  print("Too Hot or Cold!")

def criticalalarm():
  print("Over Critical Temperature")

def setup():
  adt.setLowTemp(5)
  adt.setHighTemp(50)
  adt.setCriticalTemp(60)
  adt.setAlarm(pin,alarm)
  adt.setCriticalAlarm(pin,criticalalarm)
    
def loop():
  temp = adt.getTemp() 
  print "temperature : "+str(temp)
  delay(500)  
  
run(setup,loop)

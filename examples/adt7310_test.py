#!/usr/bin/env python
'''
 adt7310_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the ADT7310 library
 for PyBBIO.

 This example program is in the public domain.
'''
from bbio import *
from bbio.libraries.ADT7310 import *

adt = ADT7310(0,0)
#interrput pin
pin = GPIO1_28
#critical pin
pinc = GPIO1_18

def alarm():
  '''executed when temp crosses threshold temperatures - high and low '''
  print("Too Hot or Cold!")

def criticalalarm():
  '''executed when temp crossed critical temperature '''
  print("Over Critical Temperature")

def setup():
  #sets low temperature threshold
  adt.setLowTemp(5)
  #sets high temperature threshold
  adt.setHighTemp(50)
  #sets high temperature threshold
  adt.setCriticalTemp(60)
  #sets the function to call when interrupt pin in active.
  adt.setAlarm(pin,alarm)
  #sets the function to call when interrupt pin in active.
  adt.setCriticalAlarm(pinc,criticalalarm)
    
def loop():
  temp = adt.getTemp() 
  print "temperature : "+str(temp)
  delay(500)  
  
run(setup,loop)

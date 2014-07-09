"""
 adt7310_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the ADT7310 library
 for PyBBIO.

 This example program is in the public domain.
"""
from bbio import *
from ADT7310 import *

adt = ADT7310(0,0)
pin = GPIO1_28  

def alarm():
  print("Too Hot or Cold!")

def setup():
  adt.setLowTemp(5)
  adt.setHighTemp(50)
  adt.setCriticalTemp(40)
  adt.setAlarm(pin,alarm)
    
def loop():
  temp = adt.getTemp() 
  print(temp)
  delay(500)  
  
run(setup,loop)

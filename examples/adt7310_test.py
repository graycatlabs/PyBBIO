from bbio import *
from ADT7310 import *
from bbio.util import addToCleanup

adt = ADT7310(0,0)
pin = GPIO1_28  

def alarm():
  print("Too Hot or Cold!")

def setup():
  adt.setLowTemp(-10)
  adt.setHighTemp(45)
  adt.setCriticalTemp(40)
  adt.setAlarm(pin,alarm)
    
def loop():
  temp = adt.getTemp() 
  print(temp)
  delay(500)  
  
run(setup,loop)
addToCleanup(adt.end())

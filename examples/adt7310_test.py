from bbio import *
from ADT7310 import *

adt = ADT7310(0,0) 

def setup():
  pass
  
def loop():
  temp = adt.getTemp() 
  print(temp)
  delay(500)  
  
run(setup,loop)
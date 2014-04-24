from bbio import *
from ADT7310 import *

def setup():
  adt = ADT7310(0,0)
  
def loop():
  temp = getTemp() 
  print(temp)
  delay(500)  
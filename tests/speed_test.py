
from bbio import *

def setup():
  pinMode(GPIO1_6, OUTPUT)
  

def loop():
  state = 1
  while(True):
    digitalWrite(GPIO1_6, state)
    state ^= 1

run(setup, loop) 

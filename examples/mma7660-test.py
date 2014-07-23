from bbio import *
from MMA7660 import *

acc = MMA7660(2)

def setup():
  acc.setOrientation()
  
def loop():
  x = acc.getX()
  y = acc.getY()
  z = acc.getZ()
  print "X : "+str(x)+" Y : "+str(y)+" Z : "+str(z)
  #tap = acc.detectTap()
  #print "Tap : "+str(tap)
  print acc.getOrientation()
  delay(1000)
  
run(setup,loop)
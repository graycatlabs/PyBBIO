from bbio import *
from bbio.libraries.BMP183 import BMP183

bmp = BMP183(SPI0)

def setup():
  pass

def loop():
  temp = bmp.getTemp()
  pressure = bmp.getPressure(bmp.OVERSAMPLE_3)

  print "\ntemperature : %0.2f C" % temp
  print "pressure    : %i Pa" % pressure

  delay(5000)
    
run(setup, loop)
"""
 GridEYE_test.py 
 Alexander Hiam <alex@graycat.io>
  
 Example program for PyBBIO's GridEYE library. 

 This example program is in the public domain.
"""

from bbio import *
from bbio.libraries.GridEYE import GridEYE

# Initialize the I2C bus:
I2C1.open()
# Create a GridEYE object:
grideye = GridEYE(I2C1)

ambient = grideye.getAmbientTemp()
frame = grideye.getFrame()

print "ambient temp: {:0.1f}C".format(ambient)
print "sensor temp:"
for y in range(8):
  string = ""
  for x in range(8):
     string += "  {:5.1f}".format(frame[y*8+x])
  print string
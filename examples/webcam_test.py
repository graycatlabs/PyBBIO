'''
 webcam_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the WebCam library
 for PyBBIO.

 This example program is in the public domain.
'''

from bbio import *
from bbio.libraries.WebCam import WebCam

cam = WebCam()
s = 0

def setup():
  pass
  
def loop():
  global s
  location = "pic"+str(s)
  cam.takeSnapshot(location)
  print "saving image to %s" % location
  s += 1
  delay(10000)
  
run(setup, loop)
"""
 mma7660_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the MMA7660 library
 for PyBBIO.

 This example program is in the public domain.
"""
from bbio import *
from bbio.libraries.MMA7660 import MMA7660

INT_PIN = GPIO1_16

accel = MMA7660(2)

def accelCallback(back_front, portrait_landscape, tap, shake):
  '''
  callback_funtion : has to take(back_front, portrait_landscape, tap, shake) 
                       as parameters.
                       back_front = 1 - Front: Equipment is lying on its front
                       back_front = 2 - Back: Equipment is lying on its back
                       
                       portrait_landscape = 1 - Left: Equipment is in landscape
                                                mode to the left
                       portrait_landscape = 2 - Right: Equipment is in landscape
                                                mode to the right
                       portrait_landscape = 5 - Down: Equipment standing 
                                                vertically in inverted orientation
                       portrait_landscape = 6 - Up: Equipment standing vertically
                                                in normal orientation
                       
                       tap = 0 - Tap Not Detected
                       tap = 1 - Tap Detected
                       
                       shake = 0 - Shake Not Detected
                       shake = 1 - Shake Detected
  '''
  if tap == 1:
    print "Tap Detected"
  if shake == 1:
    print "Shake Detected" 

def setup():
  int_cfg = accel.INT_PD  | \
            accel.INT_SHX
  '''
  configuration : INT_FB - Front/Back position change causes an interrupt
                  INT_PL - Up/Down/Right/Left position change causes interrupt
                  INT_PD - Successful tap detection causes an interrupt
                  INT_SHX - Shake detected on the X-axis causes an interrupt
                  INT_SHY - Shake detected on the Y-axis causes an interrupt
                  INT_SHZ - Shake detected on the Z-axis causes an interrupt
  '''
  accel.setInterrupt(int_cfg, INT_PIN, accelCallback)
  '''
  setInterrupt(configuration, interrupt_pin, callback_funtion)
  Sets interrupt on interrupt_pin and calls callback_funtion when interrupt occurs
  '''
  accel.settapthreshold(30)
  accel.setTapDebounce(15)

  
def loop():
  xyz = accel.getXYZ()
  print "X : "+str(xyz[0])+" Y : "+str(xyz[1])+" Z : "+str(xyz[2])
  orient = accel.getOrientation()
  if orient[1] == 1:
    print "Orientation : Left: Equipment is in landscape mode to the left"
  elif orient[1] == 2:
    print "Orientation : Right: Equipment is in landscape mode to the right"
  elif orient[1] == 5:
    print "Orientation : Down: Equipment standing vertically in inverted orientation"
  elif orient[1] == 6:
    print "Orientation : Up: Equipment standing vertically in normal orientation"
  if orient[0] == 1 :
    print "Orientation : Front: Equipment is lying on its front"
  elif orient[0] == 2:
    print "Orientation : Back: Equipment is lying on its back"
  delay(3000)

run(setup,loop)

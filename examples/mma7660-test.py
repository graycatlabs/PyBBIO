from bbio import *
from MMA7660 import MMA7660

INT_PIN = GPIO1_28

accel = MMA7660(2)

def accelCallback(back_front, portrait_landscape, tap, shake):
  if portrait_landscape == 1:
    print "Orientation : Left: Equipment is in landscape mode to the left"
  elif portrait_landscape == 2:
    print "Orientation : Right: Equipment is in landscape mode to the right"
  elif portrait_landscape == 5:
    print "Orientation : Down: Equipment standing vertically in inverted orientation"
  elif portrait_landscape == 6:
    print "Orientation : Up: Equipment standing vertically in normal orientation"
  if back_front == 1 :
    print "Orientation : Front: Equipment is lying on its front"
  elif back_front == 2:
    print "Orientation : Back: Equipment is lying on its back"
  if tap == 1:
    print "Tap Detected"
  if shake == 1:
    print "Shake Detected" 

def setup():
  int_cfg = accel.INT_FB  | \
            accel.INT_PL  | \
            accel.INT_PD  | \
            accel.INT_SHX | \
            accel.INT_SHY | \
            accel.INT_SHZ
             
  accel.setInterrupt(int_cfg, INT_PIN, accelCallback)

  
def loop():
  x = accel.getX()
  y = accel.getY()
  z = accel.getZ()
  print "X : "+str(x)+" Y : "+str(y)+" Z : "+str(z)
  delay(30000)
run(setup,loop)
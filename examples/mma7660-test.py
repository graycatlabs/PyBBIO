from bbio import *
from MMA7660 import MMA7660

INT_PIN = GPIO1_28

accel = MMA7660(2)

def accelCallback(back_front, portrait_landscape, tap, shake):
  if tap == 1:
    print "Tap Detected"
  if shake == 1:
    print "Shake Detected" 

def setup():
  int_cfg = accel.INT_PD  | \
            accel.INT_SHX             
  accel.setInterrupt(int_cfg, INT_PIN, accelCallback)
  accel.settapthreshold(4)
  accel.setTapDebounce(31)

  
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

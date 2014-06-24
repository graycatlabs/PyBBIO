
from platform import detect_platform

platform = detect_platform()

if "BeagleBone" in platform:
  from beaglebone import *

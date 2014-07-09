
from platform import detect_platform
_platform = detect_platform()
if "BeagleBone" in _platform:
  from beaglebone import *
del _platform
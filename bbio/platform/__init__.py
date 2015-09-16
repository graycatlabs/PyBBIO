
from platform import detect_platform
_platform = detect_platform()

if "BeagleBone" in _platform:
  from beaglebone import *
  import beaglebone

#elif "SomeOtherPlatform" in _platform:
#  ...

else:
  # Unsupported platform
  raise ImportError("Cannot import PyBBIO, platform not supported")

# No need to keep this in the namespace:
del _platform

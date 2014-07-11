# bbio.platform.beaglebone.config

from bbio.platform.platform import detect_platform 
_platform = detect_platform()
if "3.8" in _platform:
  from bone_3_8.config import *
elif "3.2" in _platform:
  from bone_3_2.config import *
del _platform
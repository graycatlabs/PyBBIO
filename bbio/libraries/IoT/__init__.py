
try:
  import requests
except ImportError:
  exit("\The IoT library requires the 'requests' package:\n"+\
       "  # pip install requests\n")

import thingspeak, phant

__all__ = [
  'thingspeak', 'phant'
]
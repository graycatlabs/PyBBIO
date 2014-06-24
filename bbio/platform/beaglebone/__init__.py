# initialization for beaglebone

from bbio.platform.platform import detect_platform 
PLATFORM = detect_platform()

if "3.8" in PLATFORM:
  from bone_3_8 import config
  from bone_3_8.adc import analogRead, inVolts
  from bone_3_8.pwm import analogWrite, pwmFrequency, pwmEnable, pwmDisable
  
elif "3.2" in PLATFORM:
  from bone_3_2 import config
  from bone_3_2.adc import analogRead, inVolts
  from bone_3_2.pwm import analogWrite, pwmFrequency, pwmEnable, pwmDisable
  
from gpio import pinMode, digitalWrite, digitalRead, toggle, pinState, \
                 shiftIn, shiftOut
from interrupt import attachInterrupt, detachInterrupt
from serial_port import Serial1, Serial2, Serial4, Serial5
from i2c import Wire1, Wire2

from api import platform_init, platform_cleanup
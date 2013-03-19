
from bbio.platform.beaglebone import *

def platform_init():
  analog_init()
  pwm_init()

def platform_cleanup():
  analog_cleanup()
  pwm_cleanup()
  serial_cleanup()



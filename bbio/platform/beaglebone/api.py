# api.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone platform API file.


from bbio.platform import *

def platform_init():
  analog_init()
  pwm_init()

def platform_cleanup():
  analog_cleanup()
  pwm_cleanup()
  serial_cleanup()



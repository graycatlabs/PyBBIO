# api.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone platform API file.

from adc import analog_init, analog_cleanup
from pwm import pwm_init, pwm_cleanup
from serial_port import serial_cleanup
from gpio import gpioCleanup
  
def platform_init():
  analog_init()
  pwm_init()

def platform_cleanup():
  analog_cleanup()
  pwm_cleanup()
  serial_cleanup()
  gpioCleanup()


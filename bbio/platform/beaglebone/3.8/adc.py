# adc.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone ADC driver for kernels >= 3.8.
#
# Just a wrapper for the sysfs ADC driver for the time being. 

import cape_manager
from config import *

def analog_init():
  """ Initializes the on-board 8ch 12bit ADC. """
  cape_manager.load(ADC_ENABLE_DTS_OVERLAY)


def analog_cleanup():
  pass


def analogRead(analog_pin):
  """ Returns analog value read on given analog input pin. """
  pass


def inVolts(adc_value, bits=12, vRef=1.8):
  """ Converts and returns the given ADC value to a voltage according
      to the given number of bits and reference voltage. """
  return adc_value*(vRef/2**bits)


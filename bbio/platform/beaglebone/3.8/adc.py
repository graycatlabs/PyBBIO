# adc.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone ADC driver for kernels >= 3.8.
#
# Just a wrapper for the sysfs ADC driver for the time being. 

import os, glob
import cape_manager
from config import *

def analog_init():
  """ Initializes the on-board 8ch 12bit ADC. """
  cape_manager.load(ADC_ENABLE_DTS_OVERLAY, auto_unload=False)
  # Don't unload the overlay on exit for now because it can 
  # cause kernel panic.

def analog_cleanup():
  pass

def analogRead(adc_pin):
  """ Returns voltage read on given analog input pin in millivolts. """
  if adc_pin in ADC: adc_pin = ADC[adc_pin]
  adc_file = adc_pin[0]
  if not os.path.exists(adc_file):
    # Overlay not loaded yet
    overlay = adc_pin[1]
    cape_manager.load(overlay, auto_unload=False)
  with open(glob.glob(adc_file)[0], 'rb') as f: 
    mv = f.read()
  return int(mv)

def inVolts(mv):
  """ Converts millivolts to volts... you know, to keep the API 
      consistent. """
  return mv/1000.0


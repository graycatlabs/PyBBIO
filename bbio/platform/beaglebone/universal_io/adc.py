# adc.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone ADC driver for kernels >= 3.8.
#
# Just a wrapper for the sysfs ADC driver for the time being. 

import os, glob, bbio
import cape_manager
from config import ADC, ADC_ENABLE_DTS_OVERLAY

_ADC_INITIALIZED = False

def analog_init():
  """ Initializes the on-board 8ch 12bit ADC. """
  pass

def analog_cleanup():
  pass

def analogRead(adc_pin):
  """ Returns voltage read on given analog input pin. If passed one of 
      PyBBIO's AIN0-AIN5 keywords the voltage will be returned in millivolts.
      May also be passed the path to an AIN file as created by a cape overlay,
      in which case the value will be returned as found in the file. """
  global _ADC_INITIALIZED      
  if not _ADC_INITIALIZED:
    cape_manager.load(ADC_ENABLE_DTS_OVERLAY, auto_unload=False)
    # Don't unload the overlay on exit for now because it can
    # cause kernel panic.
    bbio.delay(100)
    _ADC_INITIALIZED = True
  if adc_pin in ADC: 
    adc_pin = ADC[adc_pin]
    adc_file = glob.glob(adc_pin[0])
    if len(adc_file) == 0:
      overlay = adc_pin[1]
      # Overlay not loaded yet
      cape_manager.load(overlay, auto_unload=False)
    adc_file = glob.glob(adc_pin[0])
  else:
    adc_file = glob.glob(adc_pin)
  if len(adc_file) == 0:
    raise Exception('*Could not load overlay for adc_pin: %s' % adc_pin)
  adc_file = adc_file[0]
  # Occasionally the kernel will be writing to the file when you try 
  # to read it, to avoid IOError try up to 5 times:
  for i in range(5):
    try:
      with open(adc_file, 'rb') as f: 
        val = f.read()
      return int(val)
    except IOError:
      continue
  raise Exception('*Could not open AIN file: %s' % adc_file)


def inVolts(mv):
  """ Converts millivolts to volts... you know, to keep the API 
      consistent. """
  return mv/1000.0


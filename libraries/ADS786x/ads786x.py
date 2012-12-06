"""
 ADS786x - v0.1
 Copyright 2012 Alexander Hiam
 A library for interfacing with TI's ADS786x series
 analog-to-digital converters
"""

from bbio import *

class ADS786x(object):
  """ Base class for all each of ADS786x series classes. """
  def __init__(self, data_pin, clk_pin, cs_pin, vref=3.3):
    self._data = data_pin
    self._clk = clk_pin
    self._cs = cs_pin
    pinMode(self._data, INPUT)
    for i in (self._cs, self._clk): pinMode(i, OUTPUT)

    # Idle state for clock and cs (data doesn't matter):
    for i in (self._cs, self._clk): digitalWrite(i, HIGH)
    
    # Calculate volts per bit:
    self.dv = float(vref)/2**self.n_bits

  def read(self):
    """ Read and return the ADC value. """
    digitalWrite(self._cs, LOW)
    value = shiftIn(self._data, self._clk, MSBFIRST, n_bits=self.n_bits+3)
    digitalWrite(self._cs, HIGH)
    return value

  def readVolts(self):
    """ Sets the DAC output to the given voltage. """
    return self.read() * self.dv


class ADS7866(ADS786x):
  # Tested, working
  n_bits = 12

class ADS7867(ADS786x):
  # Untested
  n_bits = 10

class ADS7868(ADS786x):
  # Untested
  n_bits = 8

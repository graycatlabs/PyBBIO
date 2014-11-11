"""
 DACx311 - v0.1
 Copyright 2012 Alexander Hiam
 A library for interfacing with TI's DACx311 series
 digital-to-analog converters
"""

from bbio import *

class DACx311(object):
  """ Base class for all each of DACx311 series classes. """
  def __init__(self, data_pin, clk_pin, sync_pin, vref=3.3):
    self._data = data_pin
    self._clk = clk_pin
    self._sync = sync_pin
    for i in (self._data, self._sync, self._clk): pinMode(i, OUTPUT)

    # Idle state for clock and sync (data doesn't matter):
    for i in (self._sync, self._clk): digitalWrite(i, HIGH)
    
    self.max_value = 2**self.n_bits - 1
    # Calculate volts per bit:
    self.dv = float(vref)/2**self.n_bits

  def set(self, value):
    """ Set the DAC control register to the given value. """
    if (value > self.max_value): value = self.max_value
    if (value < 0): value = 0
    value <<= self.bit_shift
    digitalWrite(self._sync, LOW)

    shiftOut(self._data, self._clk, MSBFIRST, (value>>8), FALLING)
    shiftOut(self._data, self._clk, MSBFIRST, value & 0xff, FALLING)

    digitalWrite(self._sync, HIGH)

  def setVolts(self, volts):
    """ Sets the DAC output to the given voltage. """
    value = int(volts/self.dv)
    self.set(value)


class DAC5311(DACx311):
  # Untested 
  n_bits = 8
  bit_shift = 6

class DAC6311(DACx311):
  # Untested
  n_bits = 10
  bit_shift = 4

class DAC7311(DACx311):
  # Tested working
  n_bits = 12
  bit_shift = 2

class DAC8311(DACx311):
  # Untested
  n_bits = 14
  bit_shift = 0

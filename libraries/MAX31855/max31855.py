"""
 MAX31855 - v0.1
 Copyright 2012 Alexander Hiam
 A library for PyBBIO to interface with Maxim's MAX31855 
 thermocouple amplifier.
"""

from bbio import *


class MAX31855(object):
  def __init__(self, data_pin, clk_pin, cs_pin):
    self._data = data_pin
    self._clk = clk_pin
    self._cs = cs_pin
    pinMode(self._data, INPUT)
    for i in (self._cs, self._clk): pinMode(i, OUTPUT)
    self.error = None

    # Idle state for clock and cs (data doesn't matter):
    for i in (self._cs, self._clk): digitalWrite(i, HIGH)

  def readTempF(self):
    """ Reads temperature, converts to Fahrenheit and returns, or 
        returns None if error detected. """
    temp = self.readTempC() 
    return temp if not temp else temp * 9.0/5.0 + 32

  def readTempC(self):
    """ Reads and returns the temperature in Celsius, or returns None
        if error detected. """
    value = self.read()
    if not value: return None
    # Extract 14-bit signed temperature value:
    temp = (value >> 18) & 0x3fff
    sign = temp & (1<<14)
    if sign: temp = -(~temp+1 & 0x1fff)
    return temp*0.25
    
  def readTempInternal(self):
    """ Reads and returns the MAX31855 reference junction temperature 
        in Celsius, or returns None if error detected. """
    value = self.read()
    if not value: return None
    # Extract 12-bit signed temperature value:
    temp = (value >> 4) & 0xfff
    sign = temp & (1<<12)
    if sign: temp = -(~temp+1 & 0x7ff)
    return temp*0.0625

  def read(self):
    """ Receives and returns full 32-bit map from MAX31855, or sets
        self.error and returns None if fault detected. """
    self.error = None
    digitalWrite(self._cs, LOW)
    value = shiftIn(self._data, self._clk, MSBFIRST, n_bits=32)
    digitalWrite(self._cs, HIGH)

    if (value & (1<<16)):
      # Fault detected, check error bits:
      if (value & (1<<2)):
        self.error = "*Thermocouple shorted to Vcc*"
      elif (value & (1<<1)):
        self.error = "*Thermocouple shorted to GND*"
      else:
        self.error = "*Thermocouple not connected*"
      return None

    return value

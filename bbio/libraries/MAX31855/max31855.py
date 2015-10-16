"""
 MAX31855
 Copyright 2015 - Alexander Hiam <alex@graycat.io>

 A library for PyBBIO to interface with Maxim's MAX31855 thermocouple amplifier.

 MAX31855 is released as part of PyBBIO under its MIT license.
 See PyBBIO/LICENSE.txt
"""

class MAX31855(object):
  SPI_CLOCK_MODE = 1
  SPI_FREQUENCY  = 4000000
  SPI_N_BITS     = 32

  OPEN_CIRCUIT   = 1
  SHORT_TO_GND   = 2
  SHORT_TO_VCC   = 4


  def __init__(self, spi_bus, spi_cs=0, offset=0):
    self.spi_bus = spi_bus
    self.spi_cs = spi_cs
    self.offset = offset
    self.error = None

  def readTempF(self):
    """ Reads temperature, converts to Fahrenheit and returns, or 
        returns None if error detected. """
    temp = self.readTempC() 
    return temp if not temp else temp * 9.0/5.0 + 32

  def readTempC(self):
    """ Reads and returns the temperature in Celsius, or returns None
        if error detected. """
    value = self.read()
    if value == None: return None
    # Extract 14-bit signed temperature value:
    temp = (value >> 18) & 0x3fff
    # Convert 2's complement:
    if temp >= 2**13: temp -= 2**14 
    return temp*0.25 + self.offset
    
  def readTempInternal(self):
    """ Reads and returns the MAX31855 reference junction temperature 
        in Celsius, or returns None if error detected. """
    value = self.read()
    if value == None: return None
    temp = (value >> 4) & 0xfff
    # Convert 2's complement:
    if temp >= 2**11: temp -= 2**12 
    return temp*0.0625

  def read(self):
    """ Receives and returns full 32-bit map from MAX31855, or sets
        self.error and returns None if fault detected. """
    self.error = None

    # Configure SPI bus as required by the MAX31855:
    self.spi_bus.setClockMode(self.spi_cs, self.SPI_CLOCK_MODE)
    self.spi_bus.setMaxFrequency(self.spi_cs, self.SPI_FREQUENCY)
    self.spi_bus.setBitsPerWord(self.spi_cs, self.SPI_N_BITS)
    self.spi_bus.setMSBFirst(self.spi_cs)
    self.spi_bus.setCSActiveLow(self.spi_cs)

    value = self.spi_bus.read(self.spi_cs, 1)[0]

    if (value & (1<<16)):
      # Fault bit set, save error code and return None:
      self.error = value & 0b111
      return None

    return value

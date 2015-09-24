"""
GridEYE
Copyright 2015 - Alexander Hiam <alex@graycat.io>

A PyBBIO library for controlling the Panasonic AMG88 Grid-EYE I2C 8x8 thermal 
sensor array.

GridEYE is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
"""

import bbio

class GridEYE(object):
  AMG88_ADDR = 0x68
  AMG88_ALT_ADDR = 0x69

  REG_PCTL        = 0x00
  PCTL_NORMAL     = 0x00
  PCTL_SLEEP      = 0x10
  PCTL_STANDBY_60 = 0x20
  PCTL_STANDBY_10 = 0x21

  REG_RST  = 0x01
  RST_FLAG = 0x30
  RST_INIT = 0x3f

  REG_FPSC   = 0x02
  FPSC_1FPS  = 0x01
  FPSC_10FPS = 0x00


  REG_AVE     = 0x07
  AVE_ENABLE  = 0x20
  AVE_DISABLE = 0x00

  REG_TTHL = 0x0e
  REG_TTHH = 0x0f

  REG_TEMP_START = 0x80
  TEMP_N_BYTES   = 128 # 64 px, 2 byte/px

  def __init__(self, i2c_bus, addr=AMG88_ADDR):
    self.i2c_bus = i2c_bus
    self.addr = addr
    self.reset()
    bbio.delay(100)

  def getFrame(self):
    """ Reads and returns the current temperature map as a 1-dimensional list 
        of values in Celsius.
    """
    data = self.i2c_bus.readTransaction(self.addr, self.REG_TEMP_START, 
                                        self.TEMP_N_BYTES)
    frame = []
    for i in range(0, self.TEMP_N_BYTES, 2):
      temp = data[i+1]<<8 | data[i]
      if temp & (0x1<<11):
        printit = True
        # do 12-bit 2's compliment conversion
        temp -= 4096
      temp *= 0.25 # convert to C
      frame.append(temp)
    return frame

  def getAmbientTemp(self):
    """ Reads and returns the temperature of the AMG88's internal thermistor.
    """
    low, high = self.i2c_bus.readTransaction(self.addr, self.REG_TTHL, 2)
    temp = high<<8 | low
    if temp & (0x1<<11):
        # do 12-bit 2's compliment conversion
      temp -= 4096
    temp *= 0.0625 # convert to C
    return temp

  def enableAveraging(self):
    """ Enables the AMG88's built-in moving average.
    """
    # This sequence is from a Grid-EYE specifications document, I haven't
    # seen it described anywhere:
    self.i2c_bus.write(self.addr, [0x1f, 0x50])
    self.i2c_bus.write(self.addr, [0x1f, 0x45])
    self.i2c_bus.write(self.addr, [0x1f, 0x57])
    self.i2c_bus.write(self.addr, [self.REG_AVE, self.AVE_ENABLE])
    self.i2c_bus.write(self.addr, [0x1f, 0x00])

  def disableAveraging(self):
    """ Disables the AMG88's built-in moving average.
    """
    self.i2c_bus.write(self.addr, [0x1f, 0x50])
    self.i2c_bus.write(self.addr, [0x1f, 0x45])
    self.i2c_bus.write(self.addr, [0x1f, 0x57])
    self.i2c_bus.write(self.addr, [self.REG_AVE, self.AVE_DISABLE])
    self.i2c_bus.write(self.addr, [0x1f, 0x00])

  def reset(self):
    """ Resets all registers to initial settings.
    """
    self.i2c_bus.write(self.addr, [self.REG_RST, self.RST_INIT])
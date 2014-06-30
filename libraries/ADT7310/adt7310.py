from bbio import *

class ADT7310(object):

  def __init__(self, spi_no, cs):
    assert 0 <= spi_no < 2, "spi_no must be between 0 or 1"
    assert 0 <= cs < 2, "cs must be between 0 or 1"
    if spi_no == 0:
      self.spidev = SPI0
    else:
      self.spidev = SPI1
    self.cs = cs
    self.spidev.begin()
    self.spidev.setDataMode(self.cs,3)
    
  def getTemp(self):
    self.spidev.write(self.cs,0x54)
    _t = self.spidev.read(self.cs,2)
    if ( _t[0] & 128 == 0):
      temp = (((_t[0]<<8)+_t[1])>>3)/16
    else:
      temp = ((((_t[0]<<8)+_t[1])>>3)-4096)/16
    return temp
    
    
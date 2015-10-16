# spi.py 
# Part of PyBBIO
# github.com/graycatlabs/PyBBIO
# MIT License

import cape_manager, bbio, os, glob, serbus
from config import SPI_BASE_ADDRESSES

class SPIBus(serbus.SPIDev):
  def __init__(self, bus):
    super(SPIBus, self).__init__(bus)
    self._is_open = False

  def open(self):
    if self._is_open: return

    overlay = "BB-SPIDEV%i" % (self.bus)
    cape_manager.load(overlay, auto_unload=False)
    bbio.common.delay(250) # Give driver time to load
    assert cape_manager.isLoaded(overlay), "Could not load SPI overlay"

    for i in glob.glob("/sys/bus/spi/devices/*.0"):
      path = os.path.realpath(i)
      module_addr = int(path.split("/")[4].split(".")[0], 16)
      if module_addr == SPI_BASE_ADDRESSES[self.bus]:
        self.bus = int(path.split("/")[6][-1])
        break
    super(SPIBus, self).open()
    # Initialize to default parameters:
    self.setCSActiveLow(0)
    self.setBitsPerWord(0, 8)
    self.setMaxFrequency(0, 8000000)
    self.setClockMode(0, 0)
    
    self._is_open = True

  def begin(self):
    self.open()

  def end(self):
    self.close()
    
# Initialize the global SPI  instances:
SPI0 = SPIBus(0)
SPI1 = SPIBus(1)

import bbio, os, cape_manager
from bbio.platform.util import spidev

class SPI_Bus(spidev.SPIDev):
  def open(self):
    overlay = 'BB-SPIDEV%i' % (self.bus-1)
    cape_manager.load(overlay, auto_unload=False)
    bbio.delay(250) # Give driver time to load
    assert cape_manager.isLoaded(overlay), "Could not load SPI overlay"
    super(SPI_Bus, self).open()
    # Initialize to default parameters:
    self.setCSActiveLow(0)
    self.setBitsPerWord(0, 8)
    self.setMaxFrequency(0, 8000000)
    self.setClockMode(0, 0)

  def begin(self):
    self.open()

  def end(self):
    self.close()
    
# Initialize the global SPI  instances:
SPI0 = SPI_Bus(1)
SPI1 = SPI_Bus(2)

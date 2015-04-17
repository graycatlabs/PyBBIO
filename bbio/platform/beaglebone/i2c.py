# i2c.py 
# Part of PyBBIO
# github.com/graycatlabs/PyBBIO
# MIT License
# 
# Beaglebone i2c driver

import bbio, cape_manager, os
from bbio.platform.util import i2cdev

class I2CBus(i2cdev.I2CDev):
  def __init__(self, bus):
    assert 1<= bus <= 2, 'Only I2C buses 1 and 2 are available'

    # Corresponds to I2C1 or I2C2 hardware peripheral:
    self.hw_bus = bus

    # The kernel driver uses /dev/i2c-2 for the I2C1 peripheral and 
    # /dev/i2c-1 for the I2C2, so turn 1 to 2 and 2 to 1 (the fun way):
    bus = ((bus-1)^1)+1

    # Run i2cdev.I2CDev initializtion:
    super(I2CBus, self).__init__(bus)

  def open(self, use_10bit_address=False):
    """ I2CDev.open(use_10bit_address=False) -> None
        
        Initialize the I2C bus interface.
        If use_10bit_address=True the bus will use 10-bit slave addresses
        instead of 7-bit addresses. 
    """
    if not os.path.exists('/dev/i2c-%i' % self.bus_num):
      cape_manager.load('BB-I2C%i' % self.hw_bus, auto_unload=False)
      bbio.common.delay(10)
      # Make sure it initialized correctly:
      assert os.path.exists('/dev/i2c-%i' % self.bus_num), \
        'could not enable I2C bus %i' % self.hw_bus

    super(I2CBus, self).open(use_10bit_address=use_10bit_address)

  def begin(self, use_10bit_address=False):
    """ Same as I2CBus.open() """
    self.open(use_10bit_address=use_10bit_address)

  def end(self):
    """ Same as I2CBus.close() """
    self.close()

def i2c_cleanup():
  """ Closes all open i2c buses. """
  Wire1.close()
  Wire2.close()

Wire1 = I2C1 = I2CBus(1)
Wire2 = I2C2 = I2CBus(2) 

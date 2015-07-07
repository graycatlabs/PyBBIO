# i2c.py 
# Part of PyBBIO
# github.com/graycatlabs/PyBBIO
# MIT License
# 
# Beaglebone i2c driver

import bbio, cape_manager, os, glob
from bbio.platform.util import i2cdev
from config import I2C_BASE_ADDRESSES

class I2CBus(i2cdev.I2CDev):
  def __init__(self, bus):
    assert 1<= bus <= 2, 'Only I2C buses 1 and 2 are available'

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

    # Detect bus number:
    for i in glob.glob("/sys/bus/i2c/devices/i2c-*"):
      path = os.path.realpath(i)
      module_addr = int(path.split("/")[4].split(".")[0], 16)
      if module_addr == I2C_BASE_ADDRESSES[self.bus_num]:
        self.bus_num = int(path.split("/")[5][-1])
        break

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

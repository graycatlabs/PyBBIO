"""
 spi_init.py
 3.8 kernel specific SPI initialization for the BeagleBone
"""

import bbio, os, cape_manager

def spi_init(spidev):
  overlay = 'BB-SPIDEV%i-00A0' % spi_num
  assert os.path.exists('/lib/firmware/%s.dtbo' % overlay), \
    "SPI driver not present"
  cape_manager.load(overlay, auto_unload=False)
  bbio.delay(250) # Give driver time to load
"""
 spi_init.py
 3.8 kernel specific SPI initialization for the BeagleBone
"""

import bbio, os, cape_manager

def spi_init(spi_num):
  overlay = 'BB-SPIDEV%i' % spi_num
  assert os.path.exists('/lib/firmware/%s-00A0.dtbo' % overlay), \
    "SPI driver not present"
  cape_manager.load(overlay, auto_unload=False)
  bbio.delay(250) # Give driver time to load
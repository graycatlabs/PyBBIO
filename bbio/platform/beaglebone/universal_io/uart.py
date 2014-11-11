# 3.8/uart.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone pinmux driver
# For Beaglebones with 3.8 kernel

import os, glob, cape_manager, bbio
from config import UART

def uartInit(uart):
  """ Enables the given uart by loading its dto. """
  port, overlay = UART[uart]
  if os.path.exists(port): return True
  # Unloading serial port overlays crashes the current cape manager, 
  # disable until it gets fixed:
  cape_manager.load(overlay, auto_unload=False)
  if os.path.exists(port): return True

  for i in range(5):
    # Give it some time to load
    bbio.delay(100)
    if os.path.exists(port): return True
    
  # If we make it here it's pretty safe to say the overlay couldn't load
  return False
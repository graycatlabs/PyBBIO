# pinmux.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone pinmux driver
# For Beaglebone's with 3.8 kernel

from config import *


def kernelFileIO(file_object, val=None):
  """ For reading/writing files open in 'r+' mode. When called just
      with a file object, will return contents of file. When called 
      with file object and 'val', the file will be overritten with 
      new value and the changes flushed. 'val' must be type str.
      Meant to be used with Kernel driver files for much more 
      efficient IO (no need to reopen every time). """  
  file_object.seek(0)
  if (val == None): return file_object.read()
  file_object.write(val)
  file_object.flush()

def pinMux(fn, mode):
  """ Uses kernel omap_mux files to set pin modes. """
  pass

def export(gpio_pin):
  """ Reserves a pin for userspace use with sysfs /sys/class/gpio interface. 
      Returns True if pin was exported, False if it was already under 
      userspace control. """
  pass

def unexport(gpio_pin):
  """ Returns a pin to the kernel with sysfs /sys/class/gpio interface.
      Returns True if pin was unexported, False if it was already under 
      kernel control. """
  pass

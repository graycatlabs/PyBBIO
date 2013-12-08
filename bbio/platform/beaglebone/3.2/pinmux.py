# 3.2/pinmux.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone pinmux driver
# For Beaglebones with 3.2 kernel

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
  # There's no simple way to write the control module registers from a 
  # user-level process because it lacks the proper privileges, but it's 
  # easy enough to just use the built-in file-based system and let the 
  # kernel do the work. 
  try:
    with open(PINMUX_PATH+fn, 'wb') as f:
      f.write(hex(mode)[2:]) # Write hex string (stripping off '0x')
  except IOError:
    print "*omap_mux file not found: '%s'" % (PINMUX_PATH+fn)

def export(gpio_pin):
  """ Reserves a pin for userspace use with sysfs /sys/class/gpio interface. 
      Returns True if pin was exported, False if it was already under 
      userspace control. """
  if ("USR" in gpio_pin):
    # The user LEDs are already under userspace control
    return False
  gpio_num = int(gpio_pin[4])*32 + int(gpio_pin[6:])
  if (os.path.exists(GPIO_FILE_BASE + 'gpio%i' % gpio_num)): 
    # Pin already under userspace control
    return False
  with open(EXPORT_FILE, 'wb') as f:
    f.write(str(gpio_num))
  return True

def unexport(gpio_pin):
  """ Returns a pin to the kernel with sysfs /sys/class/gpio interface.
      Returns True if pin was unexported, False if it was already under 
      kernel control. """
  if ("USR" in gpio_pin):
    # The user LEDs are always under userspace control
    return False
  gpio_num = int(gpio_pin[4])*32 + int(gpio_pin[6:])
  if (not os.path.exists(GPIO_FILE_BASE + 'gpio%i' % gpio_num)): 
    # Pin not under userspace control
    return False
  with open(UNEXPORT_FILE, 'wb') as f:
    f.write(str(gpio_num))
  return True

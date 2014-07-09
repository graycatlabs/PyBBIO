# 3.2/pinmux.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone pinmux driver
# For Beaglebones with 3.2 kernel

from config import *
from sysfs import kernelFileIO

def pinMux(gpio_pin, mode, preserve_mode_on_exit=False):
  """ Uses kernel omap_mux files to set pin modes. """
  # There's no simple way to write the control module registers from a 
  # user-level process because it lacks the proper privileges, but it's 
  # easy enough to just use the built-in file-based system and let the 
  # kernel do the work. 
  fn = GPIO[gpio_pin][0]
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
  gpio_num = GPIO[gpio_pin][2]
  gpio_file = '%s/gpio%i' % (GPIO_FILE_BASE, gpio_num)
  if (os.path.exists(gpio_file)): 
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
  gpio_num = GPIO[gpio_pin][2]
  gpio_file = '%s/gpio%i' % (GPIO_FILE_BASE, gpio_num)
  if (not os.path.exists(gpio_file)): 
    # Pin not under userspace control
    return False
  with open(UNEXPORT_FILE, 'wb') as f:
    f.write(str(gpio_num))
  return True

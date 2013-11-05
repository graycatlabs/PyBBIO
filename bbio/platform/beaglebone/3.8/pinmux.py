# pinmux.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone pinmux driver
# For Beaglebone's with 3.8 kernel

from config import *
import glob, os

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

def pinMux(register_name, mode):
  """ Uses custom device tree overlays to set pin modes. """
  gpio_pin = ''
  for pin, config in GPIO.items():
    if config[2] == register_name:
      gpio_pin = pin.lower()
      break
  if not gpio_pin:
    print "*unknown pinmux register: %s" % register_name
    return
  mux_file_glob = glob.glob('%s/*%s*/state' % (OCP_PATH, gpio_pin))
  if len(mux_file_glob) == 0:
    os.system('echo PyBBIO-%s > %s' % (gpio_pin, SLOTS_PATH))
    # Should use a proper pipe here and get stdout to see if pin is
    # already reserved.

  mux_file_glob = glob.glob('%s/*%s*/state' % (OCP_PATH, gpio_pin))
  if len(mux_file_glob) == 0:
    print "*Could not load overlay for pin: %s" % gpio_pin
    return 
  mux_file = mux_file_glob[0]
  # Convert mode to ocp mux name:
  mode = 'mode_%s' % format(mode, '#010b') 
  # Possible modes:
  #  mode_0b00100111  # rx active | pull down
  #  mode_0b00110111  # rx active | pull up
  #  mode_0b00101111  # rx active | no pull
  #  mode_0b00000111  # pull down
  #  mode_0b00010111  # pull up
  #  mode_0b00001111  # no pull
  # See /lib/firmware/PyBBIO-src/*.dts for more info  
  with open(mux_file, 'wb') as f:
    f.write(mode)

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


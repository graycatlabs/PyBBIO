# 3.8/pinmux.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone pinmux driver
# For Beaglebones with 3.8 kernel

from config import OCP_PATH, GPIO, GPIO_FILE_BASE, EXPORT_FILE, UNEXPORT_FILE,\
                   SLOTS_FILE
from bbio.common import addToCleanup
import glob, os, cape_manager, bbio


def pinMux_universalio(gpio_pin, mode, preserve_mode_on_exit=False):
  return False
  
def pinMux_dtOverlays(gpio_pin, mode, preserve_mode_on_exit=False):
  gpio_pin = gpio_pin.lower()
  mux_file_glob = glob.glob('%s/*%s*/state' % (OCP_PATH, gpio_pin))
  if len(mux_file_glob) == 0:
    try:
      cape_manager.load('PyBBIO-%s' % gpio_pin, not preserve_mode_on_exit)
      bbio.delay(250) # Give driver time to load
      mux_file_glob = glob.glob('%s/*%s*/state' % (OCP_PATH, gpio_pin))
    except IOError:
      print "*Could not load %s overlay, resource busy" % gpio_pin
      return False

  if len(mux_file_glob) == 0:
    print "*Could not load overlay for pin: %s" % gpio_pin
    return False
    
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
  for i in range(3):
    # If the pin's overlay was just loaded there may not have been enough 
    # time for the driver to get fully initialized, which causes an IOError
    # when trying to write the mode; try up to 3 times to avoid this:
    try:
      with open(mux_file, 'wb') as f:
        f.write(mode)
      return True
    except IOError:
      # Wait a bit between attempts
      bbio.delay(10)
  # If we get here then it didn't work 3 times in a row; raise the IOError:
  raise

  
def pinMux(gpio_pin, mode, preserve_mode_on_exit=False):
  """ Uses custom device tree overlays to set pin modes.
      If preserve_mode_on_exit=True the overlay will remain loaded
      when the program exits, otherwise it will be unloaded before
      exiting.
      *This should generally not be called directly from user code. """
  if not gpio_pin:
    print "*unknown pinmux pin: %s" % gpio_pin
    return

  if SLOTS_FILE:
    status = pinMux_dtOverlays(gpio_pin, mode, preserve_mode_on_exit)
  else:
    status = pinMux_universalIO(gpio_pin, mode, preserve_mode_on_exit)
  if not status:
    print "*could not configure pinmux for pin %s" % gpio_pin


def export(gpio_pin, unexport_on_exit=False):
  """ Reserves a pin for userspace use with sysfs /sys/class/gpio interface. 
      If unexport_on_exit=True unexport(gpio_pin) will be called automatically
      when the program exits. Returns True if pin was exported, False if it was 
      already under userspace control. """
  if ("USR" in gpio_pin):
    # The user LEDs are already under userspace control
    return True
  gpio_num = GPIO[gpio_pin]['gpio_num']
  gpio_file = '%s/gpio%i' % (GPIO_FILE_BASE, gpio_num)
  if (os.path.exists(gpio_file)): 
    # Pin already under userspace control
    return True
  with open(EXPORT_FILE, 'wb') as f:
    f.write(str(gpio_num))
  if unexport_on_exit: 
    addToCleanup(lambda: unexport(gpio_pin))
  return True

def unexport(gpio_pin):
  """ Returns a pin to the kernel with sysfs /sys/class/gpio interface.
      Returns True if pin was unexported, False if it was already under 
      kernel control. """
  if ("USR" in gpio_pin):
    # The user LEDs are always under userspace control
    return False
  gpio_num = GPIO[gpio_pin]['gpio_num']
  gpio_file = '%s/gpio%i' % (GPIO_FILE_BASE, gpio_num)
  if (not os.path.exists(gpio_file)): 
    # Pin not under userspace control
    return False
  with open(UNEXPORT_FILE, 'wb') as f:
    f.write(str(gpio_num))
  return True


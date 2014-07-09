# gpio.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
#
# Beaglebone GPIO driver

import os, math, sysfs
from bbio.util import addToCleanup
from config import GET_USR_LED_DIRECTORY, GPIO, GPIO_FILE_BASE, INPUT,\
                   CONF_PULLUP, CONF_PULLDOWN, CONF_PULL_DISABLE,\
                   CONF_GPIO_INPUT, CONF_GPIO_OUTPUT, FALLING, HIGH, LOW,\
                   MSBFIRST

from bbio.platform.platform import detect_platform 
_platform = detect_platform()
if "3.8" in _platform:
  from bone_3_8 import pinmux
elif "3.2" in _platform:
  from bone_3_2 import pinmux
del _platform

def getGPIODirectory(gpio_pin):
  """ Returns the sysfs kernel driver base directory for the given pin. """
  if 'USR' in gpio_pin:
    # USR LEDs use a different driver
    return GET_USR_LED_DIRECTORY(gpio_pin)
  gpio_num = GPIO[gpio_pin][2]
  return '%s/gpio%i' % (GPIO_FILE_BASE, gpio_num)


def getGPIODirectionFile(gpio_pin):
  """ Returns the absolute path to the state control file for the given pin. """
  if 'USR' in gpio_pin:
    # USR LED driver doesn't have a direction file
    return ''
  d = getGPIODirectory(gpio_pin)
  return '%s/direction' % d


def getGPIOStateFile(gpio_pin):
  """ Returns the absolute path to the state control file for the given pin. """
  d = getGPIODirectory(gpio_pin)
  if 'USR' in gpio_pin:
    # USR LEDs use a different driver
    return '%s/brightness' % d
  return '%s/value' % d


def pinMode(gpio_pin, direction, pull=0, preserve_mode_on_exit=False):
  """ Sets given digital pin to input if direction=1, output otherwise.
      'pull' will set the pull up/down resistor if setting as an input:
      pull=-1 for pull-down, pull=1 for pull up, pull=0 for none. 
      If preserve_mode_on_exit=True, the DT overlay and will remain 
      loaded, the pin will remain exported to user-space control, and 
      the INPUT/OUTPUT mode will be preserved when the program exits. """

  if 'USR' in gpio_pin:
    if direction == INPUT:
      print 'warning: cannot set USR LEDs to INPUT'
    return
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  exported = pinmux.export(gpio_pin)
  if not exported:
    print "warning: could not export pin '%s', skipping pinMode()" % gpio_pin
    return
  elif not preserve_mode_on_exit:
    addToCleanup(lambda: pinmux.unexport(gpio_pin))

  direction_file = getGPIODirectionFile(gpio_pin)

  if (direction == INPUT):
    # Pinmux:
    if (pull > 0): pull = CONF_PULLUP
    elif (pull < 0): pull = CONF_PULLDOWN
    else: pull = CONF_PULL_DISABLE
    pinmux.pinMux(gpio_pin, CONF_GPIO_INPUT | pull, preserve_mode_on_exit)
    # Set input:
    with open(direction_file, 'wb') as f:
      f.write('in')
    return
  # Pinmux:
  pinmux.pinMux(gpio_pin, CONF_GPIO_OUTPUT, preserve_mode_on_exit)
  # Set output:
  with open(direction_file, 'wb') as f:
    f.write('out')


def digitalWrite(gpio_pin, state):
  """ Writes given digital pin low if state=0, high otherwise. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  gpio_file = getGPIOStateFile(gpio_pin)
  if not os.path.exists(gpio_file):
    print "warning: digitalWrite() failed, pin '%s' not exported." % gpio_pin +\
          " Did you call pinMode()?" 
    return
  if (state):    
    sysfs.kernelFilenameIO(gpio_file, '1')
  else:
    sysfs.kernelFilenameIO(gpio_file, '0')


def digitalRead(gpio_pin):
  """ Returns input pin state as 1 or 0. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  gpio_file = getGPIOStateFile(gpio_pin)
  return int(sysfs.kernelFilenameIO(gpio_file))


def toggle(gpio_pin):
  """ Toggles the state of the given digital pin. """
  digitalWrite(gpio_pin, digitalRead(gpio_pin) ^ 1)


def pinState(gpio_pin):
  """ Returns the state of a digital pin if it is configured as
      an output. Returns None if it is configuredas an input. """
  # With sysfs driver this is identical to digitalRead()
  return digitalRead(gpio_pin)


def shiftIn(data_pin, clk_pin, bit_order, n_bits=8, edge=FALLING):
  """ Implements software SPI on the given pins to receive given  number
      of bits from a slave device. edge is the edge which triggers the
      device to write data. """
  # Ensure clock is in idle state:
  digitalWrite(clk_pin, HIGH if (edge==FALLING) else LOW)
  if (bit_order == MSBFIRST): loop_range = (n_bits-1, -1, -1)
  else: loop_range = (n_bits,) 
  data = 0
  for i in range(*loop_range):    
    digitalWrite(clk_pin, LOW if (edge==FALLING) else HIGH)
    digitalWrite(clk_pin, HIGH if (edge==FALLING) else LOW)
    data |= digitalRead(data_pin) << i
  return data

def shiftOut(data_pin, clk_pin, bit_order, data, edge=FALLING):
  """ Implements software SPI on the given pins to shift out data.
      data can be list, string, or integer, and if more than one byte
      each byte will be shifted out with the same endianness as the 
      bits. """
  assert (type(data) != dict), "*shiftOut() does not support dictionaries" 
  assert (type(data) != float), "*shiftOut() does not support floats" 

  if ((type(data) != int) and ((len(data) > 1) or (type(data) == list))):
    # Test for type list here to handle lists of length 1
    for i in data if (bit_order == MSBFIRST) else data[::-1]:
      # Loop through forward if MSB first, otherwise in reverse
      shiftOut(data_pin, clk_pin, bit_order, i, edge)
  else: 
    if (type(data) == str): 
      # Data is a single character here, get ascii value:
      data = ord(data)
      n_bytes = 1
    else:
      # Value is a number, calculate number of bytes:
      if (data == 0):
        # int.bit_length(0) returns 0:
        n_bytes = 1
      else: 
        n_bytes = int(math.ceil(data.bit_length()/8.0))

    # Ensure clock is in idle state:
    digitalWrite(clk_pin, HIGH if (edge==FALLING) else LOW)

    byte_range = (n_bytes-1, -1, -1) if (bit_order == MSBFIRST) else (n_bytes,)
    bit_range = (7, -1, -1)if (bit_order == MSBFIRST) else (8,)
    # Shift out the data:
    for i in range(*byte_range):
      byte = data >> (8*i)
      for j in range(*bit_range):
        digitalWrite(data_pin, (byte>>j) & 0x01)
        digitalWrite(clk_pin, LOW if (edge==FALLING) else HIGH)
        digitalWrite(clk_pin, HIGH if (edge==FALLING) else LOW)

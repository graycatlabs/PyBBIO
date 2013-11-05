# gpio.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone GPIO driver

import memory, pinmux
from bbio.util import addToCleanup
from config import *


def pinMode(gpio_pin, direction, pull=0):
  """ Sets given digital pin to input if direction=1, output otherwise.
      'pull' will set the pull up/down resistor if setting as an input:
      pull=-1 for pull-down, pull=1 for pull up, pull=0 for none. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if pinmux.export(gpio_pin):
    addToCleanup(lambda: pinmux.unexport(gpio_pin))
  if (direction == INPUT):
    # Pinmux:
    if (pull > 0): pull = CONF_PULLUP
    elif (pull < 0): pull = CONF_PULLDOWN
    else: pull = CONF_PULL_DISABLE
    pinmux.pinMux(GPIO[gpio_pin][2], CONF_GPIO_INPUT | pull)
    # Set input:
    memory.orReg(GPIO[gpio_pin][0]+GPIO_OE, GPIO[gpio_pin][1])
    return
  # Pinmux:
  pinmux.pinMux(GPIO[gpio_pin][2], CONF_GPIO_OUTPUT)
  # Set output:
  memory.clearReg(GPIO[gpio_pin][0]+GPIO_OE, GPIO[gpio_pin][1])

def digitalWrite(gpio_pin, state):
  """ Writes given digital pin low if state=0, high otherwise. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (state):
    memory.setReg(GPIO[gpio_pin][0]+GPIO_SETDATAOUT, GPIO[gpio_pin][1])
  else:
    memory.setReg(GPIO[gpio_pin][0]+GPIO_CLEARDATAOUT, GPIO[gpio_pin][1])

def toggle(gpio_pin):
  """ Toggles the state of the given digital pin. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  memory.xorReg(GPIO[gpio_pin][0]+GPIO_DATAOUT, GPIO[gpio_pin][1])

def digitalRead(gpio_pin):
  """ Returns input pin state as 1 or 0. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (memory.getReg(GPIO[gpio_pin][0]+GPIO_DATAIN) & GPIO[gpio_pin][1]):
    return 1
  return 0

def pinState(gpio_pin):
  """ Returns the state of a digital pin if it is configured as
      an output. Returns None if it is configuredas an input. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (memory.getReg(GPIO[gpio_pin][0]+GPIO_OE) & GPIO[gpio_pin][1]):
    return None
  if (memory.getReg(GPIO[gpio_pin][0]+GPIO_DATAOUT) & GPIO[gpio_pin][1]):
    return HIGH
  return LOW

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

"""
 PyBBIO - bbio.py - v0.2
 Created: 12/2011
 Author: Alexander Hiam - ahiam@marlboro.edu - www.alexanderhiam.com
 Website: https://github.com/alexanderhiam/PyBBIO

 A Python library for hardware IO support on the TI Beaglebone.
 At the moment it is quite limited, only providing API for simple
 digital IO functionality. I have big plans for this, however, so
 keep checking the github page for updates.

 Copyright (c) 2012 - Alexander Hiam

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License

 ************************************************************************
 * Having trouble reading/writing analog registers; getting bus errors. *
 * Running Python verbosely gives no additional details.                *
 * Able to read/write the GPIO0 registers just fine, which are at a     *
 * lower address than the ADC, and other GPIOs are at higher addresses. *
 * Output of dmseg after trying to read ADC_CTRL register:              *********************
 *  [128816.761898] Unhandled fault: external abort on non-linefetch (0x1018) at 0x40785040 *
 ********************************************************************************************
"""

import struct, os, sys
from time import sleep
from mmap import mmap

# Load global configuration:
CONFIG_FILE="%s/.pybbio/beaglebone.cfg" % os.environ['HOME']
config = open(CONFIG_FILE, 'r').read()
assert ('MMAP_OFFSET' in config) and ('MMAP_SIZE' in config),\
      "*Config file '%s' must contain values MMAP_OFFSET and MMAP_SIZE" %\
                                                                CONFIG_FILE
exec(config)

# Create global mmap:
f = open("/dev/mem", "r+b")
__mmap = mmap(f.fileno(), MMAP_SIZE, offset=MMAP_OFFSET)
f.close() # Only needed to make map


def run(setup, main):
  """ The main loop; must be passed a setup and a main function.
      First the setup function will be called once, then the main
      function wil be continuously until a stop signal is raised, 
      e.g. CTRL-C or a call to the stop() function from within the
      main function. """
  try:
    _init()
    setup()
    while (True):
      main()
  except KeyboardInterrupt:
    # Manual exit signal, clean up and exit happy
    cleanup()
  except Exception, e:
    # Something may have gone wrong, clean up and print exception
    cleanup()
    print e
      
def stop():
  """ Preffered way for a program to stop itself. """
  raise KeyboardInterrupt # Expected happy stop condition in run()

def _init():
  """ Pre-run initialization, i.e. starting module clocks, etc. """
  _analog_init()
  
def _analog_init():
  """ Initializes the on-board 8ch 12bit ADC. """
  step_config = 'ADCSTEPCONFIG%i'
  #step_delay = 'ADCSTEPDELAY%i'
  ain = 'AIN%i' 
  
  # Enable ADC module clock:
  _setReg(CM_WKUP_ADC_TSC_CLKCTRL, MODULEMODE_ENABLE)
  # Wait for enable complete:
  while (_getReg(CM_WKUP_ADC_TSC_CLKCTRL) & IDLEST_MASK): time.sleep(0.1)
  
  # Must turn off write protect:
  _andReg(ADC_CTRL, ADC_STEPCONFIG_WRITE_PROTECT(0))
  # Write STEPCONFIG registers:
  for i in xrange(8):
    config = SEL_INP(eval(ain % i)) | ADC_AVG4
    print "%s: %s" % (step_config % (i+1),hex(eval(step_config % (i+1))+MMAP_OFFSET))
    print "ADC step config: %s" % bin(config)
    _andReg(eval(step_config % (i+1)), config)
  # Now we can enable ADC subsystem:
  _setReg(ADC_CTRL, TSC_ADC_SS_ENABLE)

def cleanup():
  """ Post-run cleanup, i.e. stopping module clocks, etc. """
  # Disable ADC subsystem:
  _andReg(ADC_CTRL, ~TSC_ADC_SS_ENABLE)
  # Disable ADC module clock:
  _andReg(CM_WKUP_ADC_TSC_CLKCTRL, ~MODULEMODE_ENABLE)
  __mmap.close()

def pinMode(gpio_pin, direction):
  """ Sets given digital pin to input if direction=1, output otherwise. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (direction):
    reg = _getReg(GPIO[gpio_pin][0]+GPIO_OE)
    _setReg(GPIO[gpio_pin][0]+GPIO_OE, reg | GPIO[gpio_pin][1])
    return
  reg = _getReg(GPIO[gpio_pin][0]+GPIO_OE)
  _setReg(GPIO[gpio_pin][0]+GPIO_OE, reg & ~GPIO[gpio_pin][1])

def digitalWrite(gpio_pin, state):
  """ Writes given digital pin low if state=0, high otherwise. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (state):
    reg = _getReg(GPIO[gpio_pin][0]+GPIO_DATAOUT)
    _setReg(GPIO[gpio_pin][0]+GPIO_DATAOUT, reg | GPIO[gpio_pin][1])
    return
  reg = _getReg(GPIO[gpio_pin][0]+GPIO_DATAOUT)
  _setReg(GPIO[gpio_pin][0]+GPIO_DATAOUT, reg & ~GPIO[gpio_pin][1])

def analogRead(analog_pin):
  """ Returns analog value read on given analog input pin. """
  assert (analog_pin in ADC), "*Invalid analog pin: '%s'" % analog_pin
  analog_pin = ADC[analog_pin]
  assert ((analog_pin >= 0) and (analog_pin <= 7)), "*Invalid analog pin" 
  return _getReg(ADC_FIFO0DATA)&ADC_FIFO_MASK

def digitalRead(gpio_pin):
  """ Returns pin state as 1 or 0. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  return _getReg(GPIO[gpio_pin][0]+GPIO_DATAIN) & GPIO[gpio_pin][1]

def toggle(gpio_pin):
  """ Toggles the state of the given digital pin. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  reg = _getReg(GPIO[gpio_pin][0]+GPIO_DATAOUT)
  _setReg(GPIO[gpio_pin][0]+GPIO_DATAOUT, reg ^ GPIO[gpio_pin][1])

def _andReg(address, mask):
  """ Sets 32-bit Register at address to its current value AND mask. """
  _setReg(address, _getReg(address)&mask)

def _orReg(address, mask):
  """ Sets 32-bit Register at address to its current value OR mask. """
  _setReg(address, _getReg(address)|mask)

def _xorReg(address, mask):
  """ Sets 32-bit Register at address to its current value XOR mask. """
  _setReg(address, _getReg(address)^mask)

def _getReg(address):
  """ Returns unpacked 32 bit register value starting from address. """
  return struct.unpack("<L", __mmap[address:address+4])[0]

def _setReg(address, new_value):
  """ Sets 32 bits at given address to given value. """
  __mmap[address:address+4] = struct.pack("<L", new_value)

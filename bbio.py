"""
 PyBBIO - bbio.py - rev 0.1
 Created: 12/2011
 Author: Alexander Hiam - ahiam@marlboro.edu - http://www.alexanderhiam.com
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
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>. 
"""

import struct, os, sys, time
from mmap import mmap

CONFIG_FILE="%s/.pybbio/bbio.cfg" % os.environ['HOME']

_configuration = open(CONFIG_FILE, 'r').read()
assert ('MMAP_OFFSET' in _configuration) and ('MMAP_SIZE' in _configuration),\
           "*Config file '%s' must contain values MMAP_OFFSET and MMAP_SIZE" %\
                                                                     CONFIG_FILE
exec(_configuration)

class BeagleBone(object):
  def __init__(self):
    f = open("/dev/mem", "r+b")
    self.mem = mmap(f.fileno(), MMAP_SIZE, offset=MMAP_OFFSET) 
    f.close() # Only needed to make map
    #self._analog_init()

  def pinMode(self, gpio_pin, direction):
    """ Sets given digital pin to input if direction=1, output otherwise. """
    if (direction):
      reg = self._getReg(gpio_pin[0]+GPIO_OE)
      self._setReg(gpio_pin[0]+GPIO_OE, reg | gpio_pin[1])
      return
    reg = self._getReg(gpio_pin[0]+GPIO_OE)
    self._setReg(gpio_pin[0]+GPIO_OE, reg & ~gpio_pin[1])

  def analogRead(self, analog_pin):
    """ Returns analog value read on given analog input pin. """
    assert ((analog_pin >= 0) and (analog_pin <= 7)), "*Invalid analog pin" 
    return self._getReg(ADC_FIFO0DATA)&ADC_FIFO_MASK

  def digitalWrite(self, gpio_pin, state):
    """ Writes given digital pin low if state=0, high otherwise.  """
    if (state):
      reg = self._getReg(gpio_pin[0]+GPIO_DATAOUT)
      self._setReg(gpio_pin[0]+GPIO_DATAOUT, reg | gpio_pin[1])
      return
    reg = self._getReg(gpio_pin[0]+GPIO_DATAOUT)
    self._setReg(gpio_pin[0]+GPIO_DATAOUT, reg & ~gpio_pin[1])

  def digitalRead(self, gpio_pin):
    """ Returns pin state as 1 or 0. """
    return self._getReg(gpio_pin[0]+GPIO_DATAIN) & gpio_pin[1]

  def toggle(self, gpio_pin):
    """ Toggles the state of the given digital pin. """
    reg = self._getReg(gpio_pin[0]+GPIO_DATAOUT)
    self._setReg(gpio_pin[0]+GPIO_DATAOUT, reg ^ gpio_pin[1])

  def _andReg(self, address, mask):
    """ Sets 32-bit Register at address to its current value AND mask. """
    self._setReg(address, self._getReg(address)&mask)

  def _orReg(self, address, mask):
    """ Sets 32-bit Register at address to its current value OR mask. """
    self._setReg(address, self._getReg(address)|mask)

  def _xorReg(self, address, mask):
    """ Sets 32-bit Register at address to its current value XOR mask. """
    self._setReg(address, self._getReg(address)^mask)

  def _getReg(self, address):
    """ Returns unpacked 32 bit register value starting from address. """
    print "_setReg got:\n addres: %s\n offset: %s" % (hex(address+MMAP_OFFSET), hex(address))
    return struct.unpack("<L", self.mem[address:address+4])[0]

  def _setReg(self, address, new_value):
    """ Sets 32 bits at given address to given value. """
    print "_setReg got:\n addres: %s\n new_value: %i" % (hex(address+MMAP_OFFSET),new_value)
    self.mem[address:address+4] = struct.pack("<L", new_value)

  def _analog_init(self):
    """ Initializes the on-board 8ch 12bit ADC. """
    step_config = 'ADCSTEPCONFIG%i'
    #step_delay = 'ADCSTEPDELAY%i'
    ain = 'AIN%i' 
    print "ADC_CTRL: %s" % bin(self._getReg(ADC_CTRL))
    # Must turn off write protect:
    #self._andReg(ADC_CTRL, ADC_STEPCONFIG_WRITE_PROTECT(0))
    #for i in xrange(8):
    #  config = SEL_INP(eval(ain % i)) | ADC_AVG4
    #  print "%s: %s" % (step_config % (i+1),hex(eval(step_config % (i+1))+MMAP_OFFSET))
    #  print "ADC step config: %s" % bin(config)
    #  self._andReg(eval(step_config % (i+1)), config)
      

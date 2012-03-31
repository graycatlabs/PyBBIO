"""
 PyBBIO - bbio.py - v0.3.1
 Created: 12/2011
 Author: Alexander Hiam - ahiam@marlboro.edu - www.alexanderhiam.com
 Website: https://github.com/alexanderhiam/PyBBIO

 A Python library for hardware IO support on the TI Beaglebone.
 Currently only supporting basic digital and analog IO, but more 
 peripheral support is on the way, so keep checking the Github page
 for updates.

 16-bit register support mod from sbma44 - https://github.com/sbma44

 Copyright 2012 Alexander Hiam

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import struct, os, sys, time
try:
  from mmap import mmap
except:
  print "\n mmap module not found; to install:\n\
   # opkg update && opkg install python-mmap\n"
  sys.exit(0)

# Load global configuration:
CONFIG_FILE="%s/.pybbio/beaglebone.cfg" % os.environ['HOME']
config = open(CONFIG_FILE, 'r').read()
assert ('MMAP_OFFSET' in config) and ('MMAP_SIZE' in config),\
      "*Config file '%s' must contain values MMAP_OFFSET and MMAP_SIZE" %\
                                                                CONFIG_FILE
exec(config)

sys.path.append(LIBRARIES_PATH)

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
  # Must turn off STEPCONFIG write protect:
  _andReg(ADC_CTRL, ADC_STEPCONFIG_WRITE_PROTECT(0))
  # Set STEPCONFIG1-STEPCONFIG8 to correspond to ADC inputs 0-7:
  for i in xrange(8):
    config = SEL_INP(ain % i) | ADC_AVG4 # Average 4 readings
    _andReg(eval(step_config % (i+1)), config)
  # Now we can enable ADC subsystem, re-enabling write protect:
  _setReg(ADC_CTRL, TSC_ADC_SS_ENABLE)

def cleanup():
  """ Post-run cleanup, i.e. stopping module clocks, etc. """
  _analog_cleanup()

def _analog_cleanup():
  # Disable ADC subsystem:
  _clearReg(ADC_CTRL, TSC_ADC_SS_ENABLE)
  # Disable ADC module clock:
  _clearReg(CM_WKUP_ADC_TSC_CLKCTRL, MODULEMODE_ENABLE)
  __mmap.close()

def delay(ms):
  """ Sleeps for given number of milliseconds. """
  time.sleep(ms/1000.0)

def delayMicroseconds(us):
  """ Sleeps for given number of microseconds > ~30; still working 
      on a more accurate method. """
  t = time.time()
  while (((time.time()-t)*1000000) < us): pass

def pinMode(gpio_pin, direction):
  """ Sets given digital pin to input if direction=1, output otherwise. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (direction):
    _orReg(GPIO[gpio_pin][0]+GPIO_OE, GPIO[gpio_pin][1])
    return
  _clearReg(GPIO[gpio_pin][0]+GPIO_OE, GPIO[gpio_pin][1])

def digitalWrite(gpio_pin, state):
  """ Writes given digital pin low if state=0, high otherwise. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (state):
    _orReg(GPIO[gpio_pin][0]+GPIO_DATAOUT, GPIO[gpio_pin][1])
    return
  _clearReg(GPIO[gpio_pin][0]+GPIO_DATAOUT, GPIO[gpio_pin][1])

def analogRead(analog_pin):
  """ Returns analog value read on given analog input pin. """
  assert (analog_pin in ADC), "*Invalid analog pin: '%s'" % analog_pin
  _orReg(ADC_STEPENABLE, ADC_ENABLE(analog_pin))
  while(_getReg(ADC_STEPENABLE) & ADC_ENABLE(analog_pin)): pass
  return _getReg(ADC_FIFO0DATA)&ADC_FIFO_MASK

def digitalRead(gpio_pin):
  """ Returns pin state as 1 or 0. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  if (_getReg(GPIO[gpio_pin][0]+GPIO_DATAIN) & GPIO[gpio_pin][1]):
    return 1
  return 0

def toggle(gpio_pin):
  """ Toggles the state of the given digital pin. """
  assert (gpio_pin in GPIO), "*Invalid GPIO pin: '%s'" % gpio_pin
  _xorReg(GPIO[gpio_pin][0]+GPIO_DATAOUT, GPIO[gpio_pin][1])

def _andReg(address, mask, length=32):
  """ Sets 16 or 32 bit Register at address to its current value AND mask. """
  _setReg(address, _getReg(address, length)&mask, length)

def _orReg(address, mask, length=32):
  """ Sets 16 or 32 bit Register at address to its current value OR mask. """
  _setReg(address, _getReg(address, length)|mask, length)

def _xorReg(address, mask, length=32):
  """ Sets 16 or 32 bit Register at address to its current value XOR mask. """
  _setReg(address, _getReg(address, length)^mask, length)

def _clearReg(address, mask, length=32):
  """ Clears mask bits in 16 or 32 bit register at given address. """
  _andReg(address, ~mask, length)

def _getReg(address, length=32):
  """ Returns unpacked 16 or 32 bit register value starting from address. """
  if (length == 32):
    return struct.unpack("<L", __mmap[address:address+4])[0]
  elif (length == 16):
    return struct.unpack("<H", __mmap[address:address+2])[0]
  else:
    raise ValueError("Invalid register length: %i - must be 16 or 32" % length)

def _setReg(address, new_value, length=32):
  """ Sets 16 or 32 bits at given address to given value. """
  if (length == 32):
    __mmap[address:address+4] = struct.pack("<L", new_value)
  elif (length == 16):
    __mmap[address:address+2] = struct.pack("<H", new_value)
  else:
    raise ValueError("Invalid register length: %i - must be 16 or 32" % length)

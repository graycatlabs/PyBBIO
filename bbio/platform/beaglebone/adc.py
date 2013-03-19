
from memory import *
from config import *


def analog_init():
  """ Initializes the on-board 8ch 12bit ADC. """
  # Enable ADC module clock, though should already be enabled on
  # newer Angstrom images:
  setReg(CM_WKUP_ADC_TSC_CLKCTRL, MODULEMODE_ENABLE)
  # Wait for enable complete:
  while (getReg(CM_WKUP_ADC_TSC_CLKCTRL) & IDLEST_MASK): delay(1)

  # Software reset:
  setReg(ADC_SYSCONFIG, ADC_SOFTRESET)
  while(getReg(ADC_SYSCONFIG) & ADC_SOFTRESET): pass

  # Make sure STEPCONFIG write protect is off:
  setReg(ADC_CTRL, ADC_STEPCONFIG_WRITE_PROTECT_OFF)

  # Set STEPCONFIG1-STEPCONFIG8 to correspond to ADC inputs 0-7:
  for i in xrange(8):
    config = SEL_INP('AIN%i' % i) | ADC_AVG2
    setReg(eval('ADCSTEPCONFIG%i' % (i+1)), config)
    setReg(eval('ADCSTEPDELAY%i' % (i+1)), SAMPLE_DELAY(15))
  # Now we can enable ADC subsystem, leaving write protect off:
  orReg(ADC_CTRL, TSC_ADC_SS_ENABLE)


def analog_cleanup():
  # Software reset:
  setReg(ADC_SYSCONFIG, ADC_SOFTRESET)
  while(getReg(ADC_SYSCONFIG) & ADC_SOFTRESET): pass

  # When I started writing PyBBIO on an older Angstrom image, the ADC
  # was not enabled on boot, so I had these lines to shut it back off:
  # Disable ADC subsystem:
  #_clearReg(ADC_CTRL, TSC_ADC_SS_ENABLE)
  # Disable ADC module clock:
  #_clearReg(CM_WKUP_ADC_TSC_CLKCTRL, MODULEMODE_ENABLE)
  # Newer images enable the ADC module at boot, so we just leave it 
  # running.


def analogRead(analog_pin):
  """ Returns analog value read on given analog input pin. """
  assert (analog_pin in ADC), "*Invalid analog pin: '%s'" % analog_pin

  if (getReg(CM_WKUP_ADC_TSC_CLKCTRL) & IDLEST_MASK):
    # The ADC module clock has been shut off, e.g. by a different 
    # PyBBIO script stopping while this one was running, turn back on:
    analog_init() 

  # Enable sequncer step that's set for given input:
  setReg(ADC_STEPENABLE, ADC_ENABLE(analog_pin))
  # Sequencer starts automatically after enabling step, wait for complete:
  while(getReg(ADC_STEPENABLE) & ADC_ENABLE(analog_pin)): pass
  # Return 12-bit value from the ADC FIFO register:
  return getReg(ADC_FIFO0DATA) & ADC_FIFO_MASK

def inVolts(adc_value, bits=12, vRef=1.8):
  """ Converts and returns the given ADC value to a voltage according
      to the given number of bits and reference voltage. """
  return adc_value*(vRef/2**bits)

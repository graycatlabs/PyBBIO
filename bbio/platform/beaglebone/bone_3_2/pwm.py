# pwm.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone PWM driver for kernel < 3.8


import memory, pinmux
from bbio.util import delay
from config import *


def pwm_init():
  # Enable EHRPWM module clocks:
  memory.setReg(CM_PER_EPWMSS1_CLKCTRL, MODULEMODE_ENABLE)
  # Wait for enable complete:
  while (memory.getReg(CM_PER_EPWMSS1_CLKCTRL) & IDLEST_MASK): delay(1)
  memory.setReg(CM_PER_EPWMSS2_CLKCTRL, MODULEMODE_ENABLE)
  # Wait for enable complete:
  while (memory.getReg(CM_PER_EPWMSS2_CLKCTRL) & IDLEST_MASK): delay(1)

def pwm_cleanup():
  # Disable all PWM outputs:
  for i in PWM_PINS.keys():
    pwmDisable(i)
  # Could disable EHRPWM module clocks here to save some power when
  # PyBBIO isn't running, but I'm not really worried about it for the 
  # time being.

def analogWrite(pwm_pin, value, resolution=RES_8BIT):
  """ Sets the duty cycle of the given PWM output using the
      given resolution. """
  # Make sure the pin is configured:
  pwmEnable(pwm_pin)
  try:
    assert resolution > 0, "*PWM resolution must be greater than 0"
    if (value < 0): value = 0
    if (value >= resolution): value = resolution-1
    freq = int(pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_FREQ]))
    period_ns = (1e9/freq)
    # Todo: round values properly!: 
    duty_ns = int(value * (period_ns/resolution))
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_DUTY], str(duty_ns))
    # Enable output:
    if (pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_ENABLE]) == '0\n'):
      pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_ENABLE], '1') 
  except IOError:
    print "*PWM pin '%s' reserved by another process!" % pwm_pin

# For those who don't like calling a digital signal analog:
pwmWrite = analogWrite

def pwmFrequency(pwm_pin, freq_hz):
  """ Sets the frequncy in Hertz of the given PWM output's module. """
  assert (pwm_pin in PWM_PINS), "*Invalid PWM pin: '%s'" % pwm_pin
  assert freq_hz > 0, "*PWM frequency must be greater than 0"
  # Make sure the pin is configured:
  pwmEnable(pwm_pin)
  # calculate the duty cycle in nanoseconds for the new period:
  old_duty_ns = int(kernelFileIO(PWM_FILES[pwm_pin][PWM_DUTY]))
  old_period_ns = 1e9/int(kernelFileIO(PWM_FILES[pwm_pin][PWM_FREQ]))
  duty_percent = old_duty_ns / old_period_ns
  new_period_ns = 1e9/freq_hz
  # Todo: round values properly!:
  new_duty_ns = int(duty_percent * new_period_ns)

  try: 
    # Duty cyle must be set to 0 before changing frequency:
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_DUTY], '0')
    # Set new frequency:
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_FREQ], str(freq_hz))
    # Set the duty cycle:
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_DUTY], str(new_duty_ns))
  except IOError:
    print "*PWM pin '%s' reserved by another process!" % pwm_pin
  
def pwmEnable(pwm_pin):
  """ Ensures given PWM output is reserved for userspace use and 
      sets proper pinmux. Sets frequency to default value if output
      not already reserved. """
  assert (pwm_pin in PWM_PINS), "*Invalid PWM pin: '%s'" % pwm_pin
  # Set pinmux mode:
  pinmux.pinMux(PWM_PINS[pwm_pin][0], PWM_PINS[pwm_pin][1])
  if ('sysfs' not in pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_REQUEST])):
    # Reserve use of output:
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_REQUEST], '1')
    delay(1) # Give it some time to take effect
    # Make sure output is disabled, so it won't start outputing a 
    # signal until analogWrite() is called: 
    if (pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_ENABLE]) == '1\n'):
      pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_ENABLE], '0')
    # Duty cyle must be set to 0 before changing frequency:
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_DUTY], '0')
    # Set frequency to default:
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_FREQ], str(PWM_DEFAULT_FREQ))

def pwmDisable(pwm_pin):
  """ Disables PWM output on given pin. """
  assert (pwm_pin in PWM_PINS), "*Invalid PWM pin: '%s'" % pwm_pin
  # Disable PWM output:
  if (pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_ENABLE]) == '1\n'):
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_ENABLE], '0')
  # Relinquish userspace control:
  if ('sysfs' in pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_REQUEST])):
    pinmux.kernelFileIO(PWM_FILES[pwm_pin][PWM_REQUEST], '0')

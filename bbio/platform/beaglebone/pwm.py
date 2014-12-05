# pwm.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone PWM driver for kernel >= 3.8

from bbio.platform.beaglebone import cape_manager
from bbio.platform.util import sysfs
from bbio.common import delay, addToCleanup
from config import RES_8BIT, PWM_PINS, PWM_PERIOD, PWM_DUTY, PWM_POLARITY,\
                   PWM_RUN, PWM_DEFAULT_PERIOD

PWM_PINS_ENABLED = {}

def pwm_init():
  pass

def pwm_cleanup():
  pass

def analogWrite(pwm_pin, value, resolution=RES_8BIT, polarity=0):
  """ Sets the duty cycle of the given PWM output using the
      given resolution. If polarity=0 this will set the width of
      the positive pulse, otherwise it will set the width of the
      negative pulse. """
  # Make sure the pin is configured:
  pwmEnable(pwm_pin)
  pin_config = PWM_PINS[pwm_pin]
  helper_path = pin_config[1]
  try:
    assert resolution > 0, "*PWM resolution must be greater than 0"
    if (value < 0): value = 0
    if (value >= resolution): value = resolution-1
    period_ns = int(sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_PERIOD)))
    # Todo: round values properly!: 
    duty_ns = int(value * (period_ns/resolution))
    sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_DUTY), str(duty_ns))
    if polarity == 0:
      sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_POLARITY), '0')
    else:
      sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_POLARITY), '1')
    # Enable output:
    if (sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_RUN)) == '0\n'):
      sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_RUN), '1') 
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
  pin_config = PWM_PINS[pwm_pin]
  helper_path = pin_config[1]

  old_duty_ns = int(sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_DUTY)))
  old_period_ns = int(sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_PERIOD)))

  duty_percent = old_duty_ns / old_period_ns
  new_period_ns = int(1e9/freq_hz)
  # Todo: round values properly!:
  new_duty_ns = int(duty_percent * new_period_ns)

  try: 
    # Duty cyle must be set to 0 before changing frequency:
    sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_DUTY), '0')
    # Set new frequency:
    sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_PERIOD), str(new_period_ns))
    # Set the duty cycle:
    sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_DUTY), str(new_duty_ns))
  except IOError:
    print "*PWM pin '%s' reserved by another process!" % pwm_pin
    # that's probably not the best way to handle this error...
  
def pwmEnable(pwm_pin):
  """ Ensures PWM module for the given pin is enabled and its ocp helper
      is loaded. """
  global PWM_PINS_ENABLED
  if PWM_PINS_ENABLED.get(pwm_pin): return
  pin_config = PWM_PINS[pwm_pin]
  assert (pin_config), "*Invalid PWM pin: '%s'" % pwm_pin

  for overlay in pin_config[2]:
    cape_manager.load(overlay, auto_unload=False)
    delay(250) # Give it some time to take effect
  cape_manager.load(pin_config[0], auto_unload=False)
  delay(250)

  helper_path = pin_config[1]
  # Make sure output is disabled, so it won't start outputing a 
  # signal until analogWrite() is called: 
  if (sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_RUN)) == '1\n'):
    sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_RUN), '0')

  # Duty cyle must be set to 0 before changing frequency:
  sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_DUTY), '0')
  # Is this still true??

  sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_PERIOD), 
                      str(PWM_DEFAULT_PERIOD))
  addToCleanup(lambda : pwmDisable(pwm_pin))
  PWM_PINS_ENABLED[pwm_pin] = True


def pwmDisable(pwm_pin):
  """ Disables PWM output on given pin. """
  pin_config = PWM_PINS[pwm_pin]
  assert (pin_config), "*Invalid PWM pin: '%s'" % pwm_pin
  helper_path = pin_config[1]
  sysfs.kernelFileIO('%s/%s' % (helper_path, PWM_RUN), '0')
  PWM_PINS_ENABLED[pwm_pin] = False

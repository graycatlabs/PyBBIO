"""
 Servo - v0.1
 Copyright 2012 Alexander Hiam

 Library for controlling servo motors with the BeagleBone's PWM pins.
"""

from bbio import *

class Servo(object):
  def __init__(self, pwm_pin=None, pwm_freq=50, min_ms=0.5, max_ms=2.4):
    assert (pwm_freq > 0), "pwm_freq must be positive, given: %s" %\
                          str(pwm_freq)    
    assert (min_ms > 0), "0 min_ms must be positive, given: %s" %\
                          str(min_ms)
    assert (max_ms > 0), "max_ms must be positive, given: %s" %\
                          str(max_ms)
    self.pwm_freq = pwm_freq
    self.min_ms = min_ms
    self.max_ms = max_ms
    self.pwm_pin = None
    if (pwm_pin): self.attach(pwm_pin)
    self.angle = None

  def attach(self, pwm_pin):
    """ Attach servo to PWM pin; alternative to passing PWM pin to
        __init__(). Can also be used to change pins. """
    if (self.pwm_pin):
      # Already attached to a pin, detach first
      self.detach()
    self.pwm_pin = pwm_pin

    pwmFrequency(self.pwm_pin, self.pwm_freq)
    self.period_ms = 1000.0/self.pwm_freq

  def write(self, angle):
    """ Set the angle ofthe servo in degrees. """
    if (angle < 0): angle = 0
    if(angle > 180): angle = 180
    value = (self.max_ms-self.min_ms)/180.0 * angle + self.min_ms
    analogWrite(self.pwm_pin, value, self.period_ms)
    self.angle= angle

  def read(self):
    """ return the current angle of the servo, or None if it has not
        yet been set. """
    return self.angle

  def detach(self):
    """ Detaches the servo so so pin can be used for normal PWM 
        operation. """
    if (not self.pwm_pin): return
    pwmDisable(self.pwm_pin)
    self.pwm_pin = None
    self.angle = None

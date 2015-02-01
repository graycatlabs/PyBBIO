'''
eQEP - v0.1
Copyright 2014 Rekha Seethamraju

Library for controlling rotary encoder with the Beaglebone Black's eQEP pins.

eQEP is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
'''
import os
from bbio.platform.util import sysfs
from bbio.platform.beaglebone import cape_manager
from bbio import addToCleanup, delay
from bbio.platform.beaglebone.config import OCP_PATH

class RotaryEncoder(object):
  _eqep_dirs = [
    '%s/48300000.epwmss/48300180.eqep' % OCP_PATH,
    '%s/48302000.epwmss/48302180.eqep' % OCP_PATH,
    '%s/48304000.epwmss/48304180.eqep' % OCP_PATH
  ]
  EQEP0 = 0
  EQEP1 = 1
  EQEP2 = 2
  EQEP2b = 3
    
  def __init__(self, eqep_num):
    '''
    RotaryEncoder(eqep_num)
    Creates an instance of the class RotaryEncoder. 
    eqep_num determines which eQEP pins are set up. 
    eqep_num can be: EQEP0, EQEP1, EQEP2 or EQEP2b based on which pins \
    the rotary encoder is connected to.
    '''
    assert 0 <= eqep_num <= 3 , "eqep_num must be between 0 and 3"
    if eqep_num == 3:
        overlay = "PyBBIO-eqep2b"
    	eqep_num = 2
    else:
    	overlay = 'PyBBIO-eqep%i' % eqep_num

    pwmss_overlay = "PyBBIO-epwmss%i" % eqep_num
    cape_manager.load(pwmss_overlay, auto_unload=False)
    delay(10)
    cape_manager.load(overlay, auto_unload=False)
    delay(250) # Give driver time to load 
    self.base_dir = self._eqep_dirs[eqep_num]
    self.enable()
    addToCleanup(self.disable)
    
  def enable(self):
    '''
    enable()
    Turns the eQEP hardware ON
    '''
    enable_file = "%s/enabled" % self.base_dir
    return sysfs.kernelFileIO(enable_file, 1) 
    
  def disable(self):
    '''
    disable()
    Turns the eQEP hardware OFF
    '''
    enable_file = "%s/enabled" % self.base_dir
    return sysfs.kernelFileIO(enable_file, 0)

  def setAbsolute(self):
    '''
    setAbsolute()
    Set mode as Absolute
    The position starts at zero and is incremented or 
    decremented by the encoder's movement
    '''
    mode_file = "%s/mode" % self.base_dir
    return sysfs.kernelFileIO(mode_file, 0)
    
  def setRelative(self):
    '''
    setRelative()
    Set mode as Relative
    The position is reset when the unit timer overflows.
    '''
    mode_file = "%s/mode" % self.base_dir
    return sysfs.kernelFileIO(mode_file, 1)
    
  def getMode(self):
    '''
    getMode()
    Returns the mode the eQEP hardware is in.
    '''
    mode_file = "%s/mode" % self.base_dir
    return sysfs.kernelFileIO(mode_file)

  def getPosition(self):
    '''
    getPosition()
    Get the current position of the encoder.
    In absolute mode, this attribute represents the current position 
    of the encoder. 
    In relative mode, this attribute represents the position of the 
    encoder at the last unit timer overflow.
    '''
    position_file = "%s/position" % self.base_dir
    return sysfs.kernelFileIO(position_file)
    
  def setFrequency(self,freq):
    '''
    setFrequency(freq)
    Set the frequency in Hz at which the driver reports new positions.
    '''
    period_file = "%s/period" % self.base_dir
    return sysfs.kernelFileIO(period_file,1000000000/freq)
    
  def setPosition(self,val):
    ''' 
    setPosition(value)
    Give a new value to the current position
    '''
    position_file = "%s/position" % self.base_dir
    return sysfs.kernelFileIO(position_file,val)
    
  def zero(self):
    '''
    zero()s
    Set the current position to 0
    '''
    return self.setPosition(0)
    
    

  
    
    
    

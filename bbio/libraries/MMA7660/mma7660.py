'''
MMA7660 - v0.1
Copyright 2014 Rekha Seethamraju

Library for controlling temperature sensor, MMA7660 with the Beaglebone Black's
I2C pins.

ADT7310 is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
'''

from bbio import *

class MMA7660(object):
  MMA7660_ADDR = 0x4C
  REG_X = 0x00
  REG_Y = 0x01
  REG_Z = 0x02
  REG_TILT = 0x03
  REG_SRST = 0x04
  REG_SPCNT = 0x05
  REG_INTSU = 0x06
  REG_MODE = 0x07
  REG_SR = 0x08
  REG_PDET = 0x09
  REG_PD = 0x0A
  MODE_STAND_BY = 0x00
  MODE_ACTIVE = 0x01
  SRATE_16 = 0x03
  SRATE_120 = 0x00
  SR_FLIT = 2<<5
  PD_TAP_THRESH = 0x14
  PDET_TAP_X = 0<<5
  PDET_TAP_Y = 0<<6
  PDET_TAP_Z = 1<<7
  PDET_TH = 6
  #To be used to set up interrupts
  INT_FB = 1 
  INT_PL = 1<<1
  INT_PD = 1<<2
  INT_SHX = 1<<5
  INT_SHY = 1<<6
  INT_SHZ = 1<<7
  
  def __init__(self,i2c_no):
    '''
    MMA7660(i2c_no)
    Creates an instance of the class MMA7660
    i2c_no can be 1 or 2 based on the i2c bus used
    '''
    assert 1 <= i2c_no <= 2, "i2c_no must be between 1 or 2"
    self.i2c_no = i2c_no
    if i2c_no == 1:
      self.i2cdev = Wire1
    if i2c_no == 2:
      self.i2cdev = Wire2
    self.int_pin = None 
    self.i2cdev.begin()
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,self.SRATE_120 | self.SR_FLIT)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PD,self.PD_TAP_THRESH)
    pdet = self.PDET_TH | self.PDET_TAP_X | self.PDET_TAP_Y | self.PDET_TAP_Z
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PDET,pdet)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)  
    addToCleanup(self.close)
    
  def getX(self):
    '''
    getX()
    Returns the value of X dimension. 
    Value of X can be from -31 to 32 
    '''
    x = self.i2cdev.read(self.MMA7660_ADDR,self.REG_X)
    while(x>>6==1):
      x = self.i2cdev.read(self.MMA7660_ADDR,self.REG_X)
    x = ((x<<2)-128)/4
    return x
    
  def getY(self):
    '''
    getY()
    Returns the value of Y dimension. 
    Value of Y can be from -31 to 32 
    '''
    y = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Y)
    while(y>>6==1):
      y = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Y)
    y = ((y<<2)-128)/4
    return y

  def getZ(self):
    '''
    getZ()
    Returns the value of Z dimension. 
    Value of Z can be from -31 to 32 
    '''
    z = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Z)
    while(z>>6==1):
      z = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Z)
    z = ((z<<2)-128)/4
    return z
    
  def getXYZ(self):
    '''
    getXYZ()
    Returns a list of X,Y and Z dimension values.
    Values of X, Y and Z can be from -31 to 32
    '''
    xyz = self.i2cdev.read(0x4c,0x00,3)
    return list(map(lambda x : ((x<<2)-128)/4,xyz))
    
  def setInterrupt(self, cfg, pin, callback):
    '''
    setInterrupt(configuration, interrupt_pin, callback_funtion)
    Sets interrupt on interrupt_pin and calls callback_funtion when interrupt occurs
    configuration : INT_FB - Front/Back position change causes an interrupt
                    INT_PL - Up/Down/Right/Left position change causes interrupt
                    INT_PD - Successful tap detection causes an interrupt
                    INT_SHX - Shake detected on the X-axis causes an interrupt
                    INT_SHY - Shake detected on the Y-axis causes an interrupt
                    INT_SHZ - Shake detected on the Z-axis causes an interrupt
    callback_funtion : has to take(back_front, portrait_landscape, tap, shake) 
                       as parameters.
                       back_front = 1 - Front: Equipment is lying on its front
                       back_front = 2 - Back: Equipment is lying on its back
                       
                       portrait_landscape = 1 - Left: Equipment is in landscape
                                                mode to the left
                       portrait_landscape = 2 - Right: Equipment is in landscape
                                                mode to the right
                       portrait_landscape = 5 - Down: Equipment standing 
                                                vertically in inverted orientation
                       portrait_landscape = 6 - Up: Equipment standing vertically
                                                in normal orientation
                       
                       tap = 0 - Tap Not Detected
                       tap = 1 - Tap Detected
                       
                       shake = 0 - Shake Not Detected
                       shake = 1 - Shake Detected
    '''
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_INTSU,cfg)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE) 
    self.usr_callback = callback
    self.int_pin = pin
    pinMode(self.int_pin, INPUT, PULLUP)
    attachInterrupt(self.int_pin, self._int_callback)
    
  def settapthreshold(self, value):
    '''
    settapthreshold(value)
    sets tap detection threshold
    Tap detection threshold = +/-value counts
    '''
    assert 0 <= value <= 31, "tap detection threshold must be between 0 and 31"
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PDET,value)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
  
  def settiltfilter(self, value):
    '''
    settiltfilter(value)
    Sets the rate of tilt debounce filtering
    When value = 0 - Tilt debounce filtering is disabled.
    For other values, value number of samples have to match before 
    the device updates portrait/ landscape data.
    '''
    assert 0 <= value <= 8, "Tilt debounce filtering must be between 0 and 8"
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,value)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)		
  
  def setTapDebounce(self, value):
    '''
    setTapDebounce(value)
    Sets the tap detection debounce filtering to value
    The tap detection debounce filtering requires value adjacent tap detection 
    tests to be the same to trigger a tap event
    '''
    assert 0 <= value <= 256, "tap detection debounce filter must be between \
                              0 and 256"
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PD,value)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
  
  def getOrientation(self):
    '''
    getOrientation()
    returns a list with the back_front and portrait_landscape data.
    
    back_front = 1 - Front: Equipment is lying on its front
    back_front = 2 - Back: Equipment is lying on its back
                       
    portrait_landscape = 1 - Left: Equipment is in landscape mode to the left
    portrait_landscape = 2 - Right: Equipment is in landscape mode to the right
    portrait_landscape = 5 - Down: Equipment standing vertically in 
                                   inverted orientation
    portrait_landscape = 6 - Up: Equipment standing vertically in normal orientation
    '''
    status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    while((status&0x40)>>6==1):
      status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    back_front = (status&0x03)
    portrait_landscape = (status&0x1C)>>2
    return [back_front, portrait_landscape]
  
  def _int_callback(self):
    '''
    _int_callback()
    Internal function to read status of interrupt
    '''
    status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    while((status&0x40)>>6==1):
      status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    back_front = (status&0x03)
    portrait_landscape = (status&0x1C)>>2
    tap = (status&0x20)>>5
    shake = (status&0x80)>>7
    self.usr_callback(back_front, portrait_landscape, tap, shake)
    
  def removeInterrupt(self):
    '''
    removeInterrupt()
    Detaches the interrupt
    '''
    if self.int_pin:
      detachInterrupt(self.int_pin)
      
  def close(self):
    '''
    close()
    sets the device in standby mode and closes the connection to the device.
    '''
    self.removeInterrupt()
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.end()
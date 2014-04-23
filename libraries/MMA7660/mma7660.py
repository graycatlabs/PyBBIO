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
  INT_FB = 1 
  INT_PL = 1<<1
  INT_PD = 1<<2
  INT_SHX = 1<<5
  INT_SHY = 1<<6
  INT_SHZ = 1<<7
  
  def __init__(self,i2c_no):
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
    x = self.i2cdev.read(self.MMA7660_ADDR,self.REG_X)
    while(x>>6==1):
      x = self.i2cdev.read(self.MMA7660_ADDR,self.REG_X)
    x = ((x<<2)-128)/4
    return x
    
  def getY(self):
    y = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Y)
    while(y>>6==1):
      y = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Y)
    y = ((y<<2)-128)/4
    return y

  def getZ(self):
    z = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Z)
    while(z>>6==1):
      z = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Z)
    z = ((z<<2)-128)/4
    return z
    
  def getXYZ(self):
    xyz = self.i2cdev.read(0x4c,0x00,3)
    return list(map(lambda x : ((x<<2)-128)/4,xyz))
    
  def setInterrupt(self, cfg, pin, callback):
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_INTSU,cfg)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE) 
    self.usr_callback = callback
    self.int_pin = pin
    pinMode(self.int_pin, INPUT, PULLUP)
    attachInterrupt(self.int_pin, self._int_callback)
    
  def settapthreshold(self, value):
    assert 0 <= value <= 31, "tap detection threshold must be between 0 and 31"
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PDET,value)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
  
  def settiltfilter(self, value):
    assert 0 <= value <= 8, "Tilt debounce filtering must be between 0 and 8"
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,value)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)		
  
  def setTapDebounce(self, value):
    assert 0 <= value <= 256, "tap detection debounce filter must be between \
                              0 and 256"
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PD,value)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
  
  def getOrientation(self):
    status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    while((status&0x40)>>6==1):
      status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    back_front = (status&0x03)
    portrait_landscape = (status&0x1C)>>2
    return [back_front, portrait_landscape]
  
  def _int_callback(self):
    status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    while((status&0x40)>>6==1):
      status = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    back_front = (status&0x03)
    portrait_landscape = (status&0x1C)>>2
    tap = (status&0x20)>>5
    shake = (status&0x80)>>7
    self.usr_callback(back_front, portrait_landscape, tap, shake)
    
  def removeInterrupt(self):
    if self.int_pin:
      detachInterrupt(self.int_pin)
      
  def close(self):
    self.removeInterrupt()
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.end()
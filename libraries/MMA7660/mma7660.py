from bbio import *
class MMA7660(object):

  MMA7660_ADDR = 0x4c
  REG_X = 0x00
  REG_Y = 0x01
  REG_Z = 0x02
  REG_TILT = 0x03
  REG_SRST = 0x04
  REG_SPCNT = 0x05
  REG_INTSU = 0x06
  REG_MODE = 0x07
  REG_SR = 0x08
  REG_TAP = 0x09
  MODE_STAND_BY = 0x00
  MODE_ACTIVE = 0x01
  RATE_ASLEEP_16 = 0x03

  def __init__(self,i2c_no):
    assert 1 <= i2c_no <= 2, "i2c_no must be between 1 or 2"
    self.i2c_no = i2c_no
    if i2c_no == 1:
      self.i2cdev = Wire1
    if i2c_no == 2:
      self.i2cdev = Wire2
    self.i2cdev.begin()
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,self.RATE_ASLEEP_16)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
    
  def getX(self):
    x = self.i2cdev.read(self.MMA7660_ADDR,self.REG_X)
    while(self.i2cdev.read(self.MMA7660_ADDR,self.REG_X)>>6==1):
      x = self.i2cdev.read(self.MMA7660_ADDR,self.REG_X)
    x = ((x<<2)-128)/4
    return x
    
  def getY(self):
    y = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Y)
    while(self.i2cdev.read(self.MMA7660_ADDR,self.REG_Y)>>6==1):
      y = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Y)
    y = ((y<<2)-128)/4
    return y

  def getZ(self):
    z = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Z)
    while(self.i2cdev.read(self.MMA7660_ADDR,self.REG_Z)>>6==1):
      z = self.i2cdev.read(self.MMA7660_ADDR,self.REG_Z)
    z = ((z<<2)-128)/4
    return z
    
    
    
    
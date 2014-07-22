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
    assert 1 <= i2c_no < 2, "i2c_no must be between 1 or 2"
    self.i2c_no = i2c_no
    if i2c_no == 1:
      self.i2cdev = Wire1
    if i2c_no == 2:
      self.i2cdev = Wire2
    i2cdev.begin()
    i2cdev.write(REG_MODE,MODE_STAND_BY)
    i2cdev.write(REG_SR,RATE_ASLEEP_16)
    i2cdev.write(REG_MODE,MODE_ACTIVE)
    
  def getX(self):
    x = i2cdev.read(MMA7660_ADDR,REG_X)
    while(i2cdev.read(MMA7660_ADDR,REG_X)>=64):
      x = i2cdev.read(MMA7660_ADDR,REG_X)
    x = x<<2
    return x
    
  def getY(self):
    y = i2cdev.read(MMA7660_ADDR,REG_Y)
    while(i2cdev.read(MMA7660_ADDR,REG_Y)>=64):
      y = i2cdev.read(MMA7660_ADDR,REG_Y)
    y = y<<2
    return y

  def getZ(self):
    z = i2cdev.read(MMA7660_ADDR,REG_Z)
    while(i2cdev.read(MMA7660_ADDR,REG_Z)>=64):
      z = i2cdev.read(MMA7660_ADDR,REG_Z)
    z = z<<2
    return z
    
    
    
    
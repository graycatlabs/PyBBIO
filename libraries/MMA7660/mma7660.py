#to do : docstrings
# tap enables on x,y and z

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
  REG_PDET = 0x09
  REG_PD = 0x0A
  MODE_STAND_BY = 0x00
  MODE_ACTIVE = 0x01
  RATE_16 = 0x03
  RATE_120 = 0x00
  INT_TAP = 1<<2

  def __init__(self,i2c_no):
    assert 1 <= i2c_no <= 2, "i2c_no must be between 1 or 2"
    self.i2c_no = i2c_no
    if i2c_no == 1:
      self.i2cdev = Wire1
    if i2c_no == 2:
      self.i2cdev = Wire2
    self.i2cdev.begin()
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,self.RATE_16)
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
    


  def setTap(self,tap_count = 1):
    assert 0<tap_count<256 , "tap_count must be between 1 and 255"
    TAP_THRESH = 0x00
    TAP_X = 1<<5
    TAP_Y = 1<<6
    TAP_Z = 1<<7
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,self.RATE_120)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_INTSU,self.INT_TAP)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PD,tap_count-1)
    pdet = TAP_THRESH | TAP_X | TAP_Y | TAP_Z
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_PDET,pdet)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
    
  def detectTap(self):
    tap = 0
    while(self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)>>6==1):
      tap = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT&0x20)
    tap = tap>>5
    return tap
    
  def setOrientation(self,orient_debounce=1):
    assert 0<orient_debounce<8 , "orient_debounce must be between 1 and 8"
    flit = (orient_debounce+1)<<6 | self.RATE_120
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,flit)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
    
  def getOrientation(self):
    orient = 0
    while(self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)>>6==1):
      orient = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT&0x20)
    pola = orient&0x1C
    bafro = orient&0x03
    if pola == 1:
      print "Orientation : Left: Equipment is in landscape mode to the left"
    elif pola == 2:
      print "Orientation : Right: Equipment is in landscape mode to the right"
    elif pola == 5:
      print "Orientation : Down: Equipment standing vertically in inverted orientation"
    elif pola == 6:
      print "Orientation : Up: Equipment standing vertically in normal orientation"
    if bafro == 1 :
      print "Orientation : Front: Equipment is lying on its front"
    elif bafro == 2:
      print "Orientation : Back: Equipment is lying on its back"
   
  def setShake(self):
    SHAKE_X = 1<<7
    SHAKE_Y = 1<<6
    SHAKE_Z = 1<<5
    shake = SHAKE_X | SHAKE_Y | SHAKE_Z
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,self.RATE_120)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_INTSU,shake)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)

  def getShake(self):
    shake = 0
    while(self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)>>6==1):
      shake = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT&0x80)>>7
    return shake
    
    
    
    
    

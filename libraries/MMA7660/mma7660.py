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
  SRATE_16 = 0x03
  SRATE_120 = 0x00
  SR_FLIT = 2<<5
  INT_TAP = 1<<2
  PD_TAP_THRESH = 0x14
  PDET_TAP_X = 0<<5
  PDET_TAP_Y = 0<<6
  PDET_TAP_Z = 1<<7
  PDET_TH = 6

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
    self.int_pin = None
    
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
    


  def setTapAlarm(self,int_pin,callabck):
    self._setAlarm(int_pin,callabck) 
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_INTSU,self.INT_TAP)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)
    
 
  def detectTap(self):
    tap = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    print "TAP I: "+str(tap)
    while((tap&0x40)>>6==1):
      tap = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    tap = (tap&0x20)>>5
    return tap
    

  def getOrientation(self):
    orient = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    while((orient&0x40)>>6==1):
      orient = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    pola = (orient&0x1C)>>2
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
   
  def setShakeAlarm(self,int_pin,callabck):
    self._setAlarm(int_pin,callabck) 
    SHAKE_X = 1<<7
    SHAKE_Y = 1<<6
    SHAKE_Z = 1<<5
    shake = SHAKE_X | SHAKE_Y | SHAKE_Z
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_STAND_BY)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_SR,self.SRATE_120)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_INTSU,shake)
    self.i2cdev.write(self.MMA7660_ADDR,self.REG_MODE,self.MODE_ACTIVE)

  def getShake(self):
    shake = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    print "Shake I: "+str(shake)
    while((shake&0x40)>>6==1):
      shake = self.i2cdev.read(self.MMA7660_ADDR,self.REG_TILT)
    shake = (shake&0x80)>>7
    return shake
    
  def _setAlarm(self,int_pin,callback):
    self._removeAlarm()
    self.int_pin = int_pin
    pinMode(self.int_pin, INPUT, PULLUP)
    attachInterrupt(self.int_pin,callback,FALLING) 
    
  def _removeAlarm(self):
    if self.int_pin:
      detachInterrupt(self.int_pin)
    
    
    
    
    

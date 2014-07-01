from bbio import *

class ADT7310(object):

  def __init__(self, spi_no, cs):
    assert 0 <= spi_no < 2, "spi_no must be between 0 or 1"
    assert 0 <= cs < 2, "cs must be between 0 or 1"
    if spi_no == 0:
      self.spidev = SPI0
    else:
      self.spidev = SPI1
    self.cs = cs
    self.spidev.begin()
    self.spidev.setDataMode(self.cs,3)
    
  def getTemp(self):
    '''
    getTemp()
    Reads the temperature value
    '''
    self.spidev.write(self.cs,0x54)
    _t = self.spidev.read(self.cs,2)
    if ( _t[0] & 128 == 0):
      temp = (((_t[0]<<8)+_t[1])>>3)/16
    else:
      temp = ((((_t[0]<<8)+_t[1])>>3)-4096)/16
    return temp

  def convertTemp(self,temp):
    '''
    convertTemp(temp)
    converts the temp to a 2 byte value msb first
    '''
    t = list()
    t.insert(0,temp>>8)
    t.insert(1,temp & 0xff)
    return t    
        
  def setLowTemp(self,temp):
    '''
    setLowTemp(temp)
    Sets the Low Temperature below which the Interrupt pin will activate
    '''
    t = self.convertTemp(temp)
    self.spidev.write(self.cs,[0x30,t[0],t[1]])
    
  def setHighTemp(self,temp):
    '''
    setHighTemp(temp)
    Sets the High Temperature above which the Interrupt pin will activate.
    '''
    t = self.convertTemp(temp)
    self.spidev.write(self.cs,[0x38,t[0],t[1]])
    
  def setCriticalTemp(self,temp):
    '''
    setCriticalTemp(temp)
    Sets the Critical Temperature below which the CT pin will activate.
    '''
    t = self.convertTemp(temp)
    self.spidev.write(self.cs,[0x20,t[0],t[1]])
    
  def setAlarm(self, int_pin , callback):
    '''
    setAlarm(int_pin , callback)
    Sets the int_pin to an interrupt pin ot CT pin and calls callback() 
        when interrupt or critical over temperature event occurs as required.
    '''
    self.removeAlarm(int_pin)
    self.spidev.write(self.cs,[0x08,0x00])
    pinMode(int_pin, INPUT, PULLUP)
    attachInterrupt( int_pin , callback, FALLING)
    
  def removeAlarm(self,int_pin):
    '''
    removeAlarm(int_pin )
    Removes interrupt on int_pin.
    '''
    detachInterrupt(int_pin)
    
   #Interrupt active low adn; set up critical like this? 
    
  
    
    
    
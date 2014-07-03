from bbio import *

class ADT7310(object):
  # Setting up bit values in command register - refer to table 15 
  # in datasheet
  CMD_READ          = (1<<6)
  CMD_WRITE         = 0x0
  CMD_CONTINUOUS    = (1<<2)
  ADDR_CONFIG       = (0x01<<3)
  ADDR_TEMP         = (0x02<<3)
  ADDR_LOW_TEMP     = (0x07<<3)
  ADDR_HIGH_TEMP    = (0x06<<3)
  ADDR_HYST_TEMP    = (0x05<<3)
  ADDR_CRT_TEMP     = (0x04<<3)
  CONFIG_COMPARATOR = (0x01<<4)

  def __init__(self, spi_no, cs):
    assert 0 <= spi_no < 2, "spi_no must be between 0 or 1"
    assert 0 <= cs < 2, "cs must be between 0 or 1"
    if spi_no == 0:
      self.spidev = SPI0
    else:
      self.spidev = SPI1
    self.alarm_pin = None
    self.critical_pin = None
    self.cs = cs
    self.spidev.begin()
    self.spidev.setDataMode(self.cs,3)
    self.spidev.write(self.cs,[0xff,0xff,0xff,0xff])
    delay(1)
    self.spidev.write(self.cs,[0x50])
    delay(1)
    self._continuous = False
    addToCleanup(self.end)
    
    
  def getTemp(self):
    '''
    getTemp()
    Reads the temperature value
    '''
    if self._continuous == False:
      self.spidev.write(self.cs, [self.CMD_READ | self.ADDR_TEMP | \
                      self.CMD_CONTINUOUS])
      self._continuous == True
    _t = self.spidev.read(self.cs,2)
    if ( _t[0] & 128 == 0):
      temp = (((_t[0]<<8)+_t[1])>>3)/16
    else:
      temp = ((((_t[0]<<8)+_t[1])>>3)-4096)/16
    return temp
    
  def _exitContinuous(self):
    if self._continuous == True:
      self.spidev.write(self.cs,[0x50])
      self._continuous = False

  def _encodeTemp(self,temp):
    '''
    _encodeTemp(temp)
    encodes the temp to a 2 byte value msb first
    '''
    return [temp>>8,temp & 0xff]   
        
  def setLowTemp(self,temp):
    '''
    setLowTemp(temp)
    Sets the Low Temperature below which the Interrupt pin will activate
    '''
    t = self._encodeTemp(temp)
    self._exitContinuous()
    self.spidev.write(self.cs,[self.CMD_WRITE | self.ADDR_LOW_TEMP] + \
                       self._encodeTemp(temp))
    
  def setHighTemp(self,temp):
    '''
    setHighTemp(temp)
    Sets the High Temperature above which the Interrupt pin will activate.
    '''
    self._exitContinuous()
    self.spidev.write(self.cs,[self.CMD_WRITE | self.ADDR_HIGH_TEMP] + \
                       self._encodeTemp(temp))
    
  def setCriticalTemp(self,temp):
    '''
    setCriticalTemp(temp)
    Sets the Critical Temperature below which the CT pin will activate.
    '''
    self._exitContinuous()
    t = self._encodeTemp(temp)
    self.spidev.write(self.cs, [self.CMD_WRITE | self.ADDR_CRT_TEMP]+\
                      self._encodeTemp(temp))
    
  def setHystTemp(self,temp):
    '''
    setCriticalTemp(temp)
    Sets the Critical Temperature below which the CT pin will activate.
    '''
    self._exitContinuous()
    t = self._encodeTemp(temp)
    self.spidev.write(self.cs, [self.CMD_WRITE | self.ADDR_HYST_TEMP]+\
                      self._encodeTemp(temp))

  def enableAlarm(self):
    '''
    enableAlarm()
    enables the Comparator mode for interrupts.
    '''
    self._exitContinuous()
    self.spidev.write(self.cs,[self.CMD_WRITE | self.ADDR_CONFIG] +\
                [self.CONFIG_COMPARATOR])
    
  def setAlarm(self, pin, callback, return_callback=None):
    '''
    setAlarm(alarm_pin , callback, (optional)return_callback)
    Sets the alarm_pin to an interrupt pin and calls callback() 
    when interrupt occurs as required.
    return_callback is called when the temperature falls 
    back below threshold-hysteresis.
    
    '''
    self.removeAlarm()
    self.alarm_pin = pin
    pinMode(self.alarm_pin, INPUT, PULLUP)
    attachInterrupt(self.alarm_pin , callback, FALLING)
    if return_callback!=None:
     attachInterrupt(self.alarm_pin , return_callback, RISING)
    self.enableAlarm()
  
    
  def setCriticalAlarm(pin, callback, return_callback=None):
    '''
    setCriticalAlarm(alarm_pin , callback, (optional)return_callback)
    Sets the critical_pin to be an interrupt and calls callback() 
    when over-temperature event occurs as required.
    return_callback() is optionally called when the temperature falls 
    back below threshold-hysteresis.
    '''
    self.removeCriticalAlarm()
    self.critical_pin = pin
    pinMode(self.critical_pin, INPUT, PULLUP)
    attachInterrupt(self.critical_pin , callback, FALLING)
    if return_callback!=None:
     attachInterrupt(self.critical_pin , return_callback, RISING)
    self.enableAlarm()
    
    
  def removeAlarm(self):
    if self.alarm_pin:
      '''
      removeAlarm()
      Removes alarm on interrupt pin.
      '''
      detachInterrupt(self.alarm_pin)
      
  def removeCriticalAlarm(self):
    if self.critical_pin:
      '''
      removeCriticalAlarm()
      Removes critical alarm on CT pin.
      '''
      detachInterrupt(self.critical_pin)
      
  def end(self):
    self.removeAlarm()
    self.removeCriticalAlarm()
    self.spidev.end()
    self._continuous == False
    
  def read(self, reg):
    self.spidev.write(self.cs,[CMD_READ | reg<<3])
    _t = self.spidev.read(self.cs,2)
    self._exitContinuous()
    if ( _t[0] & 128 == 0):
      temp = (((_t[0]<<8)+_t[1])>>3)/16
    else:
      temp = ((((_t[0]<<8)+_t[1])>>3)-4096)/16
    return temp
    
'''
ADT7310 - v0.1
Copyright 2014 Rekha Seethamraju

Library for controlling temperature sensor, ADT7310 with 
the Beaglebone Black's SPI pins.

ADT7310 is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
'''
from bbio import *
class ADT7310(object):
  CONFIG_COMPARATOR = (1<<4)
  CONFIG_CONTINUOUS = (0b00<<6)
  CONFIG_SHUTDOWN = (0b11<<6)
  CONFIG_13BIT = (0 << 7)
  CMD_READ = 0b01000000
  CMD_WRITE = 0b0000000
  CMD_CONTINUOUS = (1<<2)
  R_CONFIGURATION = 0x01<<3
  R_TEMP = (0x02<<3)
  R_ID = (0x03<<3)
  R_CRIT = (0x04<<3)  
  R_HYST = (0x05<<3)
  R_HIGH = (0x06<<3)
  R_LOW = (0x07<<3)
  _continuous = False

  def __init__(self,spi_no,cs):
    assert 0 <= spi_no < 2, "spi_no must be between 0 or 1"
    assert 0 <= cs < 2, "cs must be between 0 or 1"
    if spi_no == 0:
      self.spidev = SPI0
    else:
      self.spidev = SPI1
    self.cs = cs
    self.alarm_pin = None
    self.critical_pin = None
    #init spi
    self.spidev.begin()
    self.spidev.setDataMode(self.cs,3)
    self.reset()
    self.spidev.write(self.cs,[self.CMD_WRITE | self.R_CONFIGURATION]+\
                      [self.CONFIG_COMPARATOR])
    self._continuous = False
    addToCleanup(self.close)
    
  def close(self):
    '''
    close()
    removes alarms if set and closes the SPI connection
    '''
    self.removeAlarm()
    self.removeCriticalAlarm()
    self.spidev.end()
    self._continuous == False

  def reset(self):
    '''
    reset()
    resets the sensor to default values.
    '''
    self.spidev.write(self.cs,[0xff,0xff,0xff,0xff])
    delay(1)
  
  def getTempinC(self):
    '''
    getTempinC()
    Returns the 13-bit temperature value in Celsius 
    '''
    if self._continuous == False:
      self.spidev.write(self.cs, [self.CMD_READ | self.R_TEMP | \
                        self.CMD_CONTINUOUS])
      self._continuous = True
    _t = self.spidev.read(self.cs,2)
    if ( _t[0] & 128 == 0):
      temp = (((_t[0]<<8)+_t[1])>>3)/16.0
    else:
      temp = ((((_t[0]<<8)+_t[1])>>3)-8192)/16.0
    delay(240)
    return temp
    
  def getTempinF(self):
    '''
    getTempinF()
    Returns the 13-bit temperature value in Fahrenheit 
    '''
    return getTempinC()*33.8
    
  
  def _encodeTemp(self,temp):
    '''
    _encodeTemp(temp)
    encodes the temp to a 2 byte value msb first
    '''
    if (temp<0):
      temp = temp*128
    else:
      temp = temp*128 + 65536
    return [temp >> 8]+[temp & 0xff]
  
  def setHighTemp(self,temp):
    '''
    setHighTemp(temp)
    Sets the High Temperature above which the Interrupt pin will activate.
    '''
    self.spidev.write(self.cs,[self.CMD_WRITE | self.R_HIGH]+\
                      self._encodeTemp(temp))
    self._continuous = False
  
  def setLowTemp(self,temp):
    '''
    setLowTemp(temp)
    Sets the Low Temperature below which the Interrupt pin will activate
    '''
    self.spidev.write(self.cs,[self.CMD_WRITE | self.R_LOW]+\
                      self._encodeTemp(temp))
    self._continuous = False
  
  def setHystTemp(self,temp):
    '''
    setHystTemp(temp)
    Sets the Hystersis Temperature below which determines the tolerance.
    Must be between 0 and 15 C
    '''
    self.spidev.write(self.cs,[self.CMD_WRITE | self.R_HYST]+\
                      self._encodeTemp(temp))
    self._continuous = False
  
  def setCriticalTemp(self,temp):
    '''
    setCriticalTemp(temp)
    Sets the Critical Temperature below which the CT pin will activate.
    '''
    self.spidev.write(self.cs,[self.CMD_WRITE | self.R_CRIT]+\
                      self._encodeTemp(temp))
    self._continuous = False
  
  def read(self, reg):
    assert 0 <= cs < 8, "register values must be between 0 and 7"
    self.spidev.write(self.cs,[CMD_READ | reg<<3])
    _t = self.spidev.read(self.cs,2)
    if ( _t[0] & 128 == 0):
      temp = (((_t[0]<<8)+_t[1])>>3)/16
    else:
      temp = ((((_t[0]<<8)+_t[1])>>3)-4096)/16
    return temp
  
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
    attachInterrupt(self.alarm_pin, callback, FALLING)
    if return_callback!=None:
      attachInterrupt(self.alarm_pin, return_callback, RISING)

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

  def removeAlarm(self):
    '''
    removeAlarm()
    Removes alarm on interrupt pin.
    '''
    if self.alarm_pin:
      detachInterrupt(self.alarm_pin)
    
  def removeCriticalAlarm(self):
    '''
    removeCriticalAlarm()
    Removes critical alarm on CT pin.
    '''
    if self.critical_pin:
      detachInterrupt(self.critical_pin)
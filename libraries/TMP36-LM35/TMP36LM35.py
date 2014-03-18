"""
 Servo - v0.1
 Copyright 2012 Alexander Hiam

 Library for reading the values of TMP36/LM35 temperature sensors.
"""

from bbio import *

class TMP36LM35(object):
  def __init__(self, data_pin=None):
    
    self.data_pin = data_pin

  def readTempC(self):
    """ Gets the sensor data in Celsius """
    return ((analogRead(self.data_pin)*3.3)/1024) # 3.3 for the gpio pin it's max volt are 3.3 V


  def readTempF(self):
    """ Return the sensor data in Fahrenheit """
    tempC = ((analogRead(self.data_pin)*3.3)/1024) # 3.3 for the gpio pin it's max volt are 3.3 V
    return ((tempC * 9.0/5.0) + 32)

 
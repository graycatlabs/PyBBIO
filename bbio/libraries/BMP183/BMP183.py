"""
BMP183
Copyright 2015 - Alexander Hiam <alex@graycat.io>

A PyBBIO library for controlling BMP183 SPI pressure/temperature sensors.

BMP183 is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
"""
import bbio

class BMP183(object):
  ID_VALUE = 0x55
    
  REG_ID         = 0xd0
  REG_SOFT_RESET = 0xe0
  REG_CTRL_MEAS  = 0xf4
  REG_OUT_MSB    = 0xf6
  REG_OUT_LSB    = 0xf7
  REG_OUT_XLSB   = 0xf8

  CMD_TEMPERATURE      = 0x2e
  CMD_PRESSURE         = 0x34
  CMD_PRESSURE_OSS_INC = 0x40

  TEMP_CONVERSION_TIME      = 4.5 
  PRESSURE_CONVERSION_TIMES = [4.5, 7.5, 13.5, 25.5]
  
  OVERSAMPLE_0 = 0
  OVERSAMPLE_1 = 1
  OVERSAMPLE_2 = 2
  OVERSAMPLE_3 = 3

  def __init__(self, spi, cs=0):
    self.spi = spi
    self.cs = cs
    spi.begin()
    spi.setClockMode(0, 0)
    spi.setMaxFrequency(0, 3000000)
    id_val = self.readRegister(self.REG_ID)[0]
    assert id_val == self.ID_VALUE, "BMP183 not detected on SPI bus"
        
    def fromUnsigned16(bytes):
      """ Convert register values as unsigned short int """
      return bytes[0]<<8 | bytes[1]

    def fromSigned16(bytes):
      """ Convert register values as signed short int """
      x = fromUnsigned16(bytes)
      if x > 32767: return -(65536-x)
      return x
    # Read calibration coefficients:
    self.cal_AC1 = fromSigned16(self.readRegister(0xaa, 2))
    self.cal_AC2 = fromSigned16(self.readRegister(0xac, 2))
    self.cal_AC3 = fromSigned16(self.readRegister(0xae, 2))
    self.cal_AC4 = fromUnsigned16(self.readRegister(0xb0, 2))
    self.cal_AC5 = fromUnsigned16(self.readRegister(0xb2, 2))
    self.cal_AC6 = fromUnsigned16(self.readRegister(0xb4, 2))
    self.cal_B1 = fromSigned16(self.readRegister(0xb6, 2))
    self.cal_B2 = fromSigned16(self.readRegister(0xb8, 2))
    self.cal_MB = fromSigned16(self.readRegister(0xba, 2))
    self.cal_MC = fromSigned16(self.readRegister(0xbc, 2))
    self.cal_MD = fromSigned16(self.readRegister(0xbe, 2))

  def getTemp(self, return_b5_coefficient=False):
    """ Returns current temperature in Celsius. """
    self.writeRegister(self.REG_CTRL_MEAS, self.CMD_TEMPERATURE) 
    bbio.delay(self.TEMP_CONVERSION_TIME)
    msb, lsb = self.readRegister(self.REG_OUT_MSB, 2)
    val = (msb << 8) | lsb

    # Conversions are straight out of the datasheet
    x1 = (val - self.cal_AC6) * self.cal_AC5 / 32768
    x2 = self.cal_MC * 2048 / (x1 + self.cal_MD)
    b5 = x1 + x2
    temp_counts = (b5 + 8) / 16
    temp = temp_counts * 0.1 # 0.1 degree C resolution
    if return_b5_coefficient:
      return (temp, b5)
    return temp
        
  def getTempF(self):
    """ Returns current temperature in Fahrenheit. """
    tempC = self.readTemp()
    return tempC * 9./5 + 32
        
  def getPressure(self, oversampling=OVERSAMPLE_0):
    """ Returns the current pressure in Pascals. The optional parameter 
        'oversampling' can be given as one of OVERSAMPLE_1, OVERSAMPLE_2,
        or OVERSAMPLE_3 for averaging of 2, 4 or 8 samples respectively. """
    assert self.OVERSAMPLE_0 <= oversampling <= self.OVERSAMPLE_3, \
        "unsupported oversample value"

    temp, b5 = self.getTemp(return_b5_coefficient=True)
        
    offset = self.CMD_PRESSURE_OSS_INC * oversampling
    cmd = self.CMD_PRESSURE + offset
    self.writeRegister(self.REG_CTRL_MEAS, cmd) 
    bbio.delay(self.PRESSURE_CONVERSION_TIMES[oversampling])
    msb, lsb, xlsb = self.readRegister(self.REG_OUT_MSB, 3)
    val = ((msb<<16) | (lsb<<8) | xlsb) >> (8-oversampling)
    
    # Conversions are straight out of the datasheet
    b6 = b5-4000
    x1 = (self.cal_B2 * (b6*b6 / 4096)) / 2048
    x2 = self.cal_AC2 * b6 / 2048
    x3 = x1+x2
    b3 = (((self.cal_AC1*4+x3) << oversampling) + 2) / 4
    x1 = self.cal_AC3 * b6 / 8192
    x2 = (self.cal_B1 * (b6*b6 / 4096)) / 65536
    x3 = ((x1 + x2) + 2) / 4
    b4 = self.cal_AC4 * (x3 + 32768) / 32768
    b7 = (val - b3) * (50000 >> oversampling)
    if (b7 < 1<<31): p = (b7 * 2) / b4
    else: p = (b7 / b4) * 2
    x1 = (p / 256)**2
    x1 = (x1 * 3038) / 65536
    x2 = (-7357 * p) / 65536
    p += (x1 + x2 + 3791) / 16
    return p
    
  def getPressurePSI(self, oversampling=OVERSAMPLE_0):
    """ Returns the current pressure in PSI. """
    return self.getPressure(oversampling) * 0.000145037738

  def readRegister(self, addr, n_bytes=1):
    """ Reads the value in the given register, or if the optional parameter 
        'n_bytes' is greater than 1 returns n_bytes register values starting 
        at given address. """
    assert n_bytes > 0, "Can't read less than 1 byte!"
    request = [addr | 0x80] + [0]*n_bytes
    response = self.spi.transfer(self.cs, request)
    return response[1:] # slice off value read when writing register

  def writeRegister(self, addr, value):
    """ Writes the given value to the given register. """
    self.spi.write(self.cs, [addr & 0x7f, value & 0xff])


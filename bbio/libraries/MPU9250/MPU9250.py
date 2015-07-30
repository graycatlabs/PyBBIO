"""
MPU9250
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A PyBBIO library for controlling the MPU 9250 9-DOF sensor via SPI.

MPU9250 is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
"""
import bbio

class MPU9250(object):
  ID_VALUE = 0x71  	# precoded identification string in WHOAMI Reg
    
  REG_ID         = 0x75 # WHOAMI
  
  REG_I2C_MST_CTRL  = 0x24
  REG_I2C_SLV0_ADDR = 0x25
  REG_I2C_SLV0_REG  = 0x26
  REG_I2C_SLV0_CTRL = 0x27
  REG_I2C_SLV0_DO   = 0x63
  REG_USER_CTRL     = 0x6A
  
  AK8963_CNTL1 = 0x0A  
  AK8963_CNTL2 = 0x0B  

  REG_TEMP_OUT_H    = 0x41
  REG_TEMP_OUT_L    = 0x42

  CMD_TEMPERATURE      = 0x2e
  CMD_PRESSURE         = 0x34
  CMD_PRESSURE_OSS_INC = 0x40

  TEMP_CONVERSION_TIME      = 4.5 
  PRESSURE_CONVERSION_TIMES = [4.5, 7.5, 13.5, 25.5]
  
  OVERSAMPLE_0 = 0
  OVERSAMPLE_1 = 1
  OVERSAMPLE_2 = 2
  OVERSAMPLE_3 = 3

  RANGE_ACCEL = 16   # Gs
  RANGE_GYRO  = 2000 # dps
  RANGE_MAG   = 4912 # uT

  def __init__(self, spi, cs=0):
    self.spi = spi
    self.cs = cs
    spi.begin()
    spi.setClockMode(0, 0)
    spi.setMaxFrequency(0, 3000000)
    id_val = self.readRegister(self.REG_ID)[0]
    # print "\nGot WHOAMI = 0x%02x" %id_val
    assert id_val == self.ID_VALUE, "MPU9250 not detected on SPI bus"

    #This part is to set up the magnetometer, due to it being a separate device
    self.writeRegister(self.REG_I2C_MST_CTRL, 0x0D) # I2C speed 400 Khz 
    self.writeRegister(self.REG_USER_CTRL, 0x22) #

    # Reset magnetometer 
    self.writeRegister(self.REG_I2C_SLV0_ADDR, 0x0C)
    self.writeRegister(self.REG_I2C_SLV0_REG, self.AK8963_CNTL2)
    self.writeRegister(self.REG_I2C_SLV0_DO, 0x01)
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x81) 
    # Set 16-bit continues MODE1 readouts
    self.writeRegister(self.REG_I2C_SLV0_REG, self.AK8963_CNTL1)
    self.writeRegister(self.REG_I2C_SLV0_DO, 0x12 )
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x81)


  def ak8963Whoami( self):
    """ I2C WhoAmI check for the AK8963 in-built magnetometer """
    
    self.writeRegister(self.REG_I2C_SLV0_ADDR, 0x8C) 
    # READ Flag + 0x0C is AK slave addr
    self.writeRegister(self.REG_I2C_SLV0_REG, 0x00)
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x81)
    whoami_ak = self.readRegister(73, 1)
    print "\nGot WHOAMI for AK8963 = 0x%02x (0x48?) " % whoami_ak[0] 
    assert whoami_ak[0] == 0x48, "AK8963 not detected on internal I2C bus"

  def getAcceleration( self):
    """ Returns current acceleration triplet. """
    msbX, lsbX, msbY, lsbY, msbZ, lsbZ = self.readRegister(59, 6)

    valX = self.fromSigned16([msbX, lsbX]) / 32760.0 * self.RANGE_ACCEL
    valY = self.fromSigned16([msbY, lsbY]) / 32760.0 * self.RANGE_ACCEL
    valZ = self.fromSigned16([msbZ, lsbZ]) / 32760.0 * self.RANGE_ACCEL
    return [valX, valY, valZ]
  
  def getGyro( self):
    """ Returns current acceleration triplet. """
    msbX, lsbX, msbY, lsbY, msbZ, lsbZ = self.readRegister(67, 6)

    valX = self.fromSigned16([msbX, lsbX]) / 32760.0 * self.RANGE_GYRO
    valY = self.fromSigned16([msbY, lsbY]) / 32760.0 * self.RANGE_GYRO
    valZ = self.fromSigned16([msbZ, lsbZ]) / 32760.0 * self.RANGE_GYRO
    return [valX, valY, valZ]
 
  def getMag( self):
    """ Returns current acceleration triplet. """
    # bit more fun since we're reading via internal I2C
    self.writeRegister(self.REG_I2C_SLV0_ADDR, 0x8C)
    self.writeRegister(self.REG_I2C_SLV0_REG, 0x03)
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x87) # read 7
    msbX, lsbX, msbY, lsbY, msbZ, lsbZ, stat2 = self.readRegister(73,7)
         
    valX = self.fromSigned16([msbX, lsbX]) / 32760.0 * self.RANGE_MAG
    valY = self.fromSigned16([msbY, lsbY]) / 32760.0 * self.RANGE_MAG
    valZ = self.fromSigned16([msbZ, lsbZ]) / 32760.0 * self.RANGE_MAG
    return [valX, valY, valZ]
  

  def getTemp(self):
    """ Returns current temperature of sensor die in Celsius. """
    msb, lsb = self.readRegister(self.REG_TEMP_OUT_H, 2)
    val = self.fromSigned16([msb, lsb])

    # Conversions are straight out of the datahsheet
    # TEMP_degC   = ((TEMP_OUT - RoomTemp_Offset) / Temp_Sensitivity) + 21 
    # They fail to mention what RT_Offset or Temp_Sensitivity should equal to
    temp = (( val - 21) / 333.87) + 21;
    
    return temp
        
  def getTempF(self):
    """ Returns current temperature in Fahrenheit. """
    tempC = self.readTemp()
    return tempC * 9./5 + 32
        
    

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


  def fromUnsigned16(self, bytes):
    """ Convert register values as unsigned short int """
    return bytes[0]<<8 | bytes[1]

  def fromSigned16(self, bytes):
    """ Convert register values as signed short int """
    x = self.fromUnsigned16(bytes)
    if x > 32767: return -(65536-x)
    return x


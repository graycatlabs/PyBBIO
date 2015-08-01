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
  
  REG_SMPLRT_DIV    = 0x19
  REG_CONFIG        = 0x18
  REG_GYRO_CONFIG   = 0x1B
  REG_ACCEL_CONFIG1 = 0x1C
  REG_ACCEL_CONFIG2 = 0x1D
  
  REG_FIFO_EN       = 0x23
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



  # Define possible gyro & accel ranges
  RANGE_GYRO_2000DPS  = 3
  RANGE_GYRO_1000DPS  = 2
  RANGE_GYRO_500DPS   = 1
  RANGE_GYRO_250DPS   = 0
  RANGE_ACCEL_16G     = 3
  RANGE_ACCEL_8G      = 2
  RANGE_ACCEL_4G      = 1
  RANGE_ACCEL_2G      = 0

  # Same as above, used for scaling
  SCALE_GYRO  = 250, 500, 1000, 2000
  SCALE_ACCEL = 2, 4, 8, 16

  def __init__(self, spi, cs=0):
    self.spi = spi
    self.cs = cs
    spi.begin()
    spi.setClockMode(0, 0)
    spi.setMaxFrequency(0, 1000000)
    
    # Am I talking to an MPU9250?
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
    

    # Reset gyro and accel configs
    self.writeRegister(self.REG_GYRO_CONFIG, 0x00)
    self.writeRegister(self.REG_ACCEL_CONFIG1, 0x00)
    self.writeRegister(self.REG_ACCEL_CONFIG2, 0x00)
  

    # Set current ranges to max values
  
    self.currentRangeMag    = 4912 # uT; fixed!
    self.setRangeGyro(self.RANGE_GYRO_2000DPS)
    self.setRangeAccel(self.RANGE_ACCEL_16G)

    # Above code does these 
    #self.CurrentRangeGyro   = self.RANGE_GYRO_2000DPS
    #self.CurrentRangeAccel  = self.RANGE_ACCEL_16G
    
    # Done with init() 

  def ak8963Whoami(self):
    """ I2C WhoAmI check for the AK8963 in-built magnetometer """
    self.writeRegister(self.REG_I2C_SLV0_ADDR, 0x8C) 
    # READ Flag + 0x0C is AK slave addr
    self.writeRegister(self.REG_I2C_SLV0_REG, 0x00)
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x81)
    whoami_ak = self.readRegister(73, 1)
    print "\nGot WHOAMI for AK8963 = 0x%02x (0x48?) " % whoami_ak[0] 
    assert whoami_ak[0] == 0x48, "AK8963 not detected on internal I2C bus"

  def setRangeGyro(self, rangeVal):
    """ Sets the readout range for the gyroscope
    Possible values
    rangeVal == self.RANGE_GYRO_\2000DPS\1000DPS\500DPS\250DPS 
    """
    # We only accept rangeVal = 0 to 3
    if (rangeVal < 0 or rangeVal > 3):
      print "\n Invalid RANGE value! Range not changed"
      # @TODO Error handling
      return -1
    else:

      # Preserve previous REG bits
      regOld = self.readRegister(self.REG_GYRO_CONFIG, 1)[0]
      regOld &= ~(0x3<<3) # Clear [3:4] FS bits 
        # Combine regOld and rangeVal shifted to bits [3:4] GYRO_FS_SEL 
      regVal = regOld | (rangeVal<<3)
      self.writeRegister(self.REG_GYRO_CONFIG, regVal)

      gyroConf = self.readRegister(self.REG_GYRO_CONFIG, 1)[0]
      # test if we did it right??
      if (regVal == gyroConf):
        # Update Current range variable
        self.currentRangeGyro = rangeVal
        return 0
      else:
        print "\n WARNING! FAILED TO SET gyroscope range!"
        print "\n\tI've set REG_GYRO_CONFIG to %d, wanted to set to %d" % (
          gyroConf, regVal)
        return -2
        # @TODO Add proper error log

  def setRangeAccel(self, rangeVal):
    """ Sets the readout range for the accelerometer
    Possible values
    rangeVal == self.RANGE_GYRO_\16G\8G\4G\2G 
    """
    # We only accept rangeVal = 0 to 3
    if (rangeVal < 0 or rangeVal > 3):
      print "\n Invalid RANGE value! Range not changed"
      # @TODO Error handling
      return -1
    else: 

      # Preserve previous REG bits
      regOld = self.readRegister(self.REG_ACCEL_CONFIG1, 1)[0]
      regOld &= ~(0x3<<3) # Clear [3:4] FS bits 
        # Combine regOld and rangeVal shifted to bits [3:4] ACCEL_FS_SEL 
      regVal = regOld | (rangeVal<<3) 
      self.writeRegister(self.REG_ACCEL_CONFIG1, regVal)

      accelConf = self.readRegister(self.REG_ACCEL_CONFIG1, 1)[0] 
      # test if we did it right??
      if (regVal == accelConf):
        # Update Current range variable
        self.currentRangeAccel = rangeVal
        return 0
      else:
        print "\n WARNING! FAILED TO SET acceletometer range!"
        print "\n\tI've set REG_ACCEL_CONFIG to %d, wanted to set to %d" % (
          accelConf, regVal)
        return -2
        # @TODO Add proper error log

  
  def getAccel(self):
    """ Returns current acceleration triplet. """
    msbX, lsbX, msbY, lsbY, msbZ, lsbZ = self.readRegister(59, 6)

    scaling = self.SCALE_ACCEL[self.currentRangeAccel] # Get scale value
    valX = self.fromSigned16([msbX, lsbX]) / 32768.0 * scaling
    valY = self.fromSigned16([msbY, lsbY]) / 32768.0 * scaling
    valZ = self.fromSigned16([msbZ, lsbZ]) / 32768.0 * scaling
    return [valX, valY, valZ]
  
  def getGyro(self):
    """ Returns current acceleration triplet. """
    msbX, lsbX, msbY, lsbY, msbZ, lsbZ = self.readRegister(67, 6)

    scaling = self.SCALE_GYRO[self.currentRangeGyro] # Get scale value
    valX = self.fromSigned16([msbX, lsbX]) / 32768.0 * scaling
    valY = self.fromSigned16([msbY, lsbY]) / 32768.0 * scaling
    valZ = self.fromSigned16([msbZ, lsbZ]) / 32768.0 * scaling
    return [valX, valY, valZ]
 
  def getMag( self):
    """ Returns current acceleration triplet. """
    # bit more fun since we're reading via internal I2C
    self.writeRegister(self.REG_I2C_SLV0_ADDR, 0x8C)
    self.writeRegister(self.REG_I2C_SLV0_REG, 0x03)
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x87) # read 7
    msbX, lsbX, msbY, lsbY, msbZ, lsbZ, stat2 = self.readRegister(73,7)
    
    scaling = self.currentRangeMag     
    valX = self.fromSigned16([msbX, lsbX]) / 32768.0 * scaling
    valY = self.fromSigned16([msbY, lsbY]) / 32768.0 * scaling
    valZ = self.fromSigned16([msbZ, lsbZ]) / 32768.0 * scaling
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
        
  def runSelfTest(self):
    """ Initiates self test for gyroscope and accelerometer
        Returns deviation with respect to factory trim values 
    """
   
    # Init sums
    sumAccel = [0] * 200
    sumGyro = [0] * 200
    STSumAccel = [0] * 200
    STSumGyro = [0] * 200


    # Read configs for restoration
    oldRegConf      = self.readRegister(self.REG_CONFIG, 1)[0]
    oldGyroConf     = self.readRegister(self.REG_GYRO_CONFIG, 1)[0]
    oldAccelConf1   = self.readRegister(self.REG_ACCEL_CONFIG1, 1)[0]
    oldAccelConf2   = self.readRegister(self.REG_ACCEL_CONFIG2, 1)[0]

 
    # Set range and sampling rate
          # Set gyro sample rate to 1 kHz
    self.writeRegister(self.REG_SMPLRT_DIV, 0x00) 
          # Set gyro sample rate to 1 kHz and DLPF to 92 Hz
    self.writeRegister(self.REG_CONFIG, 0x02)
          # Set full scale range for the gyro to 250 dps
    self.setRangeGyro(self.RANGE_GYRO_250DPS)
          # Set accelerometer rate to 1 kHz and bandwidth to 92 Hz
    self.writeRegister(self.REG_ACCEL_CONFIG2, 0x02)
          # Set full scale range for the accelerometer to 2 Gs
    self.setRangeAccel(self.RANGE_ACCEL_2G)


    # Get 200 measurements for averaging
    for i in range(200):

      accelX, accelY, accelZ = self.getAccel()
      gyroX, gyroY, gyroZ = self.getGyro()

      sumAccel[0] += accelX
      sumAccel[1] += accelY
      sumAccel[2] += accelZ 
      sumGyro[0]  += gyroX
      sumGyro[1]  += gyroY
      sumGyro[2]  += gyroZ
  
    for i in range(3):
      sumAccel[i] /= 200.0
      sumGyro[i]  /= 200.0


    # print " AVG Accel = %f %f %f | AVG Gyro = %f %f %f" % ( sumAccel[0],sumAccel[1],sumAccel[2],  sumGyro[0], sumGyro[1],sumGyro[2])
 

    # Configure accel & gyro for self-test
      # Enable self test on all three axes and set accel range to +/- 2 g
    self.writeRegister(self.REG_ACCEL_CONFIG1, 0xE0) 
      # Enable self test on all three axes and set gyro range to +/- 250 DPS
    self.writeRegister(self.REG_GYRO_CONFIG,  0xE0)

    # Get 200 self-test measurements for averaging
    for i in range(200):

      accelX, accelY, accelZ = self.getAccel()
      gyroX, gyroY, gyroZ = self.getGyro()

      STSumAccel[0] += accelX
      STSumAccel[1] += accelY
      STSumAccel[2] += accelZ 
      STSumGyro[0]  += gyroX
      STSumGyro[1]  += gyroY
      STSumGyro[2]  += gyroZ
  
    for i in range(3):
      STSumAccel[i] /= 200.0
      STSumGyro[i]  /= 200.0


    # Set things back to normal again (0x00 to gyro & accel config)
    self.writeRegister(self.REG_ACCEL_CONFIG1, 0x00)
    self.writeRegister(self.REG_GYRO_CONFIG, 0x00)

    # Retrieve factory self-test data
    STGyroX, STGyroY, STGyroZ = self.readRegister(0x00, 3)
    STAccelX, STAccelY, STAccelZ = self.readRegister(0x0D, 3)

    FTrimGyro   = [0] * 3
    FTrimAccel  = [0] * 3
    # Compute factory trim values
    FTrimGyro[0] = 2620 * pow( 1.01, STGyroX - 1.0 )
    FTrimGyro[1] = 2620 * pow( 1.01, STGyroY - 1.0 )
    FTrimGyro[2] = 2620 * pow( 1.01, STGyroZ - 1.0 )
    FTrimAccel[0] = 2620 * pow( 1.01, STAccelX - 1.0 )
    FTrimAccel[1] = 2620 * pow( 1.01, STAccelY - 1.0 )
    FTrimAccel[2] = 2620 * pow( 1.01, STAccelZ - 1.0 )

    devGyro   = [0] * 3
    devAccel  = [0] * 3
    # Compute deviations
    for i in range(3):
      devAccel[i] = 100.0 * ( STSumAccel[i] - sumAccel[i]) / FTrimAccel[i]
      devGyro[i] = 100.0 * ( STSumGyro[i] - sumGyro[i]) / FTrimGyro[i]

    
    # Restore old configuration registers
    self.writeRegister(self.REG_CONFIG, oldRegConf)
    self.writeRegister(self.REG_GYRO_CONFIG, oldGyroConf)
    self.writeRegister(self.REG_ACCEL_CONFIG1, oldAccelConf1)
    self.writeRegister(self.REG_ACCEL_CONFIG2, oldAccelConf2)

     
    return devAccel, devGyro   

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


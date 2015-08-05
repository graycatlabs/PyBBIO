"""
MPU9250
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A PyBBIO library for controlling the MPU 9250 9-DOF sensor via SPI.

MPU9250 is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
"""
import bbio
import time

class MPU9250(object):
  
  
  # Set Register addresses  
  
  REG_XG_OFFSET_H   = 0x13  # User-defined trim values for gyroscope
  REG_XG_OFFSET_L   = 0x14
  REG_YG_OFFSET_H   = 0x15
  REG_YG_OFFSET_L   = 0x16
  REG_ZG_OFFSET_H   = 0x17
  REG_ZG_OFFSET_L   = 0x18  
  
  REG_SMPLRT_DIV    = 0x19  # Sample rate divider
  REG_CONFIG        = 0x18  # General & Gyro Config
  REG_GYRO_CONFIG   = 0x1B
  REG_ACCEL_CONFIG1 = 0x1C
  REG_ACCEL_CONFIG2 = 0x1D
 
  REG_INT_ENABLE    = 0x38
  
  REG_FIFO_EN       = 0x23
  REG_I2C_MST_CTRL  = 0x24
  REG_I2C_SLV0_ADDR = 0x25
  REG_I2C_SLV0_REG  = 0x26
  REG_I2C_SLV0_CTRL = 0x27
  REG_I2C_SLV0_DO   = 0x63
  
  REG_USER_CTRL     = 0x6A
  REG_PWR_MGMT_1    = 0x6B # Device defaults to the SLEEP mode
  REG_PWR_MGMT_2    = 0x6C 
  
  AK8963_CNTL1 = 0x0A  
  AK8963_CNTL2 = 0x0B  

  REG_TEMP_OUT_H    = 0x41
  REG_TEMP_OUT_L    = 0x42

  REG_FIFO_COUNTH   = 0x72
  REG_FIFO_COUNTL   = 0x73
  REG_FIFO_R_W      = 0x74

  REG_XA_OFFSET_H   = 0x77  # User-defined trim values for accelerometer
  REG_XA_OFFSET_L   = 0x78
  REG_YA_OFFSET_H   = 0x7A
  REG_YA_OFFSET_L   = 0x7B
  REG_ZA_OFFSET_H   = 0x7D
  REG_ZA_OFFSET_L   = 0x7E

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

  REG_ID         = 0x75 # WHOAMI REG
  MPU9250_ID_VALUE = 0x71  	# precoded identification string in WHOAMI REG
  
  def __init__(self, spi, cs=0):
    self.spi = spi
    self.cs = cs
    spi.begin()
    spi.setClockMode(0, 0)
    spi.setMaxFrequency(0, 1000000)
    
    # Am I talking to an MPU9250?
    id_val = self.readRegister(self.REG_ID)[0]
    # print "\nGot WHOAMI = 0x%02x" %id_val
    assert id_val == self.MPU9250_ID_VALUE, "MPU9250 not detected on SPI bus"

    # @TODO Fix mysterious periodic hang of magnetometer ? 
    self.writeRegister(self.REG_PWR_MGMT_1, 0x80) # Reset internal registers
    time.sleep(0.2)
    self.writeRegister(self.REG_PWR_MGMT_1, 0x01) # Auto select best clock source 
    self.writeRegister(self.REG_PWR_MGMT_2, 0x00) # Gyro & Accel ON
    time.sleep(0.2)  

                        
    accelOffsetData = self.readRegister( self.REG_XA_OFFSET_H, 2)
    print '\n AccelX_H: {:#010b}'.format(accelOffsetData[0])
    print '\n AccelX_L: {:#010b}'.format(accelOffsetData[1])


   
    #This part is to set up the magnetometer, due to it being a separate device
    self.writeRegister(self.REG_I2C_MST_CTRL, 0x0D) # I2C speed 400 Khz 
    self.writeRegister(self.REG_USER_CTRL, 0x32) #
    time.sleep(0.2) 

	  # Init magnetometer 
    self.initMag()

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

  def initMag(self):
    """ Initalize on-die AK8963 magnetometer & get offset""" 
    # Soft Reset
    self.writeRegister(self.REG_I2C_SLV0_ADDR, 0x0C)
    self.writeRegister(self.REG_I2C_SLV0_REG, self.AK8963_CNTL2)
    self.writeRegister(self.REG_I2C_SLV0_DO, 0x01)
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x81) 
    time.sleep(0.1) # Stabilize

    # Set 16-bit output & continuous MODE1 
    self.writeRegister(self.REG_I2C_SLV0_REG, self.AK8963_CNTL1)
    self.writeRegister(self.REG_I2C_SLV0_DO, 0x12 )
    self.writeRegister(self.REG_I2C_SLV0_CTRL, 0x81)
    


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

  def calibrateGyroAccel(self):
    """ Calibration function for gyroscope and accelerometer """
    
    biasGyro  = [0] * 3
    biasAccel = [0] * 3
    out = [0] * 6


    # Read configs for restoration
    oldSampleDiv    = self.readRegister(self.REG_SMPLRT_DIV, 1)[0]
    oldRegConf      = self.readRegister(self.REG_CONFIG, 1)[0]
    oldGyroConf     = self.readRegister(self.REG_GYRO_CONFIG, 1)[0]
    oldAccelConf1   = self.readRegister(self.REG_ACCEL_CONFIG1, 1)[0]
    oldAccelConf2   = self.readRegister(self.REG_ACCEL_CONFIG2, 1)[0]
    oldI2CControl   = self.readRegister(self.REG_I2C_MST_CTRL, 1)[0]
    oldUserControl  = self.readRegister(self.REG_USER_CTRL, 1)[0]

    time.sleep(1)
    confData = self.readRegister( 27, 2)
    print '\n GyroConfig: {:#010b}'.format(confData[0])
    print '\n AccelConfig: {:#010b}'.format(confData[1])
 
     
    # self.writeRegister(self.REG_PWR_MGMT_1, 0x80) # Reset internal registers
    time.sleep(0.2)
    self.writeRegister(self.REG_PWR_MGMT_1, 0x01) # Auto select best clock
    self.writeRegister(self.REG_PWR_MGMT_2, 0x00) # Gyro & Accel ON
    time.sleep(0.2)  

    #Configure device for bias calculation
    self.writeRegister(self.REG_INT_ENABLE, 0x00)   # Disable all interrupts
    self.writeRegister(self.REG_FIFO_EN, 0x00)      # Disable FIFO
    self.writeRegister(self.REG_PWR_MGMT_1, 0x00)   # Turn on internal clock
    self.writeRegister(self.REG_I2C_MST_CTRL, 0x00) # Disable I2C master
    self.writeRegister(self.REG_USER_CTRL, 0x00)    # Disable FIFO & I2C MSTR
    self.writeRegister(self.REG_USER_CTRL, 0x0C)    # Reset FIFO and DMP
    time.sleep(0.2)

    # self.writeRegister(self.REG_CONFIG, 0x01)     # Set low-pass filter to 188 Hz
    self.writeRegister(self.REG_SMPLRT_DIV, 0x00) # Set sample rate to 1 kHz
    # self.setRangeGyro(self.RANGE_GYRO_250DPS)     # Set gyro full-scale to 250 degrees per second, maximum sensitivity
    # self.setRangeAccel(self.RANGE_ACCEL_2G)       # Set accelerometer full-scale to 2 g, maximum sensitivity
    self.writeRegister(self.REG_GYRO_CONFIG, 0x00)  # Set gyro full-scale to 250 degrees per second, maximum sensitivity
    self.writeRegister(self.REG_ACCEL_CONFIG1, 0x00) # Set accelerometer full-scale to 2 g, maximum sensitivity
 
    gyrosensitivity  = 131   # = 131 LSB/degrees/sec
    accelsensitivity = 16384  # = 16384 LSB/g


    # Configure FIFO to capture accelerometer and gyro data for bias compute
    self.writeRegister(self.REG_USER_CTRL, 0x40)   # Enable FIFO  
    self.writeRegister(self.REG_FIFO_EN, 0x78)     # Enable gyro and accelerometer sensors for FIFO  (max size 512 bytes) 
    time.sleep(0.04) # accumulate 40 samples in 40 milliseconds = 480 bytes


    # At the end of sample accumulation, turn off FIFO sensor read
    self.writeRegister(self.REG_FIFO_EN, 0x00)        # Disable gyro and accelerometer sensors for FIFO
    fifoData = self.readRegister(self.REG_FIFO_COUNTH, 2) # read FIFO sample count
    fifoCount =  fifoData[0]<<8 | fifoData[1]
    packetCount = fifoCount/12  # How many sets of full gyro and accelerometer data for averaging
 
    for i in range(packetCount):

      tempAccel = [0] * 3
      tempGyro  = [0] * 3
     
      bytes = [0] * 12 
      for j in range(12):
        bytes[j] = self.readRegister(self.REG_FIFO_R_W, 1)[0] # read bytes for averaging
      
      # Form signed 16-bit integer for each sample in FIFO
      tempAccel[0] =  self.fromSigned16(bytes[0:2])   
      tempAccel[1] =  self.fromSigned16(bytes[2:4])   
      tempAccel[2] =  self.fromSigned16(bytes[4:6])   
      tempGyro[0]  =  self.fromSigned16(bytes[6:8])
      tempGyro[1]  =  self.fromSigned16(bytes[8:10])
      tempGyro[2]  =  self.fromSigned16(bytes[10:12])
     
 
      biasAccel[0] +=  tempAccel[0] # Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
      biasAccel[1] +=  tempAccel[1]
      biasAccel[2] +=  tempAccel[2]
      biasGyro[0]  +=  tempGyro[0]
      biasGyro[1]  +=  tempGyro[1]
      biasGyro[2]  +=  tempGyro[2]
  

    # Normalize sums to get average count biases
    biasAccel[0] /=  packetCount 
    biasAccel[1] /=  packetCount
    biasAccel[2] /=  packetCount
    biasGyro[0]  /=  packetCount
    biasGyro[1]  /=  packetCount
    biasGyro[2]  /=  packetCount
   

    print "\n packetCount: %d" % packetCount 
    print "\n ACCEL BIAS: %d %d %d\n GYRO BIAS: %d %d %d " % (biasAccel[0], biasAccel[1], biasAccel[2], biasGyro[0], biasGyro[1], biasGyro[2])


    #if(biasAccel[2] > 0):
    # Remove Gravity from readings
    #  biasAccel[2] -=  accelsensitivity  #    -1 G
    #else:
    #  biasAccel[2] +=  accelsensitivity  # or +1 G
    
    # Construct Gyro biases for push to the hardware gyro bias registers
    # They were reset to zero upon device hardware reset during startup

      # MULTIPLY by 4 to get 32.9 LSB per deg/s to conform to expected bias input format
      # Biases are additive, so change sign on calculated average gyro biases
    data = [0] * 6
    data[0], data[1] = self.toSigned16( -1 * biasGyro[0])
    data[2], data[3] = self.toSigned16( -1 * biasGyro[1])
    data[4], data[5] = self.toSigned16( -1 * biasGyro[2])
   
 
  # Push gyro biases to hardware registers
    self.writeRegister(self.REG_XG_OFFSET_H, data[0])
    self.writeRegister(self.REG_XG_OFFSET_L, data[1])
    self.writeRegister(self.REG_YG_OFFSET_H, data[2])
    self.writeRegister(self.REG_YG_OFFSET_L, data[3])
    self.writeRegister(self.REG_ZG_OFFSET_H, data[4])
    self.writeRegister(self.REG_ZG_OFFSET_L, data[5])
    
  # Output scaled gyro biases for display in the main program
    out[0]  =  float(biasGyro[0]) / gyrosensitivity  
    out[1]  =  float(biasGyro[1]) / gyrosensitivity
    out[2]  =  float(biasGyro[2]) / gyrosensitivity



    #Construct the accelerometer biases for push to the hardware accelerometer bias registers. These registers contain
    # factory trim values which must be added to the calculated accelerometer biases; on boot up these registers will hold
    # non-zero values. In addition, bit 0 of the lower byte must be preserved since it is used for temperature
    # compensation calculations. Accelerometer bias registers expect bias input as 2048 LSB per g, so that
    # the accelerometer biases calculated above must be divided by 8.

    biasAccelReg = [0] * 3 #  Hold the factory accelerometer trim biases
    # Read factory accelerometer trim values (!15 bit!)
    # THEY ARE NOT IN AN ADDRESS SEQUENCE OF 6 BYTES!!!    
    # Not this -> bytes = self.readRegister(self.REG_XA_OFFSET_H, 6) 
    # Addresses:
    # XA_H|XA_L = 0x77|0x78; YA_H|YA_L = 0x7A|0x7B; ZA_H|ZA_L   = 0x7D|0x7E
    bytes = [0] * 6
    bytes[0], bytes[1] = self.readRegister(self.REG_XA_OFFSET_H, 2) 
    bytes[2], bytes[3] = self.readRegister(self.REG_YA_OFFSET_H, 2) 
    bytes[4], bytes[5] = self.readRegister(self.REG_ZA_OFFSET_H, 2) 
    print "\n accel OFFSET : %s" % bytes
    biasAccelReg[0] = self.fromSigned16( bytes[0:2]) / 2 
    biasAccelReg[1] = self.fromSigned16( bytes[2:4]) / 2 
    biasAccelReg[2] = self.fromSigned16( bytes[4:6]) / 2
    # Since we're interested in the top 15 bits, we devide by 2 for the 16bit
    # signed number. Conveniently this also ignores bit 0 completely

    
    # Check for reserved bits (temperature compensation?) & preserve
    bitMask = [0] * 3
    bitMask[0] = 0x01 & bytes[1]
    bitMask[1] = 0x01 & bytes[3]
    bitMask[2] = 0x01 & bytes[5]
    
    # Construct total accelerometer bias, including calculated average accelerometer bias from above
    # bias Avg is calculated in +-2Gs / 16-bit two's compelment = 16384 Gs/LSB
    # bias in Regs is saved as +-16Gs / 15-bit two's complement = 1024 Gs/LSB
    biasAccelReg[0] -= (biasAccel[0]/16) # Subtract avg bias; in proper scale
    biasAccelReg[1] -= (biasAccel[1]/16)
    biasAccelReg[2] -= (biasAccel[2]/16)
    
    data[0], data[1] = self.toSigned16(biasAccelReg[0] * 2) 
    data[2], data[3] = self.toSigned16(biasAccelReg[1] * 2)
    data[4], data[5] = self.toSigned16(biasAccelReg[2] * 2)
      # Multiply by 2 equals to shift left
    data[1] = data[1] | bitMask[0]   # preserve reserved bit
    data[3] = data[3] | bitMask[1] 
    data[5] = data[5] | bitMask[2]

    print "\n accel OFFSET out : %s" % data
   
    #Apparently this is not working for the acceleration biases in the MPU-9250
    #Are we handling the temperature correction bit properly?
    
    #Push accelerometer biases to hardware registers
    self.writeRegister(self.REG_XA_OFFSET_H, data[0])
    self.writeRegister(self.REG_XA_OFFSET_L, data[1])
    self.writeRegister(self.REG_YA_OFFSET_H, data[2])
    self.writeRegister(self.REG_YA_OFFSET_L, data[3])
    self.writeRegister(self.REG_ZA_OFFSET_H, data[4])
    self.writeRegister(self.REG_ZA_OFFSET_L, data[5])

    time.sleep(0.2)
    bytes[0], bytes[1] = self.readRegister(self.REG_XA_OFFSET_H, 2) 
    bytes[2], bytes[3] = self.readRegister(self.REG_YA_OFFSET_H, 2) 
    bytes[4], bytes[5] = self.readRegister(self.REG_ZA_OFFSET_H, 2) 
    print "\n accel OFFSET OUT! : %s" % bytes

    #Output scaled accelerometer biases for display in the main program
    out[3] = float(biasAccel[0]) / accelsensitivity 
    out[4] = float(biasAccel[1]) / accelsensitivity
    out[5] = float(biasAccel[2]) / accelsensitivity
    
 
    # Restore old configuration registers
    self.writeRegister(self.REG_SMPLRT_DIV, oldSampleDiv)
    self.writeRegister(self.REG_I2C_MST_CTRL, oldI2CControl)
    self.writeRegister(self.REG_USER_CTRL, oldUserControl)
    self.writeRegister(self.REG_CONFIG, oldRegConf)
    self.writeRegister(self.REG_GYRO_CONFIG, oldGyroConf)
    self.writeRegister(self.REG_ACCEL_CONFIG1, oldAccelConf1)
    self.writeRegister(self.REG_ACCEL_CONFIG2, oldAccelConf2)
   
    # Set scale properly
 
    return out
              
  

    """

  uint8_t data[12]; // data array to hold accelerometer and gyro x, y, z, data
  uint16_t ii, packet_count, fifo_count;
  int32_t gyro_bias[3]  = {0, 0, 0}, accel_bias[3] = {0, 0, 0};
  
 // reset device
  writeByte(MPU9250_ADDRESS, PWR_MGMT_1, 0x80); // Write a one to bit 7 reset bit; toggle reset device
  delay(100);
   
 // get stable time source; Auto select clock source to be PLL gyroscope reference if ready 
 // else use the internal oscillator, bits 2:0 = 001
  writeByte(MPU9250_ADDRESS, PWR_MGMT_1, 0x01);  
  writeByte(MPU9250_ADDRESS, PWR_MGMT_2, 0x00);
  delay(200);                                    

// Configure device for bias calculation
  writeByte(MPU9250_ADDRESS, INT_ENABLE, 0x00);   // Disable all interrupts
  writeByte(MPU9250_ADDRESS, FIFO_EN, 0x00);      // Disable FIFO
  writeByte(MPU9250_ADDRESS, PWR_MGMT_1, 0x00);   // Turn on internal clock source
  writeByte(MPU9250_ADDRESS, I2C_MST_CTRL, 0x00); // Disable I2C master
  writeByte(MPU9250_ADDRESS, USER_CTRL, 0x00);    // Disable FIFO and I2C master modes
  writeByte(MPU9250_ADDRESS, USER_CTRL, 0x0C);    // Reset FIFO and DMP
  delay(15);
  
// Configure MPU6050 gyro and accelerometer for bias calculation
  writeByte(MPU9250_ADDRESS, CONFIG, 0x01);      // Set low-pass filter to 188 Hz
  writeByte(MPU9250_ADDRESS, SMPLRT_DIV, 0x00);  // Set sample rate to 1 kHz
  writeByte(MPU9250_ADDRESS, GYRO_CONFIG, 0x00);  // Set gyro full-scale to 250 degrees per second, maximum sensitivity
  writeByte(MPU9250_ADDRESS, ACCEL_CONFIG, 0x00); // Set accelerometer full-scale to 2 g, maximum sensitivity
 
  uint16_t  gyrosensitivity  = 131;   // = 131 LSB/degrees/sec
  uint16_t  accelsensitivity = 16384;  // = 16384 LSB/g

    // Configure FIFO to capture accelerometer and gyro data for bias calculation
  writeByte(MPU9250_ADDRESS, USER_CTRL, 0x40);   // Enable FIFO  
  writeByte(MPU9250_ADDRESS, FIFO_EN, 0x78);     // Enable gyro and accelerometer sensors for FIFO  (max size 512 bytes in MPU-9150)
  delay(40); // accumulate 40 samples in 40 milliseconds = 480 bytes

// At end of sample accumulation, turn off FIFO sensor read
  writeByte(MPU9250_ADDRESS, FIFO_EN, 0x00);        // Disable gyro and accelerometer sensors for FIFO
  readBytes(MPU9250_ADDRESS, FIFO_COUNTH, 2, &data[0]); // read FIFO sample count
  fifo_count = ((uint16_t)data[0] << 8) | data[1];
  packet_count = fifo_count/12;// How many sets of full gyro and accelerometer data for averaging
  
  for (ii = 0; ii < packet_count; ii++) {
    int16_t accel_temp[3] = {0, 0, 0}, gyro_temp[3] = {0, 0, 0};
    readBytes(MPU9250_ADDRESS, FIFO_R_W, 12, &data[0]); // read data for averaging
    accel_temp[0] = (int16_t) (((int16_t)data[0] << 8) | data[1]  ) ;  // Form signed 16-bit integer for each sample in FIFO
    accel_temp[1] = (int16_t) (((int16_t)data[2] << 8) | data[3]  ) ;
    accel_temp[2] = (int16_t) (((int16_t)data[4] << 8) | data[5]  ) ;    
    gyro_temp[0]  = (int16_t) (((int16_t)data[6] << 8) | data[7]  ) ;
    gyro_temp[1]  = (int16_t) (((int16_t)data[8] << 8) | data[9]  ) ;
    gyro_temp[2]  = (int16_t) (((int16_t)data[10] << 8) | data[11]) ;
    
    accel_bias[0] += (int32_t) accel_temp[0]; // Sum individual signed 16-bit biases to get accumulated signed 32-bit biases
    accel_bias[1] += (int32_t) accel_temp[1];
    accel_bias[2] += (int32_t) accel_temp[2];
    gyro_bias[0]  += (int32_t) gyro_temp[0];
    gyro_bias[1]  += (int32_t) gyro_temp[1];
    gyro_bias[2]  += (int32_t) gyro_temp[2];
            
}
    accel_bias[0] /= (int32_t) packet_count; // Normalize sums to get average count biases
    accel_bias[1] /= (int32_t) packet_count;
    accel_bias[2] /= (int32_t) packet_count;
    gyro_bias[0]  /= (int32_t) packet_count;
    gyro_bias[1]  /= (int32_t) packet_count;
    gyro_bias[2]  /= (int32_t) packet_count;
    
  if(accel_bias[2] > 0L) {accel_bias[2] -= (int32_t) accelsensitivity;}  // Remove gravity from the z-axis accelerometer bias calculation
  else {accel_bias[2] += (int32_t) accelsensitivity;}
   
// Construct the gyro biases for push to the hardware gyro bias registers, which are reset to zero upon device startup
  data[0] = (-gyro_bias[0]/4  >> 8) & 0xFF; // Divide by 4 to get 32.9 LSB per deg/s to conform to expected bias input format
  data[1] = (-gyro_bias[0]/4)       & 0xFF; // Biases are additive, so change sign on calculated average gyro biases
  data[2] = (-gyro_bias[1]/4  >> 8) & 0xFF;
  data[3] = (-gyro_bias[1]/4)       & 0xFF;
  data[4] = (-gyro_bias[2]/4  >> 8) & 0xFF;
  data[5] = (-gyro_bias[2]/4)       & 0xFF;
  
// Push gyro biases to hardware registers
  writeByte(MPU9250_ADDRESS, XG_OFFSET_H, data[0]);
  writeByte(MPU9250_ADDRESS, XG_OFFSET_L, data[1]);
  writeByte(MPU9250_ADDRESS, YG_OFFSET_H, data[2]);
  writeByte(MPU9250_ADDRESS, YG_OFFSET_L, data[3]);
  writeByte(MPU9250_ADDRESS, ZG_OFFSET_H, data[4]);
  writeByte(MPU9250_ADDRESS, ZG_OFFSET_L, data[5]);
  
// Output scaled gyro biases for display in the main program
  dest1[0] = (float) gyro_bias[0]/(float) gyrosensitivity;  
  dest1[1] = (float) gyro_bias[1]/(float) gyrosensitivity;
  dest1[2] = (float) gyro_bias[2]/(float) gyrosensitivity;

// Construct the accelerometer biases for push to the hardware accelerometer bias registers. These registers contain
// factory trim values which must be added to the calculated accelerometer biases; on boot up these registers will hold
// non-zero values. In addition, bit 0 of the lower byte must be preserved since it is used for temperature
// compensation calculations. Accelerometer bias registers expect bias input as 2048 LSB per g, so that
// the accelerometer biases calculated above must be divided by 8.

  int32_t accel_bias_reg[3] = {0, 0, 0}; // A place to hold the factory accelerometer trim biases
  readBytes(MPU9250_ADDRESS, XA_OFFSET_H, 2, &data[0]); // Read factory accelerometer trim values
  accel_bias_reg[0] = (int32_t) (((int16_t)data[0] << 8) | data[1]);
  readBytes(MPU9250_ADDRESS, YA_OFFSET_H, 2, &data[0]);
  accel_bias_reg[1] = (int32_t) (((int16_t)data[0] << 8) | data[1]);
  readBytes(MPU9250_ADDRESS, ZA_OFFSET_H, 2, &data[0]);
  accel_bias_reg[2] = (int32_t) (((int16_t)data[0] << 8) | data[1]);
  
  uint32_t mask = 1uL; // Define mask for temperature compensation bit 0 of lower byte of accelerometer bias registers
  uint8_t mask_bit[3] = {0, 0, 0}; // Define array to hold mask bit for each accelerometer bias axis
  
  for(ii = 0; ii < 3; ii++) {
    if((accel_bias_reg[ii] & mask)) mask_bit[ii] = 0x01; // If temperature compensation bit is set, record that fact in mask_bit
  }
  
  // Construct total accelerometer bias, including calculated average accelerometer bias from above
  accel_bias_reg[0] -= (accel_bias[0]/8); // Subtract calculated averaged accelerometer bias scaled to 2048 LSB/g (16 g full scale)
  accel_bias_reg[1] -= (accel_bias[1]/8);
  accel_bias_reg[2] -= (accel_bias[2]/8);
  
  data[0] = (accel_bias_reg[0] >> 8) & 0xFF;
  data[1] = (accel_bias_reg[0])      & 0xFF;
  data[1] = data[1] | mask_bit[0]; // preserve temperature compensation bit when writing back to accelerometer bias registers
  data[2] = (accel_bias_reg[1] >> 8) & 0xFF;
  data[3] = (accel_bias_reg[1])      & 0xFF;
  data[3] = data[3] | mask_bit[1]; // preserve temperature compensation bit when writing back to accelerometer bias registers
  data[4] = (accel_bias_reg[2] >> 8) & 0xFF;
  data[5] = (accel_bias_reg[2])      & 0xFF;
  data[5] = data[5] | mask_bit[2]; // preserve temperature compensation bit when writing back to accelerometer bias registers
 
// Apparently this is not working for the acceleration biases in the MPU-9250
// Are we handling the temperature correction bit properly?
// Push accelerometer biases to hardware registers
  writeByte(MPU9250_ADDRESS, XA_OFFSET_H, data[0]);
  writeByte(MPU9250_ADDRESS, XA_OFFSET_L, data[1]);
  writeByte(MPU9250_ADDRESS, YA_OFFSET_H, data[2]);
  writeByte(MPU9250_ADDRESS, YA_OFFSET_L, data[3]);
  writeByte(MPU9250_ADDRESS, ZA_OFFSET_H, data[4]);
  writeByte(MPU9250_ADDRESS, ZA_OFFSET_L, data[5]);

// Output scaled accelerometer biases for display in the main program
   dest2[0] = (float)accel_bias[0]/(float)accelsensitivity; 
   dest2[1] = (float)accel_bias[1]/(float)accelsensitivity;
   dest2[2] = (float)accel_bias[2]/(float)accelsensitivity;
    """
 
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
  
  def toUnsigned16(self, int):
    """ Convert unsigned short int to register values """
    return [(int >> 8) & 0xFF, int & 0xFF]


  def toSigned16(self, int):
    """ Convert signed short int to register values"""
    if int < 0: return self.toUnsigned16(65536 + int ) # int is negative
    return self.toUnsigned16(int) 


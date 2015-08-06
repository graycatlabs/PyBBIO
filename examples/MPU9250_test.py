"""
MPU9250_test.py
Niko Visnjic <self@nvisnjic.com>

Short demonstration on how to use the MPU9250 library included
with PyBBIO. Interfaces with the MPU9250 9-DOF sensor to measure
accelerometer, gyroscope and magnetometer data.

This ecample program is in the public domain.
"""

from bbio import * 
# Import the MPU9250 class from the MPU9250 library:
from bbio.libraries.MPU9250 import MPU9250

# Create a new instance of the MPU9250 class using SPI0 with the
# default to CS0 chip select pin:
mpu = MPU9250(SPI0)

def setup():
	
	delay(200) # Let the I2C reset settle
	# Sanity check
	mpu.magWhoami() # Do we have a line to the AK8963?

	# Set mag rate to 100Hz (default = 8hz)
	mpu.setRateMag(mpu.RATE_MAG_100HZ);

	delay(200)
	# check mag CNTL1 reg
	AKCTRL1 = mpu.readRegisterSLV0(mpu.AK8963_CNTL1, 1)[0]
	print '\n rate to 100Hz; AK893_CNTL1 = {:#010b}'.format(AKCTRL1)

	# Read first 15 bytes from mag and print
	datamag = mpu.readRegisterSLV0(0x00, 14)
	print '\n\t %s' % datamag

	# Test read and write to mag
	mpu.writeRegisterSLV0(mpu.AK8963_CNTL1, 0x02) #set 14 bit 8Hz continous
	readReg = mpu.readRegisterSLV0(mpu.AK8963_CNTL1, 1)[0]
	print '\n AK893_CNTL1 changed to  = {:#010b}'.format(readReg)

	# fix to 100Hz 16 bit
	mpu.writeRegisterSLV0(mpu.AK8963_CNTL1, 0x16) #set 16 bit 100Hz cont
	readReg = mpu.readRegisterSLV0(mpu.AK8963_CNTL1, 1)[0]
	print '\n AK893_CNTL1 changed to  = {:#010b}'.format(readReg)

	# Change gyro range for fun
	mpu.setRangeGyro(mpu.RANGE_GYRO_500DPS)
	
	delay(500)
	confData = mpu.readRegister( 27, 2)
	print '\n GyroConfig: {:#010b}'.format(confData[0])
	print '\n AccelConfig: {:#010b}'.format(confData[1])

	# Change it back to maximum
	mpu.setRangeGyro(mpu.RANGE_GYRO_2000DPS)
	# Can we mess it up?
	mpu.setRangeGyro(27)
	
	delay(500)
	confData = mpu.readRegister( 27, 2)
	print '\n GyroConfig: {:#010b}'.format(confData[0])
	print '\n AccelConfig: {:#010b}'.format(confData[1])

	# Do a selftest before we start
	devAccel, devGyro = mpu.runSelfTest()
	
	print "\n Sensor deviations from factory self-test values:"
	print "\n\t ACCEL: %f %f %f" % (devAccel[0], devAccel[1], devAccel[2])
	print "\n\t GYRO: %f %f %f" % (devGyro[0], devGyro[1], devGyro[2])
	
	# Calibrate Gyro & Accelerometer sensors
	data = mpu.calibrateAccelGyro()

	print "\n Sensor offset (bias) values:"
	print "\n\t ACCEL BIAS: %f %f %f\n\n\t GYRO BIAS: %f %f %f " % (data[0],data[1],data[2],data[3],data[4],data[5])
	
	
	# Did we fix everything when we're out of the calibration
	delay(500)
	confData = mpu.readRegister( 27, 2)
	print '\n AccelConfig: {:#010b}'.format(confData[1])
	print '\n GyroConfig: {:#010b}'.format(confData[0])
	delay(500)

			
	accelOffsetData = mpu.readRegister( 119, 2)
	print '\n AccelX_H: {:#010b}'.format(accelOffsetData[0])
	print '\n AccelX_L: {:#010b}'.format(accelOffsetData[1])
	
	scale = mpu.currentRangeAccel
	print "\n ACCEL RANGE = %d" % mpu.SCALE_ACCEL[scale]

	mpu.currentRangeAccel = 3
	mpu.currentRangeGyro = 3

def loop():

	# Get data
	accelX, accelY, accelZ = mpu.getAccel()
	gyroX, gyroY, gyroZ = mpu.getGyro()
	magX, magY, magZ = mpu.getMag()
	
	# Test print for conveinence 
	
	print "\n===============================================================================\n"
	print "\n AccelX: %.3f Gs \t | AccelY: %.3f Gs\t | AccelZ: %.3f Gs" % (accelX, accelY, accelZ )
	print "\n GyroX: %.3f dps \t | GyroY: %.3f dps\t | GyroZ: %.3f dps" % (gyroX, gyroY, gyroZ )
	print "\n MagX: %.3f uT \t | MagY: %.3f uT\t | MagZ: %.3f uT" % (magX, magY, magZ )

	degC = mpu.getTemp()
	
	print "\n On-die temperature: %d C" % degC 
	
	delay(200)

run(setup, loop)

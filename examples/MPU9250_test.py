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
	mpu.ak8963Whoami()
	
	# Change gyro range for fun
	mpu.setRangeGyro(mpu.RANGE_GYRO_500DPS)
	
	delay(1000)
	confData = mpu.readRegister( 27, 2)
	print '\n GyroConfig: {:#010b}'.format(confData[0])
	print '\n AccelConfig: {:#010b}'.format(confData[1])

	# Change it back to maximum
	mpu.setRangeGyro(mpu.RANGE_GYRO_2000DPS)
	mpu.setRangeGyro(27)
	
	delay(1000)
	confData = mpu.readRegister( 27, 2)
	print '\n GyroConfig: {:#010b}'.format(confData[0])
	print '\n AccelConfig: {:#010b}'.format(confData[1])
	

	# Do a selftest before we start
	devAccel, devGyro = mpu.runSelfTest()
	
	print "\n Sensor deviations from factory self-test values:"
	print "\n\t ACCEL: %f %f %f" % (devAccel[0], devAccel[1], devAccel[2])
	print "\n\t GYRO: %f %f %f" % (devGyro[0], devGyro[1], devGyro[2])
	

	# mpu.calibrateGyroAccel()

	delay(1000)
	confData = mpu.readRegister( 27, 2)
	print '\n GyroConfig: {:#010b}'.format(confData[0])
	print '\n AccelConfig: {:#010b}'.format(confData[1])
	delay(1000)
		

def loop():

	# mpu.calibrateGyroAccel()


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

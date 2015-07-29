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
	
	# Setup accel and gyro for full range
	mpu.writeRegister( 27, 24) # GryoConfig   = 0b00011000
	mpu.writeRegister( 28, 24) # AccelConfig1 = 0b00011000

	confData = mpu.readRegister( 27, 2)
	print '\n GyroConfig: {:#010b}'.format(confData[0])
	print '\n AccelConfig: {:#010b}'.format(confData[1])

	delay(100) # Let the I2C reset settle
	# Sanity check
	mpu.ak8963Whoami()

def loop():

	# Get data
	accelX, accelY, accelZ = mpu.getAcceleration()
	gyroX, gyroY, gyroZ = mpu.getGyro()
	magX, magY, magZ = mpu.getMag()
	
	# Test print for conveinence 
	
	print "\n===============================================================================\n"
	print "\n AccelX: %.3f Gs \t | AccelY: %.3f Gs\t | AccelZ: %.3f Gs" % (accelX, accelY, accelZ )
	print "\n GyroX: %.3f dps \t | GyroY: %.3f dps\t | GyroZ: %.3f dps" % (gyroX, gyroY, gyroZ )
	print "\n MagX: %.3f uT \t | MagY: %.3f uT\t | MagZ: %.3f uT" % (magX, magY, magZ )

	delay(200)

run(setup, loop)

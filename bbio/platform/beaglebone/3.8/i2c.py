# serial_port.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# This library - github.com/deepakkarki
# Apache 2.0 license
# 
# Beaglebone i2c driver

#Note : Three i2c buses are present on the BBB; i2c-0 is used for eeprom access - so not useable
#		i2c-1 is loaded default; /devices/ocp.2/4819c000.i2c/i2c-1  ---- this actually is the i2c2 bus
#		to activate i2c1 bus; echo BB-I2C1 > /sys/devices/bone_capemgr.8/slots; will be now present at /dev/i2c-2
#		reference : http://datko.net/2013/11/03/bbb_i2c/

try:
  import smbus
except:
  print "\n python-smbus module not found\n"

class _I2C_BUS(object):

	def __init__(self, bus):
		'''
		self : _I2C_BUS object
		bus : string - represents bus address eg. i2c0, i2c1
		'''
		self.config = bus
		self.bus = None # This is the smbus object

	def begin(self):
		'''
		Initializes the I2C bus with BBB as master
		'''
		pass

	def write(self, addr, val):
		'''
		Writes value 'val' to address 'addr'
		addr : integer between (0-127) - Address of slave device
		val : string, integer or list - if list, writes each value in the list
		returns number of bytes written
		'''
		pass

	def read(self, addr, size=1):
		'''
		Reads 'size' number of bytes from slave device 'addr'
		addr : integer between (0-127) - Address of slave device
		size : integer - number of bytes to be read
		returns the bytes read as a tuple
		'''
		pass

	def end(self):
		'''
		BBB exits the bus
		'''
		pass

	def _process(self, val):
		'''
		Internal function to handle datatype conversions while writing to the devices
		val - some object
		returns a processed val that can be written to the I2C device
		'''
		pass

	def available(self, addr):
		'''
		Master can query the slave and check if slave is ready to give data
		'''
		#don't know if it is possible as of now using smbus 
		pass

	def prints(self, addr, string):
		'''
		prints a string to the device with address 'addr' 
		addr : integer(0-127) - address of slave device
		string : string - to be written to slave device
		'''
		pass




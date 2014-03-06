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

##
##		NOTE : WORK IN PROGRESS. DO NOT USE CODE. CONTAINS LOTS OF COMMENTS TO SELF!!
##

import config

try:
  import smbus
except:
  print "\n python-smbus module not found\n"

class _I2C_BUS(object):

	def __init__(self, bus):
		'''
		self : _I2C_BUS object
		bus : string - represents bus address eg. i2c1, i2c2
		'''
		self.config = bus
		self.bus = None # This is the smbus object
		self.open = False

	def begin(self):
		'''
		Initializes the I2C bus with BBB as master
		'''
		if not i2cInit(self.config):
			print "Could not initialize i2c bus : %s" % self.config 
			return
		self.bus = smbus.SMBus(int(I2C[self.config][0][-1]))
		self.open = True

	def write(self, addr, val):
		'''
		Writes value 'val' to address 'addr'
		addr : integer between (0-127) - Address of slave device
		val : string, integer or list - if list, writes each value in the list
		returns number of bytes written
		'''
		if not self.open:
			print "I2C bus : %s - not initialized" % self.config

		if type(addr) == int:
			return self.bus.write_byte(addr, val)

		else:
			return self._write_list(addr, self._process(val))


	def _write_list(self, addr, val):
		'''
		called from write when val is a string or list - this is internal to keep interface simple
		addr : integer between (0-127) - Address of slave device
		val : list - Of either characters or integers.
		'''
		#remove this - insead have a recursive fn which will convert lists to list of integers - and returns it back to write
		pass


	def read(self, addr, size=1):
		'''
		Reads 'size' number of bytes from slave device 'addr'
		addr : integer between (0-127) - Address of slave device
		size : integer - number of bytes to be read
		returns an int if size is 1; else list of integers
		'''
		if not self.open:
			print "I2C bus : %s - not initialized, open before read" % self.config

		if size == 1:
			return self.bus.read_byte(addr)

		

		else:
			read_data = []
			for i in range(size):
				data = self.bus.read_byte(addr)
				if data == -1: #No more data to be read
					break
				else :
					read_data.append(data)

		return read_data


	def end(self):
		'''
		BBB exits the bus
		'''
		if self.bus:
			self.bus.close()



	def _process(self, val):
		'''
		Internal function to handle datatype conversions while writing to the devices
		val - some object
		returns a processed val that can be written to the I2C device
		'''
		# Keep this for prints, add the below check in write itself. All that is allowed is [int, str, list(int), list(str)]
		if type(val) == str:
			return map(lambda x: ord(x), list(val))
			#convert string to list of ascii values



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
		#make this just like serial.println - i.e. add formating and all

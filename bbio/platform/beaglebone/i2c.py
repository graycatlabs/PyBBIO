# i2c.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# This library - github.com/deepakkarki
# MIT License
# 
# Beaglebone i2c driver

#Note : Three i2c buses are present on the BBB; i2c-0 is used for eeprom access - so not useable
#       i2c-1 is loaded default; /devices/ocp.2/4819c000.i2c/i2c-1  ---- this actually is the i2c2 bus
#       to activate i2c1 bus; echo BB-I2C1 > /sys/devices/bone_capemgr.8/slots; will be now present at /dev/i2c-2
#       reference : http://datko.net/2013/11/03/bbb_i2c/

import bbio
from config import I2C

from bbio.platform.platform import detect_platform 
_platform = detect_platform()
if "3.8" in _platform:
  from bone_3_8.i2c_setup import i2cInit
elif "3.2" in _platform:
  from bone_3_2.i2c_setup import i2cInit
del _platform

try:
  import smbus
except:
  print "\n python-smbus module not found\n"
  print "on Angstrom Linux : ~#opkg install python-smbus\n"
  print "on Ubuntu, Debian : ~#apt-get install python-smbus"


class _I2C_BUS(object):

    def __init__(self, bus):
        '''
        self : _I2C_BUS object
        bus : string - represents bus address eg. i2c1, i2c2; not dev_file
        '''
        assert bus in I2C, "Invalid bus address %s" %bus
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
        #smbus takes the dev_file number as parameter, not bus number
        #so if I pass 1 as the parameter, is uses /dev/i2c-1 file not i2c1 bus
        self.open = True

    def write(self, addr, reg, val):
        '''
        Writes value 'val' to address 'addr'
        addr : integer between (0-127) - Address of slave device
        reg : register of the slave device you want to write to
        val : string, integer or list - if list, writes each value in the list
        returns number of bytes written
        '''
        if not self.open:
            print "I2C bus : %s - not initialized" % self.config
            return

        try:
            if type(val) == int:
                self.bus.write_byte_data(addr, reg, val)
                return 1

            else:
                data = self._format(val)
                if data:
                    for i, unit in enumerate(data):
                        self.bus.write_byte_data(addr, reg+i, unit)
                        bbio.delay(4) #4 microsecond delay
                        #delay reqd, otherwise loss of data
                    return len(data)
                else: 
                    return 0

        except IOError as e:
            print "Bus is active : check if device with address %d is connected/activated" %addr


    def _format(self, val):
        '''
        used to format values given to write into reqd format 
        val : string or list (of integers or strings)
        returns : list of integers, if bad paramater - returns None
        '''

        if type(val) == str:
            return map(lambda x: ord(x), list(val))

        if type(val) == list and len(val):
            #non empty list

            if len(filter(lambda x: type(x) == int, val)) == len(val):
                #all variables are integers
                return val

            if len(filter(lambda x: type(x) == str, val)) == len(val):
                #all variables are strings
                data = []
                for unit in val:
                    data.extend(list(unit))
                return map(lambda x: ord(x), list(data))

        return None


    def read(self, addr, reg, size=1):
        '''
        Reads 'size' number of bytes from slave device 'addr'
        addr : integer between (0-127) - Address of slave device
        reg : register of the slave device you want to read from
        size : integer - number of bytes to be read
        returns an int if size is 1; else list of integers
        '''
        if not self.open:
            print "I2C bus : %s - not initialized, open before read" % self.config

        try:

            if size == 1:
                return self.bus.read_byte_data(addr, reg)

            else:
                read_data = []
                for i in range(size):
                    data = self.bus.read_byte_data(addr, reg+i)
                    bbio.delay(4)
                    read_data.append(data)

            return read_data

        except IOError as e:
            print "Bus is active : check if device with address %d is connected/activated" %addr


    def end(self):
        '''
        BBB exits the bus
        '''
        if self.bus:
            result = self.bus.close()
            self.open = False
            return True
        else:
            print "i2c bus : %s - is not open. use begin() first" % self.config 
            return False



    def _process(self, val):
        '''
        Internal function to handle datatype conversions while writing to the devices
        val - some object
        returns a processed val that can be written to the I2C device
        '''
        # Keep this for prints
        pass

    def prints(self, addr, string):
        '''
        prints a string to the device with address 'addr' 
        addr : integer(0-127) - address of slave device
        string : string - to be written to slave device
        '''
        pass
        #fill this later - could be used to send formatted text across to some I2C based screens (?)

def i2c_cleanup():
    """
    Ensures that all i2c buses opened by current process are freed. 
    """
    for bus in (Wire1, Wire2):
        if bus.open:
            bus.end()

#For arduino like similariy 
Wire1 = _I2C_BUS('i2c1') #pins 17-18 OR 24-26
# ^ not initialized by default; /dev/i2c-2
#need to apply overlay for this

Wire2 = _I2C_BUS('i2c2') #pins 19-20 OR 21-22
#initialized by default; /dev/i2c-1# i2c.py 

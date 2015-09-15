"""
 HTU21D
 Copyright 2015 - Alexander Hiam <alex@graycat.io>

 A PyBBIO library for controlling HTU21D I2C humidity sensor.

 HTU21D is released as part of PyBBIO under its MIT license.
 See PyBBIO/LICENSE.txt
"""
import bbio, math

class HTU21D(object):
  I2C_ADDRESS = 0x40

  CMD_TEMP          = 0xf3
  CMD_RH            = 0xf5
  CMD_USER_REG_READ = 0xe7 
  CMD_RESET         = 0xfe

  USER_REGISTER_DEFAULT = 0x02 # Reset value of the user register

  CRC_DIVISOR = 0b100110001

  def __init__(self, i2c):
    self.i2c = i2c
    if i2c == -1:
      # Testing mode, don't try to open an I2C interface
      return
    i2c.write(self.I2C_ADDRESS, [self.CMD_RESET])
    bbio.delay(15)
    usr_reg = i2c.readTransaction(self.I2C_ADDRESS, self.CMD_USER_REG_READ, 1)
    assert usr_reg[0] == self.USER_REGISTER_DEFAULT, \
      "HTU21D not detected on I2C bus"

  def getHumidity(self):
    """ Reads and returns the current relative humidity

    Received value is checked against a CRC and an AssertionError is thrown if 
    it is invalid.
    """
    self.i2c.write(self.I2C_ADDRESS, [self.CMD_RH])
    bbio.delay(50)
    msb, lsb, crc = self.i2c.read(self.I2C_ADDRESS, 3)

    raw_value = (msb<<8) | lsb
    assert self.checkCRC(raw_value, crc), "received invalid data"
    # Should that really throw an error?

    # Conversion formula from datasheet:
    return -6.0 + 125.0 * (raw_value/65536.0)

  def getTemp(self):
    """ Reads and returns the current ambient temperature in Celsius

    Received value is checked against a CRC and an AssertionError is thrown if 
    it is invalid.
    """
    self.i2c.write(self.I2C_ADDRESS, [self.CMD_TEMP])
    bbio.delay(50)
    msb, lsb, crc = self.i2c.read(self.I2C_ADDRESS, 3)

    raw_value = (msb<<8) | lsb
    assert self.checkCRC(raw_value, crc), "received invalid data"
    # Should that really throw an error?

    # Conversion formula from datasheet:
    return -46.85 + 175.72 * (raw_value/65536.0)

  def getTempF(self):
    """ Reads and returns the current ambient temperature in fahrenheit

    Received value is checked against a CRC and an AssertionError is thrown if 
    it is invalid.
    """
    tempC = self.getTemp()
    return tempC * 9./5 + 32

  def calculateDewPoint(self, rh, temp):
    """ Calculates and returns the dew point for the given RH and temp C

    >>> round(HTU21D(-1).calculateDewPoint(50.0, 25.0))
    14.0
    >>> round(HTU21D(-1).calculateDewPoint(65.0, -10.0))
    -15.0
    """
    # A, B and C are constants in the dew point calculations
    A = 8.1332
    B = 1762.39
    C = 235.66
    pp = 10**(A - B / (temp + C)) # Partial pressure
    return -(C + B / (math.log(rh * (pp/100.), 10) - A))

  def checkCRC(self, value, crc):
    """ Checks the given 2-byte value against the given CRC
        
    Uses the HTU21D's divisor polynomial of x^8 + x^5 + x^4 + 1 given in 
    the datasheet.
    See http://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks

    >>> HTU21D(-1).checkCRC(0xDC, 0x79)
    True
    >>> HTU21D(-1).checkCRC(0x683A, 0x7C)
    True
    >>> HTU21D(-1).checkCRC(0x683A, 0x01)
    False
    """
    value <<= 8
    divisor = self.CRC_DIVISOR << 15
    for i in range(16):
      if value & 1<<(23-i):
        # There's a 1 above the x^8 bit of the divisor polynomial
        value ^= divisor
      divisor >>= 1
    if (value & 0xff) == crc: return True
    return False

if __name__ == "__main__":
    import doctest
    doctest.testmod()
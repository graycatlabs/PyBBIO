"""
 ADXL345
 Copyright 2015 - Alexander Hiam <alex@graycat.io>

 A PyBBIO library for controlling the ADXL345 accelerometer.
 Currently only the I2C mode has been tested.

 ADXL345 is released as part of PyBBIO under its MIT license.
 See PyBBIO/LICENSE.txt
"""

import bbio

class ADXL345(object):
  RANGE_2G = 0
  RANGE_4G = 1
  RANGE_8G = 2
  RANGE_16G = 3

  # Pre-calculated unit conversion multipliers:
  G_PER_BIT = [
    0.00390625,
    0.0078125,
    0.015625,
    0.03125
    ]

  INT_DOUBLE_TAP = 1<<5
  INT_SINGLE_TAP = 1<<6
  INT1 = 1
  INT2 = 2

  REG_THRESH_TAP = 0x1d
  REG_DUR_TAP    = 0x21
  REG_LATENT_TAP = 0x22
  REG_WINDOW_TAP = 0x23

  REG_TAP_AXES  = 0x2a
  TAP_AXES_X_EN = 1<<2
  TAP_AXES_Y_EN = 1<<1
  TAP_AXES_Z_EN = 1

  REG_POWER_CTL     = 0x2D
  POWER_CTL_MEASURE = 1<<3

  REG_INT_ENABLE = 0x2e
  REG_INT_MAP    = 0x2f
  REG_INT_SOURCE = 0x30

  REG_DATA_FORMAT = 0x31
  
  REG_DATAX0 = 0x32
  REG_DATAX1 = 0x33
  REG_DATAY0 = 0x34
  REG_DATAY1 = 0x35
  REG_DATAZ0 = 0x36
  REG_DATAZ1 = 0x37

  MODE_SPI       = 1
  SPI_CLOCK_MODE = 3

  MODE_I2C     = 0
  I2C_ADDR     = 0x1d
  I2C_ALT_ADDR = 0x53

  def __init__(self, bus, spi_cs=0, i2c_addr=0x1d, spi_frequency=4000000):
    if bus == bbio.I2C1 or bus == bbio.I2C2:
      self.mode = self.MODE_I2C
    elif bus == bbio.SPI0 or bus == bbio.SPI1:
      self.mode = self.MODE_SPI
      self.spi_cs = spi_cs
      self.spi_frequency = spi_frequency
    else:
      raise ValueError("bus must be an PyBBIO I2C or SPI object")

    self.bus = bus
    self.i2c_addr = i2c_addr

    # Enable sampling:
    self.writeReg(self.REG_POWER_CTL, self.POWER_CTL_MEASURE)
    # Set to default range of +/- 2G:
    self.setRange(self.RANGE_2G)

  def getXYZ(self):
    """ Read and return the current acceleration as a list: [x,y,z]. """
    data = self.readReg(self.REG_DATAX0, 6)
    samples = [0]*3
    for i in range(0, 3):
      # Combine high and low byte:
      samples[i] = (data[i+i+1]<<8) | data[i+i]
      # Convert from 2's complement:
      if samples[i] >= 32768: samples[i] -= 65536
      # Convert to G:
      samples[i] *= self.G_PER_BIT[self.accel_range]
    return samples

  def setRange(self, accel_range):
    """ Set the current range to one of: 
          ADXL345.RANGE_2G  for +/- 2g
          ADXL345.RANGE_4G  for +/- 4g
          ADXL345.RANGE_8G  for +/- 8g
          ADXL345.RANGE_16G for +/- 16g 
    """
    accel_range &= 0b11 # ensure it's only 2 bits
    self.writeReg(self.REG_DATA_FORMAT, accel_range)
    self.accel_range = accel_range

  def enableInterrupt(self, interrupt, int_pin):
    """ Map the given tap interrupt (ADXL345.INT_SINGLE_TAP or 
        ADXL345.INT_DOUBLE_TAP) to the given interrupt pin (ADXL345.INT1 or 
        ADXL345.INT2) and enable it.
    """
    if interrupt != self.INT_DOUBLE_TAP and interrupt != self.INT_SINGLE_TAP:
       raise ValueError("interrupt must be one of ADXL345.INT_SINGLE_TAP or ADXL345.INT_DOUBLE_TAP")

    if int_pin != self.INT1 and int_pin != self.INT2:
       raise ValueError("int_pin must be one of ADXL345.INT1 or ADXL345.INT2")

    # Map the interrupt to the pin:
    int_map = self.readReg(self.REG_INT_MAP)[0]
    if (int_pin == self.INT2):
      # bit=1 for INT2, set bit:
      int_map |= interrupt
    else:
      # bit=0 for INT1, clear bit:
      int_map &= ~interrupt

    self.writeReg(self.REG_INT_MAP, int_map)
    
    # Read current register value:
    int_enable = self.readReg(self.REG_INT_ENABLE)[0]

    # First disable interrupt and ensure any pending interrupts are cleared:
    int_enable &= ~interrupt # 0 to enable interrupt
    self.writeReg(self.REG_INT_ENABLE, int_enable)
    self.getInterrupts()

    int_enable |= interrupt # 1 to enable interrupt
    self.writeReg(self.REG_INT_ENABLE, int_enable)

  def disableInterrupt(self, interrupt):
    """ Disables the given interrupt, either ADXL345.INT_SINGLE_TAP or 
        ADXL345.INT_DOUBLE_TAP.
    """
    if interrupt != self.INT_DOUBLE_TAP and interrupt != self.INT_SINGLE_TAP:
      raise ValueError("interrupt must be one of ADXL345.INT_SINGLE_TAP or ADXL345.INT_DOUBLE_TAP")

    int_enable = self.readReg(self.REG_INT_ENABLE)[0]
    int_enable &= ~interrupt # 0 to enable interrupt
    self.writeReg(self.REG_INT_ENABLE, int_enable)

  def enableTapDetection(self, threshold_g=3, duration_ms=20, 
                           latency_ms=100, window_ms=1000):
    """ Enables ADXL345 internal single and double tap detection, using
        the given parameters (described in the docs for their own individual 
        methods). The default values should work fairly well when tapping on
        the PCB on which the ADXL345 is mounted.
    """
    self.writeReg(self.REG_TAP_AXES, 0)
    enable = self.TAP_AXES_X_EN | self.TAP_AXES_Y_EN | self.TAP_AXES_Z_EN
    self.writeReg(self.REG_TAP_AXES, enable)
    self.setTapThreshold(threshold_g) # threshold in g
    self.setTapDuration(duration_ms)  # minimum duration of tap
    self.setTapLatency(latency_ms)    # double-tap latency
    self.setTapWindow(window_ms)      # double-tap window

  def setTapThreshold(self, threshold):
    """ Sets the threshold in G that must be crossed for a tap to be detected.
    """
    # Convert to bits:
    threshold /= 0.0625
    # Round to nearest integer:
    threshold = int(threshold + 0.5)
    # Constrain to single byte:
    if threshold > 255: threshold = 255
    self.writeReg(self.REG_THRESH_TAP, threshold)

  def setTapDuration(self, duration):
    """ Sets the time in milliseconds that the acceleration in any axis must
        remain above the tap threshold for a tap to be detected.
    """
    duration /= 0.625
    duration = int(duration + 0.5)
    if duration > 255: duration = 255
    self.writeReg(self.REG_DUR_TAP, duration)

  def setTapLatency(self, latency):
    """ Sets the minimum amount of time in milliseconds after one tap is
        detected that must pass before a second tap crosses the tap threshold.
        Any crossing of the threshold before this time has passed is considered
        noise and a second tap won't be detected.
    """
    latency /= 1.25
    latency = int(latency + 0.5)
    if latency > 255: latency = 255
    self.writeReg(self.REG_LATENT_TAP, latency)

  def setTapWindow(self, window):
    """ Sets the maximum amount of time in seconds that two taps must occur
        within for a double tap to be detected.
    """
    window /= 1.25
    window = int(window + 0.5)
    if window > 255: window = 255
    self.writeReg(self.REG_WINDOW_TAP, window)

  def getInterrupts(self):
    """ Reads and returns the INT_SOURCE register. Must be called in interrupt
        handler to clear interrupt status if using tap detection.
    """
    # Read and return INT_SOURCE register:
    return self.readReg(self.REG_INT_SOURCE)[0]

  def writeReg(self, reg, val):
    """ Writes the given value to the given register. """
    # Limit to 6-bit address space:
    reg &= 0x3f
    # Ensure the value is a single byte:
    val &= 0xff

    if self.mode == self.MODE_I2C:
      self.bus.write(self.i2c_addr, [reg, val])

    elif self.mode == self.MODE_SPI:
      self.bus.setClockMode(self.spi_cs, self.SPI_CLOCK_MODE)
      self.bus.setMaxFrequency(self.spi_cs, self.spi_frequency)
      self.bus.write(self.spi_cs, [reg, val])
      
  def readReg(self, reg, n_bytes=1):
    """ Reads and returns the given number of bytes (default 1) from the given
        register as a list. """
    # Limit to 6-bit address space:
    reg &= 0x3f

    if self.mode == self.MODE_I2C:
      return self.bus.readTransaction(self.i2c_addr, reg, n_bytes)

    elif self.mode == self.MODE_SPI:
      # Set read bit:
      reg |= 1<<7
      if (n_bytes > 1):
        # Set multiple byte bit:
        reg |= 1<<6
      self.bus.setClockMode(self.spi_cs, self.SPI_CLOCK_MODE)
      self.bus.setMaxFrequency(self.spi_cs, self.spi_frequency)
      return self.bus.transfer(self.spi_cs, [reg] + [0]*n_bytes)[1:]

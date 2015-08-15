"""
 ADXL345
 Copyright 2015 - Alexander Hiam <alex@graycat.io>

 A PyBBIO library for controlling ADXL345 accelerometer.
 Currently only supports I2C mode.

 ADXL345 is released as part of PyBBIO under its MIT license.
 See PyBBIO/LICENSE.txt
"""

class ADXL345(object):
  RANGE_2G = 0
  RANGE_4G = 1
  RANGE_8G = 2
  RANGE_16G = 3

  # Precalculated unit conversion multipliers:
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

  def __init__(self, i2c, addr=0x53):
    self.i2c = i2c
    self.addr = addr

  def begin(self):
    self.i2c.begin()
    self.i2c.write(self.addr, [0x2D, 1<<3])
    self.set_range(self.RANGE_2G)

  def get_xyz(self):
    """ Read and return the current acceleration as a list: [x,y,z]. """
    data = self.i2c.readTransaction(self.addr, 0x32, 6)
    samples = [0]*3
    for i in range(0, 3):
      samples[i] = (data[i+i+1]<<8) | data[i+i]
      if samples[i] >= 32768: samples[i] -= 65536
      samples[i] *= self.G_PER_BIT[self.accel_range]
    return samples

  def set_range(self, accel_range):
    """ Set the current range to one of: 
          ADXL345.RANGE_2G  : +/- 2g
          ADXL345.RANGE_4G  : +/- 4g
          ADXL345.RANGE_8G  : +/- 8g
          ADXL345.RANGE_16G : +/- 16g """
    accel_range &= 0b11 # ensure it's only 2 bits
    self.i2c.write(self.addr, [0x31, accel_range])
    self.accel_range = accel_range

  def enable_interrupt(self, interrupt, int_pin):
    """ Map the given interrupt  """
    # Map the interrupt to the pin:
    int_map = self.i2c.readTransaction(self.addr, 0x2F, 1)[0]
    if (int_pin == self.INT2):
      # bit=1 for INT2, set bit:
      int_map |= interrupt
    else:
      # bit=0 for INT1, clear bit:
      int_map &= ~interrupt
    self.i2c.write(self.addr, [0x2F, int_map])
    
    # Enable the interrupt
    int_enable = self.i2c.readTransaction(self.addr, 0x2E, 1)[0]
    int_enable |= interrupt # 1 to enable interrupt
    self.i2c.write(self.addr, [0x2E, int_enable])

  def enable_tap_detection(self):
    # Enable taps for the different axes:
    self.i2c.write(self.addr, [0x2A, 0x7])
    self.set_tap_threshold(3) # 3g threshold
    self.set_tap_duration(20) # 20ms minimum duration
    self.set_tap_latency(100) # 100ms double-tap latency
    self.set_tap_window(1000) # 1s double-tap window

  def set_tap_threshold(self, threshold):
    # Convert to bits:
    threshold /= 0.0625
    # Round to nearest integer:
    threshold = int(threshold + 0.5)
    # Constrain to single byte:
    if threshold > 255: threshold = 255
    self.i2c.write(self.addr, [0x1D, threshold])

  def set_tap_duration(self, duration):
    duration /= 0.625
    duration = int(duration + 0.5)
    if duration > 255: duration = 255
    self.i2c.write(self.addr, [0x21, duration])

  def set_tap_latency(self, latency):
    latency /= 1.25
    latency = int(latency + 0.5)
    if latency > 255: latency = 255
    self.i2c.write(self.addr, [0x22, latency])

  def set_tap_window(self, window):
    window /= 1.25
    window = int(window + 0.5)
    if window > 255: window = 255
    self.i2c.write(self.addr, [0x23, window])

  def get_interrupts(self):
    # Read and return INT_SOURCE register:
    return self.i2c.readTransaction(self.addr, 0x30, 1)[0]
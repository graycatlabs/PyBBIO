# serial_port.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone serial driver

import os, glob, cape_manager, bbio
from config import UART, DEC, BIN, OCT, HEX

try:
  import serial
except:
  print "\n pyserial module not found; to install:\n\
   # opkg update && opkg install python-pyserial\n"

def uartInit(uart):
  """ Enables the given uart by loading its dto. """
  port, overlay = UART[uart]
  if os.path.exists(port): return True
  # Unloading serial port overlays crashes the current cape manager, 
  # disable until it gets fixed:
  cape_manager.load(overlay, auto_unload=False)
  if os.path.exists(port): return True

  for i in range(5):
    # Give it some time to load
    bbio.delay(100)
    if os.path.exists(port): return True
    
  # If we make it here it's pretty safe to say the overlay couldn't load
  return False

# _UART_PORT is a wrapper class for pySerial to enable Arduino-like access
# to the UART1, UART2, UART4, and UART5 serial ports on the expansion headers:
class _UART_PORT(object):
  def __init__(self, uart):
    assert uart in UART, "*Invalid UART: %s" % uart
    self.config = uart
    self.baud = 0
    self.open = False
    self.ser_port = None
    self.peek_char = ''

  def begin(self, baud, timeout=1, **kwargs):
    """ Starts the serial port at the given baud rate. 'timeout' as well
        as any other given keyword arguments will be passed to the PySerial 
        Serial class' __init__() method, see the PySerial docs for more info. 
    """
    if not uartInit(self.config):
      print "*Could not open serial port defined by: %s" % self.config
      self.ser_port = None
      return
    port = UART[self.config][0]
    self.baud = baud
    self.ser_port = serial.Serial(port, baud, timeout=timeout, **kwargs)
    self.open = True 

  def end(self):
    """ Closes the serial port if open. """
    if not(self.open): return
    self.flush()
    self.ser_port.close()
    self.ser_port = None
    self.baud = 0
    self.open = False

  def available(self):
    """ Returns the number of bytes currently in the receive buffer. """
    return self.ser_port.inWaiting() + len(self.peek_char)

  def read(self):
    """ Returns first byte of data in the receive buffer or -1 if timeout reached. """
    if (self.peek_char):
      c = self.peek_char
      self.peek_char = ''
      return c
    byte = self.ser_port.read(1)
    return -1 if (byte == None) else byte

  def peek(self):
    """ Returns the next char from the receive buffer without removing it, 
        or -1 if no data available. """
    if (self.peek_char):
      return self.peek_char
    if self.available():
      self.peek_char = self.ser_port.read(1)
      return self.peek_char
    return -1    

  def flush(self):
    """ Waits for current write to finish then flushes rx/tx buffers. """
    self.ser_port.flush()
    self.peek_char = ''

  def prints(self, data, base=None):
    """ Prints string of given data to the serial port. Returns the number
        of bytes written. The optional 'base' argument is used to format the
        data per the Arduino serial.print() formatting scheme, see:
        http://arduino.cc/en/Serial/Print """
    return self.write(self._process(data, base))

  def println(self, data, base=None):
    """ Prints string of given data to the serial port followed by a 
        carriage return and line feed. Returns the number of bytes written.
        The optional 'base' argument is used to format the data per the Arduino
        serial.print() formatting scheme, see: http://arduino.cc/en/Serial/Print """
    return self.write(self._process(data, base)+"\r\n")

  def write(self, data):
    """ Writes given data to serial port. If data is list or string each
        element/character is sent sequentially. If data is float it is 
        converted to an int, if data is int it is sent as a single byte 
        (least significant if data > 1 byte). Returns the number of bytes
        written. """
    assert self.open, "*%s not open, call begin() method before writing" %\
                      UART[self.config][0]

    if (type(data) == float): data = int(data)
    if (type(data) == int): data = chr(data & 0xff)

    elif ((type(data) == list) or (type(data) == tuple)):
      bytes_written = 0
      for i in data:
        bytes_written += self.write(i)  
      return bytes_written

    elif (type(data) != str):
      # Type not supported by write, e.g. dict; use prints().
      return 0

    written = self.ser_port.write(data)
    # Serial.write() returns None if no bits written, we want 0:
    return written if written else 0

  def _process(self, data, base):
    """ Processes and returns given data per Arduino format specified on 
        serial.print() page: http://arduino.cc/en/Serial/Print """
    if (type(data) == str):
      # Can't format if already a string:
      return data

    if (type(data) is int):
      if not (base): base = DEC # Default for ints
      if (base == DEC):
        return str(data) # e.g. 20 -> "20"
      if (base == BIN):
        return bin(data)[2:] # e.g. 20 -> "10100"
      if (base == OCT):
        return oct(data)[1:] # e.g. 20 -> "24"
      if (base == HEX):
        return hex(data)[2:] # e.g. 20 -> "14"

    elif (type(data) is float):
      if not (base): base = 2 # Default for floats
      if ((base == 0)):
        return str(int(data))
      if ((type(base) == int) and (base > 0)):
        return ("%0." + ("%i" % base) + "f") % data

    # If we get here data isn't supported by this formatting scheme,
    # just convert to a string and return:
    return str(data)

# Initialize the global serial port instances:
Serial1 = _UART_PORT('UART1')
Serial2 = _UART_PORT('UART2')
Serial4 = _UART_PORT('UART4')
Serial5 = _UART_PORT('UART5')

def serial_cleanup():
  """ Ensures that all serial ports opened by current process are closed. """
  for port in (Serial1, Serial2, Serial4, Serial5):
    port.end()

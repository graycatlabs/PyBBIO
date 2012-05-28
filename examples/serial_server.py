# serial_server.py - Alexander Hiam - 4/15/12
# 
# Creates a simple web interface to the Serial2 port.
#
# Serial2 TX = pin 21 on P9 header
# Serial2 RX = pin 22 on P9 header
#
# Run this program and navigate to http://your_beaglebone_ip:8000
# in your web brower.
#
# See BBIOServer tutorial:
#  https://github.com/alexanderhiam/PyBBIO/wiki/BBIOServer
#
# This example is in the public domain

from bbio import *
from BBIOServer import *

# Create a server instance:
server = BBIOServer()

# A global buffer for received data:
data =''

def serial_tx(string):
  """ Sends given string to Serial2. """
  Serial2.println(string)

def serial_rx():
  """ Returns received data if any, otherwise current data buffer. """
  global data
  if (Serial2.available()):
    # There's incoming data
    data =''
    while(Serial2.available()):
      # If multiple characters are being sent we want to catch
      # them all, so add received byte to our data string and 
      # delay a little to give the next byte time to arrive:
      data += Serial2.read()
      delay(5) 
  return data

def setup():
  # Start the serial port at 9600 baud:
  Serial2.begin(9600)
  # Create the web page:
  serial = Page("Serial")
  serial.add_text("A simple interface to Serial2.")
  serial.add_entry(lambda string: serial_tx(string), "Send", newline=True)
  serial.add_monitor(lambda: serial_rx(), "Received:", newline=True)

  # Start the server:
  server.start(serial)

def loop():
  # Server has stopped; exit happily:
  stop()

run(setup, loop)

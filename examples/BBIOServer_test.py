#!/usr/bin/env python
"""
 BBIOServer_test.py 
 Alexander Hiam

 An example to demonstrate the use of the BBIOServer library
 for PyBBIO.

 This example program is in the public domain.
"""

# First we must import PyBBIO: 
from bbio import *
# Then we can import BBIOServer:
from BBIOServer import *

# Now we create a server instance:
server = BBIOServer()
# Port 8000 is used by default, but can be specified when creating
# server instance:
#  server = BBIOServer(port_number)

def voltage(analog_pin):
  """ Takes analog reading from given pin and returns a string 
      of the voltage to 2 decimal places. """
  return "%0.2f" % (analogRead(analog_pin) * (1.8 / 2**12))

def print_entry(text):
  """ Just prints the given text. """
  print "Text entered: \n  '%s'" % text

def setup():
  # Set the LEDs we'll be ontrolling as outputs:
  pinMode(USR2, OUTPUT)
  pinMode(USR3, OUTPUT)

  # Create our first page with the title 'PyBBIO Test':
  home = Page("PyBBIO Test")
  # Add some text to the page:
  home.add_text("This is a test of the BBIOServer library for PyBBIO."+\
                " Follow the links at the left to test the different pages.")                 
  # Create a new page to test the text input:
  text = Page("Text Input")
  text.add_text("Press submit to send the text in entry box:")

  # Create the text entry box on a new line; button will say 'Submit',
  # and when submitted the text in the box will be sent to print_entry().
  # Because print_entry is not a standard PyBBIO function, we must pass
  # a pointer to it as the 'pointer' parameter:
  text.add_entry("print_entry(%s)", "Submit", newline=True, pointer=print_entry)

  # Create a new page to test the buttons and monitors:
  io = Page("I/O")
 
  # Make a LED control section using a heading:
  io.add_heading("LED Control")
  io.add_text("Control the on-board LEDs", newline=True)

  # Add a button on a new line with the label 'Toggle USR2 LED' that will
  # call 'toggle(USR2)' when pressed. Because toggle() is a standard 
  # PyBBIO function, we don't need to pass in a pointer:
  io.add_button("toggle(USR2)", "Toggle USR2 LED", newline=True)

  # Add a monitor which will continually call 'pinState(USR2)' and 
  # display the return value in the form: 'current state: [value]':
  io.add_monitor("pinState(USR2)", "current state:")

  # Same thing here with the other LED:
  io.add_button("toggle(USR3)", "Toggle USR3 LED", newline=True)
  io.add_monitor("pinState(USR3)", "current state:")

  # Create another section for ADC readings:
  io.add_heading("ADC Readings")
  io.add_text("Read some ADC inputs", newline=True)

  # Add a monitor to display the ADC value:
  io.add_monitor("analogRead(AIN0)", "AIN0 value:", newline=True)

  # And one on the same line to display the voltage using the
  # vlotage() function defined above (passing a pointer to it).
  # Because units are given this time, the value will be displayed
  # in the form: 'voltage: [value] v':
  io.add_monitor("voltage(AIN0)", "voltage:", units="v", pointer=voltage)

  # Same thing here:
  io.add_monitor("analogRead(AIN1)", "AIN1 value:", newline=True)
  io.add_monitor("voltage(AIN1)", "voltage:", units="v", pointer=voltage)

  # Then start the server, passing it all the pages. The first page
  # passed in will be the home page:
  server.start(home, text, io)


def loop():
  # The server will block until ctrl-c is pressed, so if we get here
  # we know the server is no longer running. If we don't stop at this
  # point we will continue looping over this function until ctrl-c is
  # pressed again. If we don't need to do anything here it's easiest 
  # to just stop the loop here:
  print "\nServer has stopped"
  stop()

# Then run it the usual way:
run(setup, loop)

# Now, on a computer on the same network as you beaglebone, open your
# browser and navigate to:
#  your_beaglebone_ip:8000 
#  (replacing 8000 if you specified a different port)
# You should be redirected to your_beaglebone_ip:8000/pages/PyBBIOTest.html

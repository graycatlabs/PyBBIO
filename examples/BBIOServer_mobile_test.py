#!/usr/bin/env python
"""
 BBIOServer_mobile_test.py 
 Alexander Hiam

 An example to demonstrate the use of the BBIOServer library
 for PyBBIO.

 This creates the same interface as BBIOServer_test.py, except
 the pages use the 'mobile.css' stylesheet, making it mobile
 device friendly. 

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
# It also defaults to blocking mode, but if we wanted it to run
# non-blocking, i.e. the loop() routine continues as normal while 
# the server runs in the background, we could say:
#  server = BBIOServer(blocking=False)


def voltage(analog_pin):
  """ Takes analog reading from given pin and returns a string 
      of the voltage to 2 decimal places. """
  return "%0.2f" % inVolts(analogRead(analog_pin))

def print_entry(text):
  """ Just prints the given text. """
  print "Text entered: \n  '%s'" % text

def setup():
  # Set the LEDs we'll be ontrolling as outputs:
  pinMode(USR2, OUTPUT)
  pinMode(USR3, OUTPUT)

  # Create our first page with the title 'PyBBIO Test', specifying the
  # mobile device stylesheet:
  home = Page("PyBBIO Test", stylesheet="mobile.css")
  # Add some text to the page:
  home.add_text("This is a test of the BBIOServer library for PyBBIO, "+\
                "using the 'mobile.css' mobile device stylesheet. " +\
                "Follow the links above to test the different pages.")                 
  # Create a new page to test the text input:
  text = Page("Text Input", stylesheet="mobile.css")
  text.add_text("Press submit to send the text in entry box:")

  # Create the text entry box on a new line; button will say 'Submit',
  # and when submitted the text in the box will be sent to print_entry():
  text.add_entry(lambda text: print_entry(text), "Submit", newline=True)

  # Create a new page to test the buttons and monitors:
  io = Page("I/O", stylesheet="mobile.css")
 
  # Make a LED control section using a heading:
  io.add_heading("LED Control")
  io.add_text("Control the on-board LEDs", newline=True)

  # Add a button on a new line with the label 'Toggle USR2 LED' that will
  # call 'toggle(USR2)' when pressed:
  io.add_button(lambda: toggle(USR2), "Toggle USR2 LED", newline=True)

  # Add a monitor which will continually call 'pinState(USR2)' and 
  # display the return value in the form: 'current state: [value]':
  io.add_monitor(lambda: pinState(USR2), "current state:")

  # Same thing here with the other LED:
  io.add_button(lambda: toggle(USR3), "Toggle USR3 LED", newline=True)
  io.add_monitor(lambda: pinState(USR3), "current state:")

  # Create another section for ADC readings:
  io.add_heading("ADC Readings")
  io.add_text("Read some ADC inputs", newline=True)

  # Add a monitor to display the ADC value:
  io.add_monitor(lambda: analogRead(AIN0), "AIN0 value:", newline=True)

  # And one on the same line to display the voltage using the voltage()
  # function defined above. Because the units variable is used this time
  # the value will be displayed in the form: 'voltage: [value] v':
  io.add_monitor(lambda: voltage(AIN0), "voltage:", units="v")

  # Same thing here:
  io.add_monitor(lambda: analogRead(AIN1), "AIN1 value:", newline=True)
  io.add_monitor(lambda: voltage(AIN1), "voltage:", units="v")

  # Then start the server, passing it all the pages. The first page
  # passed in will be the home page:
  server.start(home, text, io)


def loop():
  # We're running in blocking mode, so we won't get here until ctrl-c
  # is preseed. 
  print "\nServer has stopped"
  stop()



# Then run it the usual way:
run(setup, loop)

# Now, on a computer on the same network as you beaglebone, open your
# browser and navigate to:
#  your_beaglebone_ip:8000 
#  (replacing 8000 if you specified a different port)
# You should be redirected to your_beaglebone_ip:8000/pages/PyBBIOTest.html

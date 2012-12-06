"""
 DACx311.py 
 Alexander Hiam - 11/2012
 
 Example program for PyBBIO's DACx311 library to 
 output a triangle wave.

 This example program is in the public domain.
"""

from bbio import *
from DACx311 import *

# Set variables for the pins connected to the DAC:
data_pin = GPIO1_6  # P8.3
clk_pin  = GPIO1_7  # P8.4
sync_pin = GPIO1_2  # P8.5

# Create an instance of the DAC class:
dac = DAC7311(data_pin, clk_pin, sync_pin)

# Set a few global variables:
volts     = 0.0 # Initial voltage
increment = 0.1 # Ammount to increment volts by each time
pause     = 75  # ms to wait between each increment

def setup():
  # Nothing to do here, the DACx311 class sets pin modes
  pass

def loop():
  global volts, increment
  # Set voltage in volts and increment:
  dac.setVolts(volts)
  volts += increment

  # If at upper or lower limit, negate the incrememnt value:
  if((volts >= 3.3) or (volts <= 0)):
    # Notice here that it's still possible that volts is either
    # above 3.3 or below 0, and it won't be incremented again until
    # after the DAC is next set. That's OK though, because values
    # passed to the DACx311 class are checked and constrained to
    # within this range.
    increment = -increment

  # Wait a bit:
  delay(10)

# Run the program:
run(setup, loop)

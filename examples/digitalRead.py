# digitalRead.py - Alexander Hiam - 2/2012
# USR3 LED mirrors GPIO1_6 until CTRL-C is pressed.

# Import PyBBIO library:
from bbio import *

# Create a setup function:
def setup():
  # Set the GPIO pins:
  pinMode('USR3', OUTPUT)
  pinMode('GPIO1_6', INPUT)

# Create a main function:
def main():
  state = digitalRead('GPIO1_6')
  digitalWrite('USR3', state)
  # It's good to put a bit of a delay in if possible
  # to keep the processor happy:
  sleep(0.1)

# Start the loop:
run(setup, main)

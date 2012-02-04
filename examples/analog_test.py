# analog_test.py - Alexander Hiam
# Testing analogRead()

# Import PyBBIO library:
from bbio import *

# Create a setup function:
def setup():
  # Nothing to do here

# Create a main function:
def main():
  print analogRead(AIN7)
  sleep(0.5)

# Start the loop:
run(setup, main)

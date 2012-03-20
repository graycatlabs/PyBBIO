# analog_test.py - Alexander Hiam
# Testing analogRead()

# Import PyBBIO library:
from bbio import *

# Create a setup function:
def setup():
  # Nothing to do here
  pass

# Create a main function:
def main():
  print analogRead('VSYS')
  sleep(0.5)

# Start the loop:
run(setup, main)

# switch.py - Alexander Hiam - 2/2012
#
# Uses a switch to toggle the state of two LEDs.
# Demonstrates the use of global variables in Python.
# 
# The circuit:
#  - Momentary switch between 3.3v and GPIO1_15
#  - 10k ohm resistor from GPIO1_15 to ground
#  - Green LED from GPIO1_17 through 330 ohm resistor to ground
#  - Red LED from GPIO3_21 through 330 ohm resistor to ground
#
# This example is in the public domain

# Import PyBBIO library:
from bbio import *

SWITCH  = GPIO1_15 # P8.15
LED_GRN = GPIO1_17 # P9.23
LED_RED = GPIO3_21 # P9.25

LED_STATE = 0 # 0=green LED lit, 1=red LED lit.
SW_STATE  = 0 # =1 when switch pressed; only change LED_STATE
              # once per press.

# Create a setup function:
def setup():
  # Set the switch as input:
  pinMode(SWITCH, INPUT)
  # Set the LEDs as outputs:
  pinMode(LED_GRN, OUTPUT)
  pinMode(LED_RED, OUTPUT)
  
# Create a main function:
def main(): 
  global LED_STATE, SW_STATE 
  # Python requires you explicitely declare all global variables 
  # that you want to change within a code block using the global
  # statement; see:
  #  http://docs.python.org/reference/simple_stmts.html#the-global-statement

  if (digitalRead(SWITCH) == HIGH):
    if (SW_STATE == 0):
      # Just pressed, not held down.
      # Set SW_STATE and toggle LED_STATE
      SW_STATE = 1 
      LED_STATE ^= 1
    # Otherwise switch is held down, don't do anything.
  else:
    # Switch not pressed, reset SW_STATE:
    SW_STATE = 0

  if (LED_STATE == 0):
    digitalWrite(LED_GRN, HIGH)
    digitalWrite(LED_RED, LOW)
  else:
    digitalWrite(LED_GRN, LOW)
    digitalWrite(LED_RED, HIGH)
  # It's good to put a bit of a delay in if possible
  # to keep the processor happy:
  delay(50)

# Start the loop:
run(setup, main)

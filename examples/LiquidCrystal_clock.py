"""
 LiquidCrystal_clock.py 
 Alexander Hiam <alex@graycat.io> 

 An example to demonstrate the use of the LiquidCrystal library
 included with PyBBIO. Displays the date and time on a 16x2 character
 LCD.

 This example program is in the public domain.
"""
from bbio import *
# Import the LiquidCrystal class from the LiquidCrystal library:
from bbio.libraries.LiquidCrystal import LiquidCrystal
from time import strftime

RS_PIN = GPIO0_30
RW_PIN = GPIO0_31
EN_PIN = GPIO1_16
D4_PIN = GPIO0_5
D5_PIN = GPIO0_13
D6_PIN = GPIO0_3
D7_PIN = GPIO1_17

lcd = LiquidCrystal(RS_PIN, RW_PIN, EN_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN)

last_date = ''
last_time = ''

def setup():
  lcd.begin(16, 2) # (columns, rows)
 
def loop():
  global last_date, last_time
  date = strftime("%x") # date in locale's standard format
  time = strftime("%X") # time in locale's standard format

  if date != last_date or time != last_time:
    # Only update the display if the date or time has changed. This
    # reduces the flicker you see when repeatedly writing the same
    # string.
    lcd.clear() # clear the screen
    lcd.home()  # return to column 0, row 0
    lcd.prints(date) 
    lcd.goto(0, 1) # go to column 0, row 1 
    lcd.prints(time)
    last_date = date
    last_time = time
  delay(10)
  
run(setup, loop)
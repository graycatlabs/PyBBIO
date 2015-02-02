"""
 LiquidCrystal_glyph.py 
 Alexander Hiam <alex@graycat.io> 

 An example to demonstrate the use of the LiquidCrystal library
 included with PyBBIO. Demonstrates creating and displaying custom
 characters.

 This example program is in the public domain.
"""
from bbio import *
# Import the LiquidCrystal class from the LiquidCrystal library:
from bbio.libraries.LiquidCrystal import LiquidCrystal

RS_PIN = GPIO0_30
RW_PIN = GPIO0_31
EN_PIN = GPIO1_16
D4_PIN = GPIO0_5
D5_PIN = GPIO0_13
D6_PIN = GPIO0_3
D7_PIN = GPIO1_17

lcd = LiquidCrystal(RS_PIN, RW_PIN, EN_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN)

# This is how the custom 5x8 characters are defined:
glyph0 = [
  0b00000,
  0b00000,
  0b01110,
  0b10001,
  0b10010,
  0b10001,
  0b01110,
  0b00000,
]

glyph1 = [
  0b00000,
  0b00000,
  0b01110,
  0b10001,
  0b01001,
  0b10001,
  0b01110,
  0b00000,
]

glyph2 = [
  0b00000,
  0b01110,
  0b10001,
  0b11011,
  0b10001,
  0b11011,
  0b10101,
  0b00000,
]

def setup():
  lcd.begin(16, 2) # (columns, rows)
  # Load the custom glyphs into the display's RAM:
  lcd.createGlyph(0, glyph0)
  lcd.createGlyph(1, glyph1)
  lcd.createGlyph(2, glyph2)

def loop():
  lcd.clear()
  lcd.home()
  lcd.scrollDisplay(-5)
  for i in range(3): 
    # Tell the display to put the given glyph at the current location:
    lcd.displayGlyph(2) 
  lcd.scrollCursor(1)
  lcd.displayGlyph(0)
  
  for i in range(21):
    lcd.scrollDisplay(1)
    delay(400)
  delay(200)
  
  lcd.clear()
  lcd.goto(16,1)
  for i in range(3): 
    lcd.displayGlyph(2)
  lcd.scrollCursor(1)
  lcd.displayGlyph(1)
  
  for i in range(21):
    lcd.scrollDisplay(-1)
    delay(400)
  delay(200)
  
run(setup, loop)
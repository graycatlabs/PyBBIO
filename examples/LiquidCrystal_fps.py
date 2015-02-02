"""
 LiquidCrystal_fps.py 
 Alexander Hiam <alex@graycat.io> 

 An example to demonstrate the use of the LiquidCrystal library
 included with PyBBIO. Calculated and displays the approximate maximum
 refresh rate when writing all characters on a 16x2 LCD.

 This example program is in the public domain.
"""
from bbio import *
from bbio.libraries.LiquidCrystal import LiquidCrystal
import string, time

RS_PIN = GPIO0_30
RW_PIN = GPIO0_31
EN_PIN = GPIO1_16
D4_PIN = GPIO0_5
D5_PIN = GPIO0_13
D6_PIN = GPIO0_3
D7_PIN = GPIO1_17

lcd = LiquidCrystal(RS_PIN, RW_PIN, EN_PIN, D4_PIN, D5_PIN, D6_PIN, D7_PIN)

def setup():
  lcd.begin(16, 2) # (columns, rows)
 
def loop():
  alphabet = string.lowercase
  line1 = alphabet[:16]
  line2 = alphabet[16:]+"012345"
  n_frames = 100 # number of frames to write
  start_time = time.time() 
  for i in range(n_frames):
    lcd.clear()
    lcd.home()
    lcd.prints(line1)
    lcd.goto(0, 1)
    lcd.prints(line2)
  duration = time.time() - start_time 
  fps = n_frames / duration
  lcd.clear()
  lcd.home()
  lcd.prints("refresh rate:")
  lcd.goto(0, 1)
  lcd.prints("%0.1f fps" % fps)
  exit()
  
run(setup, loop)
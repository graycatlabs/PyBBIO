"""
LiquidCrystal
Copyright 2015 - Alexander Hiam <alex@graycat.io>

A PyBBIO library for controlling HD44780 style character LCDs.
Supports 8, 16 and 20 character wide displays with 1, 2 and 4 rows. 
Does not support reading the controller's RAM.

LiquidCrystal is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
"""
import bbio

class LiquidCrystal(object):
  ON                         = 1
  OFF                        = 0
  BLINK                      = 1
  NOBLINK                    = 0

  COMMAND_CLEAR              = 0x1
  COMMAND_HOME               = 1<<1

  COMMAND_ENTRYMODE          = 1<<2
  ENTRYMODE_SHIFTRIGHT       = 1<<1
  ENTRYMODE_SHIFTDISPLAY     = 1
  
  COMMAND_DISPLAYCTRL        = 1<<3
  DISPLAYCONTROL_ON          = 1<<2
  DISPLAYCONTROL_CURSORON    = 1<<1
  DISPLAYCONTROL_CURSORBLINK = 1
  
  COMMAND_SHIFT              = 1<<4
  SHIFT_DISPLAY              = 1<<3
  SHIFT_RIGHT                = 1<<2

  COMMAND_FUNCTIONSET        = 1<<5
  FUNCTIONSET_8BIT           = 1<<4
  FUNCTIONSET_2LINE          = 1<<3
  FUNCTIONSET_FONT_5X11      = 1<<2
  
  COMMAND_CGRAM_ADDR         = 1<<6
  COMMAND_DDRAM_ADDR         = 1<<7
    
  def __init__(self, *pins):
    if len(pins) == 6 or len(pins) == 10:
      self.rs, self.enable = pins[:2] 
      self.data_pins = pins[2:]
      self.rw = None
    elif len(pins) == 7 or len(pins) == 11:
      self.rs, self.rw, self.enable = pins[:3] 
      self.data_pins = pins[3:]
    else:
      raise Exception("Invalid number of pins")

    if len(self.data_pins) == 4: self.mode_bits = 4
    else: self.mode_bits = 8
    self._display_ctrl = 0
    self._ddram_address = 0
    
  def begin(self, cols, rows): 
    """ Initializes the LCD driver and sets it to the given number of rows
        and columns. """  
    assert cols == 8 or cols == 16 or cols == 20, \
           "LiquidCrystal only supports 8, 16 and 20 row displays" 
    assert rows == 1 or rows == 2 or rows == 4, \
           "LiquidCrystal only supports 1, 2 and 4 column displays" 
    self.cols = cols
    self.rows = rows

    for pin in (self.rs, self.enable)+self.data_pins:
      bbio.pinMode(pin, bbio.OUTPUT)
    if self.rw: bbio.pinMode(self.rw, bbio.OUTPUT)
    
    bbio.digitalWrite(self.enable, bbio.LOW) # idle state
    
    # This is the initialization procedure as defined in the HD44780 datasheet:
    if self.mode_bits == 8: 
      self.writeCommand(self.COMMAND_FUNCTIONSET | self.FUNCTIONSET_8BIT)
    else: self._write4bits((self.COMMAND_FUNCTIONSET | self.FUNCTIONSET_8BIT)>>4)
    bbio.delay(5)

    if self.mode_bits == 8: 
      self.writeCommand(self.COMMAND_FUNCTIONSET | self.FUNCTIONSET_8BIT)
    else: self._write4bits((self.COMMAND_FUNCTIONSET | self.FUNCTIONSET_8BIT)>>4)
    bbio.delay(5)
    
    if self.mode_bits == 8: 
      self.writeCommand(self.COMMAND_FUNCTIONSET | self.FUNCTIONSET_8BIT)
    else: self._write4bits((self.COMMAND_FUNCTIONSET | self.FUNCTIONSET_8BIT)>>4)
    
    function_set = 0
    if self.mode_bits == 8: function_set = self.FUNCTIONSET_8BIT
    else:
      # Must put in 4 bit mode before we can set the rows and cols
      self._write4bits(self.COMMAND_FUNCTIONSET>>4)
    if self.rows > 1: function_set |= self.FUNCTIONSET_2LINE
    self.writeCommand(self.COMMAND_FUNCTIONSET | function_set)
    
    self.setDisplay(self.OFF)
    self.clear()
    self._entry_mode = self.ENTRYMODE_SHIFTRIGHT
    self.writeCommand(self.COMMAND_ENTRYMODE | self._entry_mode)
    self.setDisplay(self.ON)
  
  def clear(self):
    """ Clears all characters in the dispay's RAM. """
    self.writeCommand(self.COMMAND_CLEAR)
    bbio.delay(2)
    
  def home(self):
    """ Resets the scroll and puts the cursor at 0,0. """
    self.writeCommand(self.COMMAND_HOME)
    bbio.delay(2)
    
  def goto(self, col, row):
    """ Puts the cursor at the given column and row. """
    if row == 1: col += 0x40
    if self.rows == 4:
      if row == 2: col += 0x14
      elif row == 3: col += 0x54
    self._setDDRAMAddress((col & 0x7f))
    
  def prints(self, str):
    """ Prints the given string to the display, starting at the current cursor
        location. """
    for c in str:
      self.writeData(ord(c) & 0xff)
            
  def createGlyph(self, glyph_num, glyph):
    """ Puts the given glyph into the the display's custom glyph RAM at 
        location glyph_num, which can be 0-7. """
    assert glyph_num >= 0 and glyph_num < 8, "only 0-7 are valid glyphs"
    length = len(glyph)
    assert length == 40 or length == 8, "a glyph must by an array of length 8"
    start_addr = glyph_num*8
    self.writeCommand(self.COMMAND_CGRAM_ADDR | start_addr)
    for row in range(8):
      self.writeData(glyph[row] & 0x1f)
    # Return to DDRAM access mode:
    self._setDDRAMAddress(self._ddram_address)

  def displayGlyph(self, glyph_num):
    """ Display the glyph saved in the given location in the display's custom
        glyph RAM at the current cursor location. """
    assert glyph_num >= 0 and glyph_num < 8, "only 0-7 are valid glyphs"
    self.writeData(glyph_num)
  
  def scrollDisplay(self, ammount):
    """ Scrolls the whole display the given ammount. Positive numbers scroll 
        the display to the right, negative to the left. """
    if ammount > 0: dir = self.SHIFT_RIGHT
    else: dir = 0
    for i in range(abs(ammount)):
      self.writeCommand(self.COMMAND_SHIFT | self.SHIFT_DISPLAY | dir)
      
  def  scrollCursor(self, ammount):
    """ Moves the cursor the given ammount. Positive numbers move it right,
        negative left. """
    if ammount > 0: dir = self.SHIFT_RIGHT
    else: dir = 0
    for i in range(abs(ammount)):
      self.writeCommand(self.COMMAND_SHIFT | dir)

  def setDisplay(self, state):
    """ Turns the display on if state is LiquidCrystal.ON, off if state is
        LiquidCrystal.OFF. Turning off the display will preserve the characters
        currently in the display's RAM. """
    if state == self.ON:
      self._display_ctrl |= self.DISPLAYCONTROL_ON
    else:
      self._display_ctrl &= ~self.DISPLAYCONTROL_ON
    self.writeCommand(self.COMMAND_DISPLAYCTRL | self._display_ctrl)
    
  def setCursor(self, state, blink):
    """ Set cursor visibility with state = LiquidCrystal.ON or 
        LiquidCrystal.OFF, set cursor blinking with blink = LiquidCrystal.BLINK
        or LiquidCrystal.NOBLINK. """
    if state == self.ON:
      self._display_ctrl |= self.DISPLAYCONTROL_CURSORON
    else: 
      self._display_ctrl &= ~self.DISPLAYCONTROL_CURSORON
    if blink == self.BLINK:
      self._display_ctrl |= self.DISPLAYCONTROL_CURSORBLINK
    else: 
      self._display_ctrl &= ~self.DISPLAYCONTROL_CURSORBLINK
    self.writeCommand(self.COMMAND_DISPLAYCTRL | self._display_ctrl)
   
  def leftToRight(self):
    """ Set string writing from left to right (default). """
    self._entry_mode |= self.ENTRYMODE_SHIFTRIGHT
    self.writeCommand(self.COMMAND_ENTRYMODE | self._entry_mode)
   
  def leftToRight(self):
    """ Set string writing from right to left. """
    self._entry_mode &= ~self.ENTRYMODE_SHIFTRIGHT
    self.writeCommand(self.COMMAND_ENTRYMODE | self._entry_mode)
    
  def autoscroll(self, state):
    """ If state = LiquidCrystal.ON then writing characters will shift the 
        entire display instead of just the cursor. Call with LiquidCrystal.OFF
        to disable. """
    if state == self.ON:
      self._entry_mode |= self.ENTRYMODE_SHIFTDISPLAY
    else:
      self._entry_mode &= ~self.ENTRYMODE_SHIFTDISPLAY
    self.writeCommand(self.COMMAND_ENTRYMODE | self._entry_mode)
       
  def writeCommand(self, command):
    """ Writes the given byte to the display in command mode. """
    bbio.digitalWrite(self.rs, bbio.LOW)
    self._writeByte(command)
  
  def writeData(self, data):
    """ Writes the given byte to the display in data mode. """
    bbio.digitalWrite(self.rs, bbio.HIGH)
    self._writeByte(data)
    
  def _write4bits(self, bits):
    """ Writes out the lowest 4 bits of the given value. """
    if self.rw: bbio.digitalWrite(self.rw, bbio.LOW)
    for bit in range(4):
      bbio.digitalWrite(self.data_pins[bit], (bits>>bit) & 0x1)
    bbio.digitalWrite(self.enable, bbio.HIGH)
    bbio.digitalWrite(self.enable, bbio.LOW)    
    
  def _writeByte(self, byte):
    """ Writes out the lowest byte of the given integer value. """
    if self.rw: bbio.digitalWrite(self.rw, bbio.LOW)
    bbio.digitalWrite(self.enable, bbio.LOW)
    if self.mode_bits == 8:
      for bit in range(8):
        bbio.digitalWrite(self.data_pins[bit], (byte>>bit) & 0x1)
      bbio.digitalWrite(self.enable, bbio.HIGH)
      bbio.digitalWrite(self.enable, bbio.LOW)
    else:
      self._write4bits(byte>>4)
      self._write4bits(byte)
  
  def _setDDRAMAddress(self, addr):
    """ Sets the current DDRAM address. """
    self.writeCommand(self.COMMAND_DDRAM_ADDR | addr)
    self._ddram_address = addr

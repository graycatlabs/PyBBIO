# io_test.py - Alexander Hiam 
# This was a quick test I wrote before starting in on PyBBIO.
# It's a good demonstration of how to use /dev/mem for hardware
# access. Blinks the on-board LED marked USR2

from mmap import mmap
import time, struct

GPIO1_offset = 0x4804c000  # Start of GPIO1 mux
GPIO1_size = 0x4804cfff-GPIO1_offset
GPIO_OE = 0x134
GPIO_SETDATAOUT = 0x194
GPIO_CLEARDATAOUT = 0x190
LED2 = 1<<22 # Pin 22 in gpio registers

f = open("/dev/mem", "r+b" )
map = mmap(f.fileno(), GPIO1_size, offset=GPIO1_offset) 
f.close() # Only needed to make map

# Grab the entire GPIO_OE register: 
packed_reg = map[GPIO_OE:GPIO_OE+4] # This is a packed string
# Unpack it:
reg_status = struct.unpack("<L", packed_reg)[0]
# Set LED1 bit low for output without effecting anything else:
reg_status &= ~(LED2)
# Repack and set register:
map[GPIO_OE:GPIO_OE+4] = struct.pack("<L", reg_status)

# blink 10 times:
for i in xrange(5):
  # Set it high:
  map[GPIO_SETDATAOUT:GPIO_SETDATAOUT+4] = struct.pack("<L", LED2)
  time.sleep(0.5) # Wait half a second
  # Set it low:
  map[GPIO_CLEARDATAOUT:GPIO_CLEARDATAOUT+4] = struct.pack("<L", LED2)
  time.sleep(0.5)

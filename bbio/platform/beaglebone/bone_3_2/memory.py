# memory.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone memory register access driver
#
# 16-bit register support mod from sbma44 - https://github.com/sbma44


from bbio.platform.beaglebone.bone_3_2 import bone_mmap

def andReg(address, mask, length=32):
  """ Sets 16 or 32 bit Register at address to its current value AND mask. """
  setReg(address, getReg(address, length)&mask, length)

def orReg(address, mask, length=32):
  """ Sets 16 or 32 bit Register at address to its current value OR mask. """
  setReg(address, getReg(address, length)|mask, length)

def xorReg(address, mask, length=32):
  """ Sets 16 or 32 bit Register at address to its current value XOR mask. """
  setReg(address, getReg(address, length)^mask, length)

def clearReg(address, mask, length=32):
  """ Clears mask bits in 16 or 32 bit register at given address. """
  andReg(address, ~mask, length)

def getReg(address, length=32):
  """ Returns unpacked 16 or 32 bit register value starting from address. """
  if (length == 32):
    return bone_mmap.getReg(address)
  elif (length == 16):
    return bone_mmap.getReg16(address)
  else:
    raise ValueError("Invalid register length: %i - must be 16 or 32" % length)

def setReg(address, new_value, length=32):
  """ Sets 16 or 32 bits at given address to given value. """
  if (length == 32):
      bone_mmap.setReg(address, new_value)
  elif (length == 16):
      bone_mmap.setReg16(address, new_value)
  else:
    raise ValueError("Invalid register length: %i - must be 16 or 32" % length)

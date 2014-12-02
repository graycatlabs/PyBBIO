# cape_manager.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone Cape Manager driver
# For Beaglebone's with 3.8 kernel or greater

from bbio.platform.beaglebone.config import SLOTS_FILE
from bbio.common import addToCleanup

def load(overlay, auto_unload=True):
  """ Attempt to load an overlay with the given name. If auto_unload=True it
      will be auto-unloaded at program exit (the current cape manager crashes
      when trying to unload certain overlay fragments). """
  with open(SLOTS_FILE, 'rb') as f:
    capes = f.read()
  if (',%s\n' % overlay) in capes:
    # already loaded
    return
  with open(SLOTS_FILE, 'wb') as f:
    f.write(overlay)
  if auto_unload:
    addToCleanup(lambda: unload(overlay))
    
def unload(overlay):
  """ Unload the first overlay matching the given name if present. Returns 
      True if successful, False if no mathcing overlay loaded. """ 
  with open(SLOTS_FILE, 'rb') as f:
    slots = f.readlines()
  for slot in slots:
    if overlay in slot:
      load('-%i' % int(slot.split(':')[0]))
      return True
  return False 

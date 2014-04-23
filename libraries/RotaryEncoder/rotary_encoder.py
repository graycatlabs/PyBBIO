
from bbio.platform import sysfs
from bbio import addToCleanup, cape_manager
from bbio import OCP_PATH

class RotaryEncoder(object):
  _eqep_dirs = [
    '%s/48300000.epwmss/48300180.eqep' % OCP_PATH,
    '%s/48302000.epwmss/48302180.eqep' % OCP_PATH,
    '%s/48304000.epwmss/48304180.eqep' % OCP_PATH
  ]
  
    
  def __init__(self, eqep_num):
    assert 0 <= eqep_num < 3, "eqep_num must be between 0 and 2"
 
    
    try:
      cape_manager.load('PyBBIO-bone_epeq%s' % eqep_num, 1)
      bbio.delay(250) # Give driver time to load
    except IOError:
      print "*Could not load bone_epeq%s overlay, resource busy" % eqep_num
      return
    
    self.eqep_num = eqep_num
    self.base_dir = self._eqep_dirs[eqep_num]
    self.mode = mode
    self.enable(self.mode)
    addToCleanup(self.disable)
    
  def enable(self,m):
    enable_file = "%s/enabled" % self.base_dir
    set_mode = "%s/mode" % self.base_dir
    return kernelFilenameIO(enable_file, 1) & kernelFilenameIO(enable_file, m)
    
  def disable(self):
    enable_file = "%s/enabled" % self.base_dir
    return kernelFilenameIO(enable_file, 0)

  def setAbsolute(self):
    '''
    Set mode as Absolute
    '''
    set_mode = "%s/mode" % self.base_dir
    return kernelFilenameIO(enable_file, 0)
    
  def setRelative(self):
    '''
    Set mode as Relative
    '''
    set_mode = "%s/mode" % self.base_dir
    return kernelFilenameIO(enable_file, 1)
    
  def getMode(self):
    mode_file = "%s/enabled" % self.base_dir
    return kernelFilenameIO(mode_file)

  def getPosition(self):
    '''
    Get the current position of the encoder
    '''
    position_file = "%s/position" % self.base_dir
    return kernelFilenameIO(position_file)
    
  def setFrequency(self,freq):
    '''
    Set the frequency in Hz at which the driver reports new positions.
    '''
    period_file = "%s/period" % self.base_dir
    return kernelFilenameIO(period_file,1000000000/freq)
    
  def setPosition(self,val):
    '''    
    Give a new value to the current position
    '''
    position_file = "%s/position" % self.base_dir
    return kernelFilenameIO(position_file,val)
    
  def zero():
    '''
    Set the current position to 0
    '''
    return setPosition(0)
    
    

  
    
    
    

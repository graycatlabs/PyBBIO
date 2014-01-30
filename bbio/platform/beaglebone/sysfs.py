# sysfs.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Helper routines for sysfs kernel drivers

import glob

def kernelFileIO(file_object, val=None):
  """ For reading/writing files open in 'r+' mode. When called just
      with a file object, will return contents of file. When called 
      with file object and 'val', the file will be overritten with 
      new value and the changes flushed. 'val' must be type str.
      Meant to be used with Kernel driver files for much more 
      efficient IO (no need to reopen every time). """  
  file_object.seek(0)
  if (val == None): return file_object.read()
  file_object.write(val)
  file_object.flush()


def kernelFilenameIO(fn, val=None):
  """ Same as kernelFileIO() but takes a filename instead of an already
      open file object. The filename should be a complete absolute path,
      and may inlcued asterisks, e.g. /sys/devices/ocp.*/some/file. """
  fn = glob.glob(fn)[0]
  with open(fn, 'r+') as f:
    return kernelFileIO(f, val)

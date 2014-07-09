# sysfs.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Helper routines for sysfs kernel drivers

import glob
from bbio.platform.util._sysfs import _kernelFileIO


def kernelFilenameIO(fn, val=''):
  """ Calls _kernelFileIO. The filename should be a complete absolute path,
      and may inlcued asterisks, e.g. /sys/devices/ocp.*/some/file.
      For reading/writing files open in 'r+' mode. When called just
      with a file name, will return contents of file. When called
      with file name and 'val', the file will be overritten with
      new value and the changes flushed and returned. 'val' must be type str.
      Meant to be used with Kernel driver files for much more
      efficient IO (no need to reopen every time). """
  fn = glob.glob(fn)[0]
  return _kernelFileIO(fn, str(val))

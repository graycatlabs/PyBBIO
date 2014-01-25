# sysfs.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Helper routines for sysfs kernel drivers


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

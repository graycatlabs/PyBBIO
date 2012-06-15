#!/usr/bin/env python
# PyBBIO setup script

from distutils.core import setup
import fileinput, sys, os


# A bit of a hack here; replace line in config file to point to
# the libraries directory:
lib_path = os.path.join(os.getcwd(), 'libraries')
old_config_line = 'LIBRARIES_PATH = """Do not edit!"""\n'
new_config_line = 'LIBRARIES_PATH = "%s"\n' % lib_path
config_file = 'bbio/config.py'
config_str = open(config_file, 'rb').read()
with open(config_file, 'wb') as config:
  config.write(config_str.replace(old_config_line, new_config_line))


# Earlier versions of PyBBIO used a shell script to install the 
# bbio module, and it was put in a different directory than this 
# script will install it. The old install directory is before the 
# new in the Python search path, so we have to make sure to remove
# the old install if it is there:
old_install = ("/usr/lib/python2.7/bbio.py", 
               "/usr/lib/python2.7/bbio.pyo")
removed_old_install = False
for f in old_install:
  if os.path.exists(f):
    try:
      os.remove(f)
      removed_old_install = True
    except Exception as e:
      print ("**Error!**\nAn old PyBBIO install was found at %s\nbut could"+\
            " not be removed. Exception raised:\n%s\nAborting install.") %\
            (f, e)
      sys.exit(0)
if (removed_old_install):
  print \
"""
 An old installation of PyBBIO was removed, but its config file was
 preserved in ~/.pybbio/, in case any local customizations were made.
 If you have no need to save the old config file you can delete the
 entire ~/.pybbio/ directory, as all configuration is now contained 
 in the bbio package.
"""

# Finally we can install the package:
setup(name='PyBBIO',
      version='0.4',
      description='A Python library for Arduino-style hardware IO support on the Beaglebone',
      author='Alexander Hiam',
      author_email='ahiam@marlboro.edu',
      license='Apache 2.0',
      url='https://github.com/alexanderhiam/PyBBIO/wiki',
      packages=['bbio'])

# Now replace the local config file to original state to keep git
# from complaining when updating with 'git pull':
with open(config_file, 'wb') as config:
  config.write(config_str.replace(new_config_line, old_config_line))



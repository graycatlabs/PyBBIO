#!/usr/bin/env python
# PyBBIO setup script

import fileinput, sys, os


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


# A bit of a hack here; replace line in config file to point to
# the libraries directory:
lib_path = os.path.join(os.getcwd(), 'libraries')
old_config_line = 'LIBRARIES_PATH = """Do not edit!"""\n'
new_config_line = 'LIBRARIES_PATH = "%s"\n' % lib_path
config_file = 'bbio/config.py'
config_str = open(config_file, 'rb').read()
with open(config_file, 'wb') as config:
  config.write(config_str.replace(old_config_line, new_config_line))


# Finally we can install the package:
print "Installing PyBBIO..."

if (not "-f" in sys.argv):

  from distutils.core import setup

  setup(name='PyBBIO',
        version='0.5',
        description='A Python library for Arduino-style hardware IO support on the Beaglebone',
        author='Alexander Hiam',
        author_email='ahiam@marlboro.edu',
        license='Apache 2.0',
        url='https://github.com/alexanderhiam/PyBBIO/wiki',
        packages=['bbio'])

else: 
  # '-f' flag was given; force the install:
  # The Beaglebone's Python can have some issues with OpenSSL, which
  # causes the standard distutils install to crash. See: 
  #  https://github.com/alexanderhiam/PyBBIO/issues/5
  # This is a quick and dirty hack to make sure it installs while I
  # find a better solution:
  print "bypassing distutils"
  import shutil
  shutil.rmtree("/usr/lib/python2.7/site-packages/bbio", ignore_errors=True)
  shutil.copytree("bbio", "/usr/lib/python2.7/site-packages/bbio")


# Now replace the local config file to original state to keep git
# from complaining when updating with 'git pull':
with open(config_file, 'wb') as config:
  config.write(config_str.replace(new_config_line, old_config_line))
print "Finished!"

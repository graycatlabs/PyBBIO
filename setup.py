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


# Through version 0.5 distutils was used to install PyBBIO instead of 
# setuptools, and PyBBIO was installed into a different directory. This
# test looks for all the possible distutils install directories. If an
# old distutils install is found, the user is notified that it should be 
# removed and isntall is aborted:
possible_old_install_paths = ["/usr/local/lib/python2.7/dist-packages/",
                              "/usr/local/lib/python2.7/site-packages/",
                              "/usr/lib/python2.7/site-packages/",
                              "/usr/lib/python2.7/dist-packages/"]
for p in possible_old_install_paths:
  if os.path.exists(p + "bbio"):
    print \
""" 
An old installation of PyBBIO was found which must be removed manually 
before installation can continue. Remove old install with:
  # rm -rf %sbbio
  # rm -rf %sPyBBIO*
Then run the setup.py script again.
""" % (p, p)
    sys.exit(0)

# Some Angstrom images are missing the py_compile module; get it if not
# present:
import random
python_lib_path = random.__file__.split('random')[0]
if not os.path.exists(python_lib_path + 'py_compile.py'):
  print "py_compile module missing; installing to %spy_compile.py" %\
                                                          python_lib_path
  import urllib2
  url = "http://hg.python.org/cpython/raw-file/4ebe1ede981e/Lib/py_compile.py"
  py_compile = urllib2.urlopen(url)
  with open(python_lib_path+'py_compile.py', 'w') as f:
    f.write(py_compile.read())
  print "testing py_compile..."
  try:
    import py_compile
    print "py_compile installed successfully"
  except Exception, e:
    print "*py_compile install failed, could not import"
    print "*Exception raised:"
    raise e


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

try:
  from setuptools import setup, Extension

  warnings = []

  driver_extensions = []
  driver_packages = []
  driver_data = []


  # detect platform:
  platform = ''
  with open('/proc/cpuinfo', 'rb') as f:
    cpuinfo = f.read().lower() 
  if ('armv7' in cpuinfo and 
      ('am335x' in cpuinfo or 'am33xx' in cpuinfo)):
    platform = 'BeagleBone'

  import commands
  uname_status, uname = commands.getstatusoutput('uname -a')
  if uname_status > 0:
    exit('*uname failed, cannot detect kernel version! uname output:\n %s' % uname)
  if ('3.8' in uname):
    platform += ' Black'
  

  if (platform == 'BeagleBone Black'):
    # BeagleBone or BeagleBone Black with kernel >= 3.8
    driver_extensions = [Extension('bbio.platform.beaglebone.driver', 
                                   ['bbio/platform/beaglebone/src/beaglebone.c', 
                                    'bbio/platform/util/mmap_util.c'],
                                   include_dirs=['bbio/platform/util'])]
    driver_packages = ['bbio.platform.beaglebone']
    driver_data = [('bbio/platform', ['bbio/platform/beaglebone/api.py']),
                   ('bbio/platform/beaglebone', 
                    ['bbio/platform/beaglebone/3.8/config.py',
                     'bbio/platform/beaglebone/3.8/pinmux.py'])]


  elif (platform == 'BeagleBone'):
    # BeagleBone or BeagleBone Black with kernel < 3.8 (probably 3.2)
    driver_extensions = [Extension('bbio.platform.beaglebone.driver', 
                                   ['bbio/platform/beaglebone/src/beaglebone.c', 
                                    'bbio/platform/util/mmap_util.c'],
                                   include_dirs=['bbio/platform/util'])]
    driver_packages = ['bbio.platform.beaglebone']
    driver_data = [('bbio/platform', ['bbio/platform/beaglebone/api.py']),
                   ('bbio/platform/beaglebone', 
                    ['bbio/platform/beaglebone/3.2/config.py', 
                     'bbio/platform/beaglebone/3.2/pinmux.py'])]

    # Older Angstrom images only included support for one of the PWM modules
    # broken out on the headers, check and warn if no support for PWM2 module:
    if (not os.path.exists('/sys/class/pwm/ehrpwm.2:0')):
      w = "you seem to have an old BeagleBone image which only has drivers for\n"+\
          "the PWM1 module, PWM2A and PWM2B will not be available in PyBBIO.\n"+\
          "You should consider updating Angstrom!"
      warnings.append(w)


  setup(name='PyBBIO',
        version='0.6',
        description='A Python library for Arduino-style hardware IO support on single board Linux systems',
        author='Alexander Hiam',
        author_email='ahiam@marlboro.edu',
        license='Apache 2.0',
        url='https://github.com/alexanderhiam/PyBBIO/wiki',
        packages=['bbio', 'bbio.platform'] + driver_packages,
        ext_modules=driver_extensions, 
        data_files=driver_data)

  print "install finished with %i warnings" % len(warnings)
  if (len(warnings)):
    for i in range(len(warnings)):
      print "*Warning [%i]: %s\n" % (i+1, warnings[i])

  print "PyBBIO is now installed on your %s, enjoy!" % platform
except Exception, e:
  print "Install failed with exception:\n%s" % e

# Now replace the local config file to original state to keep git
# from complaining when updating with 'git pull':
with open(config_file, 'wb') as config:
  config.write(config_str.replace(new_config_line, old_config_line))


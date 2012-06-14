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

setup(name='PyBBIO',
      version='0.4',
      description='A Python library for Arduino-style hardware IO support on the Beaglebone',
      author='Alexander Hiam',
      author_email='ahiam@marlboro.edu',
      license='Apache 2.0',
      url='https://github.com/alexanderhiam/PyBBIO/wiki',
      packages=['bbio'],
     )

# Now replace the local config file to original state to keep git
# from complaining:
with open(config_file, 'wb') as config:
  config.write(config_str)



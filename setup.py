
import sys, os, shutil, glob


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

print "Installing PyBBIO..." 

from setuptools import setup, Extension, find_packages

install_requires = [
  'pyserial'
]

extensions = [
  Extension('bbio.platform.util._spi',
            ['bbio/platform/util/spimodule.c']),
  Extension('bbio.platform.util.sysfs',
            ['bbio/platform/util/sysfs.c']),  
  Extension('bbio.platform.beaglebone.gpio',
            ['bbio/platform/beaglebone/gpio.c',
             'bbio/platform/util/sysfs.c'],
            include_dirs=['bbio/platform/util']),
]

data_files = [
  # Install the BBIOServer src files to ~/.BBIOServer:
  ('%s/.BBIOServer/src' % os.getenv('HOME'), 
   glob.glob('bbio/libraries/BBIOServer/src/*.*')),

  # Install the DT overlays:
  ('/lib/firmware', 
   glob.glob('tools/overlays/compiled/*.dtbo')),
]

setup(name='PyBBIO',
      version='0.9.3',
      description='A Python library for Arduino-style hardware IO support on the BeagleBone and BeagleBone Black',
      long_description=open('README.md').read(),
      author='Alexander Hiam',
      author_email='alex@graycat.io',
      license='MIT License',
      url='https://github.com/graycatlabs/PyBBIO/wiki',
      download_url='https://github.com/graycatlabs/PyBBIO/tarball/v0.9.3',
      keywords=['BeagleBone', 'BeagleBone Black', 'IO', 'GPIO', 'ADC', 'PWM', 
                'I2C', 'SPI', 'bbio', 'eQEP'],
      packages=find_packages(),
      data_files=data_files,
      ext_modules=extensions, 
      install_requires=install_requires,
      platforms=['BeagleBone', 'BeagleBone Black'],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware'
      ])

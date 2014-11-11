
import sys, os, shutil


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

from setuptools import setup, Extension

install_requires = [
  'pyserial'
]

packages = ['bbio', 'bbio.platform', 'bbio.platform.util', 
            'bbio.platform.beaglebone', 'bbio.platform.beaglebone.bone_3_8',
            'bbio.platform.beaglebone.bone_3_2']

extensions = [Extension('bbio.platform.util._sysfs',
              ['bbio/platform/util/_sysfs.c']),
              Extension('bbio.platform.util._spi',
              ['bbio/platform/util/spimodule.c']),
              Extension('bbio.platform.beaglebone.bone_3_2.bone_mmap',
              ['bbio/platform/beaglebone/bone_3_2/bone_mmap.c',
               'bbio/platform/util/mmap_util.c'],
               include_dirs=['bbio/platform/util'])]
                                   
setup(name='PyBBIO',
      version='0.9.2',
      description='A Python library for Arduino-style hardware IO support on the BeagleBone and BeagleBone Black',
      long_description=open('README.md').read(),
      author='Alexander Hiam',
      author_email='hiamalexander@gmail.com',
      license='MIT License',
      url='https://github.com/alexanderhiam/PyBBIO/wiki',
      download_url='https://github.com/alexanderhiam/PyBBIO/tarball/v0.9.2',
      keywords=['BeagleBone', 'BeagleBone Black', 'IO', 'GPIO', 'ADC', 'PWM', 
                'I2C', 'SPI', 'bbio'],
      packages=packages,
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

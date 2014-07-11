
import sys, os, shutil

# detect platform:
PLATFORM = ''
with open('/proc/cpuinfo', 'rb') as f:
  cpuinfo = f.read().lower() 
if ('armv7' in cpuinfo and 
    ('am335x' in cpuinfo or 'am33xx' in cpuinfo)):
  PLATFORM = 'BeagleBone'

  import commands
  uname_status, uname = commands.getstatusoutput('uname -a')
  if uname_status > 0:
    exit('uname failed, cannot detect kernel version! uname output:\n %s' % uname)
  if ('3.2' in uname):
    PLATFORM += ' 3.2'
  else:
    PLATFORM += ' >=3.8'

assert PLATFORM, "Could not detect a supported platform, aborting!"

TASK = ''
if len(sys.argv) > 1:
  if sys.argv[1] == 'install':
    TASK = 'install'
  if sys.argv[0] == '-c':
    # happens when called by pip
    if len(sys.argv) > 2 and sys.argv[1] == 'develop':
      # pip is installing the package
      TASK = 'install'

def preinstall():

  # Check for device tree compiler:
  from distutils import spawn
  assert spawn.find_executable('dtc'), "dtc not installed, aborting!"

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

  # List of directories by relative path to copy to /usr/local/lib/PyBBIO/:
  dirs_to_copy = [
    'libraries',
    'examples'
  ]

  for d in dirs_to_copy:
    # Copy the libraries directory to /usr/local/lib:
    dst = '/usr/local/lib/PyBBIO/%s' % d
    src = os.path.join(os.getcwd(), d)
    if os.path.exists(dst):
      print "Found old PyBBIO '%s' directory, replacing" % d
      shutil.rmtree(dst)
    shutil.copytree(src, dst)


if TASK == 'install':
  preinstall()
  print "Installing PyBBIO..." 

from setuptools import setup, Extension

warnings = []

driver_extensions = []
driver_packages = []
driver_package_dirs = {}
driver_data = []

install_requires = [
  'pyserial',
  'smbus'
]

if 'BeagleBone' in PLATFORM:
  # 3.2 and 3.8, list common things:
  driver_packages += ['bbio.platform.beaglebone']
  driver_extensions += [Extension('bbio.platform.util._sysfs',
                                  ['bbio/platform/util/_sysfs.c']),
                        Extension('bbio.platform.util._spi',
                                   ['bbio/platform/util/spimodule.c'])]

if (PLATFORM == 'BeagleBone >=3.8'):
  # BeagleBone or BeagleBone Black with kernel >= 3.8  
  driver_packages += ['bbio.platform.beaglebone.bone_3_8']

  if TASK == 'install':
    os.system('python tools/install-bb-overlays.py')

elif (PLATFORM == 'BeagleBone 3.2'):
  # BeagleBone or BeagleBone Black with kernel < 3.8 (probably 3.2)
  driver_packages += ['bbio.platform.beaglebone.bone_3_2']
  
  driver_extensions += [Extension('bbio.platform.beaglebone.bone_3_2.bone_mmap',
                        ['bbio/platform/beaglebone/bone_3_2/bone_mmap.c',
                         'bbio/platform/util/mmap_util.c'],
                         include_dirs=['bbio/platform/util'])]
                                   
  # Older Angstrom images only included support for one of the PWM modules
  # broken out on the headers, check and warn if no support for PWM2 module:
  if (not os.path.exists('/sys/class/pwm/ehrpwm.2:0')):
    w = "you seem to have an old BeagleBone image which only has drivers for\n"+\
        "the PWM1 module, PWM2A and PWM2B will not be available in PyBBIO.\n"+\
        "You should consider updating Angstrom!"
    warnings.append(w)

setup(name='PyBBIO',
      version='0.9',
      description='A Python library for Arduino-style hardware IO support on the BeagleBone and BeagleBone Black',
      long_description=open('README.md').read(),
      author='Alexander Hiam',
      author_email='hiamalexander@gmail.com',
      license='MIT License',
      url='https://github.com/alexanderhiam/PyBBIO/wiki',
      download_url='https://github.com/alexanderhiam/PyBBIO/tarball/v0.9',
      keywords=['BeagleBone', 'BeagleBone Black', 'IO', 'GPIO', 'ADC', 'PWM', 'I2C', 'bbio'],
      packages=['bbio', 'bbio.platform', 'bbio.platform.util'] + driver_packages,
      package_dir=driver_package_dirs,
      ext_modules=driver_extensions, 
      install_requires=install_requires,
      platforms=['BeagleBone', 'BeagleBone Black'],
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Hardware'
      ])
#data_files=driver_data,

if TASK == 'install':
  print "install finished with %i warnings" % len(warnings)
  if (len(warnings)):
    for i in range(len(warnings)):
      print "*Warning [%i]: %s\n" % (i+1, warnings[i])
  print "PyBBIO is now installed on your %s, enjoy!" % PLATFORM

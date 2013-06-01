"""
 PyBBIO - bbio.py - v0.6
 Author: Alexander Hiam - ahiam@marlboro.edu - www.alexanderhiam.com
 Website: https://github.com/alexanderhiam/PyBBIO

 A Python library for hardware IO support on the TI Beaglebone.
 Currently only supporting basic digital and analog IO, but more 
 peripheral support is on the way, so keep checking the Github page
 for updates.

 Copyright 2012, 2013 Alexander Hiam

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import sys, time

from platform import *
from util import *
from config import LIBRARIES_PATH

sys.path.append(LIBRARIES_PATH)

def bbio_init():
  """ Pre-run initialization, i.e. starting module clocks, etc. """
  global START_TIME_MS
  START_TIME_MS = time.time()*1000
  platform_init()

def bbio_cleanup():
  """ Post-run cleanup, i.e. stopping module clocks, etc. """
  # Run user cleanup routines:
  for cleanup in ADDITIONAL_CLEANUP:
    try:
      cleanup()
    except Exception as e:
      # Something went wrong with one of the cleanup routines, but we
      # want to keep going; just print the error and continue
      print "*Exception raised trying to call cleanup routine '%s':\n  %s" %\
            (cleanup, e)
  platform_cleanup()

def delay(ms):
  """ Sleeps for given number of milliseconds. """
  time.sleep(ms/1000.0)

def delayMicroseconds(us):
  """ Sleeps for given number of microseconds > ~30; still working 
      on a more accurate method. """
  t = time.time()
  while (((time.time()-t)*1000000) < us): pass


# The following code detects if Python is running interactively,
# and if so initializes PyBBIO on import and registers PyBBIO's
# cleanup to be called at exit, otherwise it defines the run() and
# stop() methods for the file based control flow:
import __main__
if not hasattr(__main__, '__file__'):
  # We're in the interpreter, see: 
  #  http://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode
  bbio_init()
  print "PyBBIO initialized"
  import atexit
  def interactive_cleanup():
    bbio_cleanup()
    print "Finished PyBBIO cleanup"
  atexit.register(interactive_cleanup)

else:
  # Imported in a Python file, define run() and stop():
  def run(setup, loop):
    """ The main loop; must be passed a setup and a loop function.
        First the setup function will be called once, then the loop
        function wil be called continuously until a stop signal is 
        raised, e.g. CTRL-C or a call to the stop() function from 
        within the loop. """
    try:
      bbio_init()
      setup()
      while (True):
        loop()
    except KeyboardInterrupt:
      # Manual exit signal, clean up and exit happy
      bbio_cleanup()
    except Exception, e:
      # Something may have gone wrong, clean up and re-raise exception
      bbio_cleanup()
      raise e
      
  def stop():
    """ Preffered way for a program to stop itself. """
    raise KeyboardInterrupt # Expected happy stop condition in run()

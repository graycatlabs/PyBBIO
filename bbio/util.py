# util.py
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
#
# This file contains routines and variables that may need to be
# accessed by internal drivers, which cannot import the bbio.py
# file because it imports them.

import time

ADDITIONAL_CLEANUP = [] # See add_cleanup() below.
START_TIME_MS = 0 # Set in run() - used by millis() and micros().

START_TIME_MS = 0
def util_init():
  global START_TIME_MS
  START_TIME_MS = time.time()*1000

def addToCleanup(routine):
  """ Takes a callable object to be called during the cleanup once a 
      program has stopped, e.g. a function to close a log file, kill 
      a thread, etc. """
  ADDITIONAL_CLEANUP.append(routine)

def millis():
  """ Returns roughly the number of millisoconds since program start. """
  return time.time()*1000 - START_TIME_MS

def micros():
  """ Returns roughly the number of microsoconds since program start. """
  return time.time()*1000000 - START_TIME_MS*1000

def delay(ms):
  """ Sleeps for given number of milliseconds. """
  time.sleep(ms/1000.0)

def delayMicroseconds(us):
  """ Sleeps for given number of microseconds > ~30; still working 
      on a more accurate method. """
  t = time.time()
  while (((time.time()-t)*1000000) < us): pass

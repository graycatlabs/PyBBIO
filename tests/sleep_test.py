#!/usr/bin/env python
"""
 sleep_test.py - Alexander Hiam - 3/2012

 Testing the accuracy of different methods of sleeping
 in units of microseconds and milliseconds. Uses Python's
 time.sleep(), as well as usleep() and nanosleep() from libc
 using ctypes.

 This was written for testing delay methods for the Beaglebone,
 which did not have python ctypes installed by default for me.
 Install on the Beaglebone with:
   # opkg update && opkg install python-ctypes 
"""

import ctypes, time

#--- Microsecond delay functions: ---

# Load libc shared library:
libc = ctypes.CDLL('libc.so.6')


def sleepMicroseconds(us):
  """ Delay microseconds using time.sleep(). """
  time.sleep(us * 1e-6)

def delayMicroseconds(us):
  """ Delay microseconds with libc usleep() using ctypes. """
  libc.usleep(int(us))


class Timespec(ctypes.Structure):
  """ timespec struct for nanosleep, see:
      http://linux.die.net/man/2/nanosleep """
  _fields_ = [('tv_sec', ctypes.c_long), 
              ('tv_nsec', ctypes.c_long)]

libc.nanosleep.argtypes = [ctypes.POINTER(Timespec), 
                           ctypes.POINTER(Timespec)]
nanosleep_req = Timespec()
nanosleep_rem = Timespec()

def nanosleepMicroseconds(us):
  """ Delay microseconds with libc nanosleep() using ctypes. """
  if (us >= 1000000): 
    sec = us/1000000
    us %= 1000000
  else: sec = 0
  nanosleep_req.tv_sec = sec
  nanosleep_req.tv_nsec = int(us * 1000)

  libc.nanosleep(nanosleep_req, nanosleep_rem)

#------------------------------------

#--- Millisecond delay functions: ---

def sleepDelay(ms):
  """ Delay milliseconds using time.sleep(). """
  time.sleep(ms/1000.0)

def delay(ms):
  """ Delay milliseconds with libc usleep() using ctypes. """
  ms = int(ms*1000)
  libc.usleep(ms)

def betterDelay(ms):
  """ Delay milliseconds with libc usleep() using ctypes and
      some simple error compensation. """
  if (ms >= 0.1):
    # Fix some of the error calculated through testing 
    # different sleep values on the Beaglebone, change 
    # accordingly:
    ms -= 0.1 
  ms = int(ms*1000)
  libc.usleep(ms)

#------------------------------------

#--- Tests: -------------------------

def test_delayus(delayus):
  """ Tests microsecond delay function. """

  n_tests = [1000, 1000, 1000, 500, 500, 250, 100,  100,      10,       2]
  tests   = [   0,  0.5,    1,  10,  50, 100, 500, 1000,  100000, 1000000]

  total_error = 0.0
  time_no_delay = 0 

  for i in range(len(n_tests)):
    total = 0.0
    error = 0.0
    for j in range(n_tests[i]):
      before = time.time()
      t = tests[i]
      if (t != 0): 
        delayus(t)
        # If testing no delay, i.e. t=0, then we don't
        # call the delay function. That way we can record
        # the time it takes to call the time() functions,
        # get test values, etc.
      total += time.time() - before 

    avg = (total/n_tests[i])
    avg *= 1000000 # sec -> usec
    # Subtract time recorded without calling delayus():
    avg -= time_no_delay 
    if (t == 0): time_no_delay = avg # Record no delay time
    error = abs(avg-t)
    if (t): 
      total_error += error
      # Because our no delay test doesn't call delayus(),
      # it wouldn't make sense to include it in our average error.
    print "%10.1f usec delay: time = %0.3f usec, error = %0.3f" %\
           (tests[i], avg, error)

  print "\n  avg error = +- %0.3f usec\n" % (total_error/len(n_tests))


def test_delayms(delayms):  
  """ Tests millisecond delay function. """

  n_tests = [1000, 1000, 1000, 1000,  100,   40,  10,   4,    2,   1]
  tests   = [   0,  0.1,  0.5,    1,   10,  50, 100, 500, 1000, 5000]

  # Uncomment to test a 1 minute delay:
  #tests.append(60000); n_tests.append(1)

  total_error = 0.0
  time_no_delay = 0 

  for i in range(len(n_tests)):
    total = 0.0
    error = 0.0
    for j in range(n_tests[i]):
      before = time.time()
      t = tests[i]
      if (t != 0): 
        delayms(t)
        # If testing no delay, i.e. t=0, then we don't
        # call the delay function. That way we can record
        # the time it takes to call the time() functions,
        # get test values, etc.
      total += time.time() - before 

    avg = (total/n_tests[i])
    avg *= 1000 # sec -> msec
    # Subtract time recorded without calling delayms():
    avg -= time_no_delay 
    if (t == 0): time_no_delay = avg # Record no delay time
    error = abs(avg-t)
    if (t): 
      total_error += error
      # Because our no delay test doesn't call delayms(),
      # it wouldn't make sense to include it in our average error.
    print "%10.1f msec delay: time = %0.3f msec, error = %0.3f" %\
           (tests[i], avg, error)

  print "\n  avg error = +- %0.3f msec\n" % (total_error/len(n_tests))

#------------------------------------


print "\n Microsecond delay using time.sleep():"
test_delayus(sleepMicroseconds)
print 20*'-'
print "\n Microsecond delay using ctypes and usleep():"
test_delayus(delayMicroseconds)
print 20*'-'
print "\n Microsecond delay using ctypes and nanosleep():"
test_delayus(nanosleepMicroseconds)
print 20*'-'

print "\n Millisecond delay using time.sleep():"
test_delayms(sleepDelay)
print 20*'-'
print "\n Millisecond delay using ctypes and usleep():"
test_delayms(delay)
print 20*'-'
print "\n Millisecond delay using ctypes and usleep() \n\
 with simple error compensation:"
test_delayms(betterDelay)
print 20*'-'


#!/usr/bin/env python
"""
 SafeProcess_test.py 
 Alexander Hiam

 An example to demonstrate the use of the SafeProcess library
 for PyBBIO.

 This example program is in the public domain.
"""

from bbio import *
from SafeProcess import *

def foo():
  while(True):
    print "foo"
    delay(1000)

def setup():
  p = SafeProcess(target=foo)
  p.start()

def loop():
  print "loop"
  delay(500)

run(setup, loop)

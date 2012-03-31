# A quick test to demonstrate the libraries directory scheme.
# 
# imports and tests PyBBIO/libraries/example.py

try:
  import example
except:
  print "\nWe can't import the PyBBIO library until we've imported bbio"

print "Importing bbio"
from bbio import *

print "now we can import example"
import example

print "testing example library:"
example.foo()

#!/usr/bin/env python

'''
 phant_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the PhantStream library
 for PyBBIO.
 It reads from the analog pin and 

 This example program is in the public domain.


To use the PhantStream library:
make a steam on the phant server
https://data.sparkfun.com/streams/make
or install phant on the bbb and get the 
public key, private key and the url
PhantStream("*public key*",(optional)"*private key*"\
,(optional)"*url*")
if the stream is being hosted on Spark Fun's server, 
it can be left blank. 
For additional information read the wiki page.
https://github.com/alexanderhiam/PyBBIO/wiki/PhantStream
'''
from bbio import *
from PhantStream import *


pot = AIN0
p = PhantStream("*public key*","*private key*")
def setup():
  pass
  
def loop():
  val = analogRead(pot)
  v = inVolts(val)
  p.send(voltage=v)
  delay(1000)
  
run(setup,loop)
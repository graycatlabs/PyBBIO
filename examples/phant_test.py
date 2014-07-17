#!/usr/bin/env python

'''
 phant_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the PhantStream library
 for PyBBIO.

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
'''
from bbio import *
from PhantStream import *


pot = AIN0
p = PhantStream("*public key*","*private key*")
def setup():
  pass
  
def loop():
  val = analogRead(pot)
  voltage = inVolts(val)
  p.send(volts=voltage)
  delay(500)
  
run(setup,loop)
'''
PhantStream - v0.1
Copyright 2014 Rekha Seethamraju

Library for using Spark Fun's Phant IoT server from the 
Beaglebone Black

PhantStream is released as part of PyBBIO under its MIT license.
See PyBBIO/LICENSE.txt
'''
from bbio import *
import json, urllib, os, urllib2

class PhantStream(object):
  def __init__(self, public_key, private_key="", url="https://data.sparkfun.com/"):
    '''
    PhantStream(public_key,(optional)private_key, (optional)url)
    all arguments must be sent as strings.
    private_key is required for sending data to or clearing the server.
    If data is being being hosted on data.sparkfun.com, the url field can be empty
    If data is being being hosted on the beaglebone, url must be mentioned.
    '''
    self.public_key = str(public_key)
    self.private_key = str(private_key)
    self.url = url
    self.url_read = os.path.join(url,"output",self.public_key)
    self.url_send = os.path.join(url,"input",self.public_key)
    
  def send(self,samples):
    '''
    send(samples)
    samples must be a dictionary
    requires the private key
    returns successful if log was successful else returns error message
    '''
    try:
      assert self.private_key!="", "private key required for logging"
      data =urllib.urlencode(samples)
      headers = {
         'Phant-Private-Key' : self.private_key,
         'Content-type': 'application/x-www-form-urlencoded'
          }
      req = urllib2.Request(self.url_send, data, headers)
      response = urllib2.urlopen(req)
      return response.read()
      
    except urllib2.HTTPError as hpe:
      print hpe

  def getJSON(self):
    '''
    getJSON()
    returns the logged data as a list of dictionaries i.e in .json format
    '''
    try:
      f = urllib2.urlopen(self.url_read+".json")
      return f.read()
    except urllib2.HTTPError as hpe:
      print hpe
    
  def getCSV(self):
    '''
    getCSV()
    returns the logged data as a .csv
    '''
    try:
      f = urllib2.urlopen(self.url_read+".csv")
      return f.read()
    except urllib2.HTTPError as hpe:
      print hpe
    
  def getJSONinFile(self,file_name):
    '''
    getJSONinFile("file_name")
    writes the logged data in .json to the file specified by file_name
    '''
    data = self.getJSON()
    with open(file_name, 'w') as outfile:
      json.dump(data, outfile)

  def getCSVinFile(self,file_name):
    '''
    getCSVinFile("file_name")
    writes the logged data in .csv to the file specified by file_name
    '''
    csv = self.getCSV()
    fp = open(file_name, "wb")
    fp.write(csv)
    fp.close()
      
  def clear(self):
    '''
    clear()
    clears the logged data in the stream
    requires private key.
    returns message from server.
    '''
    try:
      assert self.private_key!="", "private key required for logging"
      url_send = self.url_send+"/clear?private_key="+self.private_key
      f = urllib2.urlopen(url_send)
      return f.read()
    except urllib2.HTTPError as hpe:
      print hpe

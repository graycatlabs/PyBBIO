from bbio import *

class PhantStream(object):
  def __init__(self, public_key, private_key="", url="https://data.sparkfun.com/"):
   self.public_key = public_key
   self.private_key = private_key
   self.url_read = url+"output/"+self.public_key
   self.url_send = url+"input/"+self.public_key

  def send(self, **samples):
    url = self.url_send+"?private_key="+self.private_key
    for field, value in samples.iteritems():
      url = url+"&"+field+"="+value
    requests.post(url)
    
  def getJSON(self):
    url = self.url_read+".json"
    r = requests.get(url)
    return r.json()
    
  def getCSV(self):
    url = self.url_read()+".csv"
    r = requests.get(url)
    return r.text
    
  
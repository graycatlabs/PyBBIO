import os, glob, cape_manager
from bbio.platform.spimodule import SPI

'''
BB-SPIDEV0-00A0.dtbo	      
BB-SPIDEV1-00A0.dtbo	      
BB-SPIDEV1A1-00A0.dtbo
ADAFRUIT-SPI0-00A0.dtbo   
ADAFRUIT-SPI1-00A0.dtbo
'''

class spi(object):
    
  def __init__(self, spi_num):
      
      self.spi_num = spi_num
      
      assert 0 <= spi_num < 2, "SPI must be between 0 or 1"
    
      overlay = 'BB-SPIDEV%i-00A0' % spi_num
      assert os.path.exists('/lib/firmware/%s.dtbo' % overlay), \
       "SPI driver not present"
    
      cape_manager.load(overlay)
      bbio.delay(250) # Give driver time to load
    
    

  def begin(self,device):
      '''
      begin(device no)
      Connects the BBB to the specified SPI device
      '''
      return open(spi_num,device)

  def end(self):
     '''
     end()
     Disconnects the object from the interface
     ''' 
     return close()
     
  def read(self,noofbytes):
      '''
      read(len)
      Read len bytes from SPI device
      '''
      return readbytes(noofbytes)

  def write(self,list):
      '''
      write([list])
      Write bytes to SPI device
      '''
      return writebytes(list)
      
  def transfer2(self,list,delay):
      '''
      transfer1([list],delay)
      Perform SPI transaction.
      CS will be released and reactivated between blocks.
      delay specifies delay in usec between blocks.
      '''
      return xfer(list,delay)
      
  def transfer(self,list):
      '''
      transfer1([list])
      Perform SPI transaction.
      CS will be held active between blocks.
      '''
      return xfer2(list)

      
     

# Initialize the global SPI  instances:
SPI0 = spi('0')
SPI0 = spi('1')
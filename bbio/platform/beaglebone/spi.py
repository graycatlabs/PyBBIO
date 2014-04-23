
from bbio.platform import _spi
from spi_init import spi_init
from config import MSBFIRST, LSBFIRST

class SPI_Bus(object):
    
  def __init__(self, spi_bus, spi_dev):
      
    self.spi_bus = spi_bus
    self.spi_dev = spi_dev
    assert 0 <= spi_bus < 2, "spi_bus must be between 0 or 1"
    assert 0 <= spi_dev < 2, "spi_dev must be between 0 or 1"
    
    self.spidev = _spi.SPI()
    
  def begin(self):
    '''
    begin(device no)
    Connects the BBB to the specified SPI device
    '''
    spi_init(self.spi_bus)

    self.spidev.open(self.spi_bus+1, self.spi_dev)

  def end(self):
    '''
    end()
    Disconnects the object from the interface
    ''' 
    self.spidev.close()
     
  def read(self,noofbytes):
    '''
    read(len)
    Read len bytes from SPI device
    '''
    return self.spidev.readbytes(noofbytes)

  def write(self,list):
    '''
    write([list])
    Write bytes to SPI device
    '''
    self.spidev.writebytes(list)
      
  def transfer(self,list):
    '''
    transfer1([list])
    Perform SPI transaction.
    CS will be held active between blocks.
    '''
    return self.spidev.xfer2(list)

  def setDataMode(self,mode):
    '''
    setDataMode(mode)
    SPI mode as two bit pattern of 
    Clock Polarity  and Phase [CPOL|CPHA]
	min: 0b00 = 0 max: 0b11 = 3
    '''
    self.spidev.mode()=mode
    
  def setBitOrder(self,lsbf):
    '''
    setBitOrder(lsbfirst)
    for lsb first 1
    for msb first 0     
    '''
    self.spidev.lsbfirst=lsbf
    
  def setMaxFreq(self,freq):
    '''
    setMaxFreq(freq)
    maximum speed in Hz
    '''
    self.spidev.msh=freq
    
  def CShigh(self):
    '''
    CShigh()
    makes CS active high
    '''
    self.spidev.cshigh=1


# Initialize the global SPI  instances:
SPI0 = SPI_Bus(0, 0)
SPI1 = SPI_Bus(1, 0)

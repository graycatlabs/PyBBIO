import bbio, os, cape_manager
from bbio.platform.util import _spi
from config import LSBFIRST,MSBFIRST


def spi_init(spi_num):
  overlay = 'BB-SPIDEV%i' % spi_num
  assert os.path.exists('/lib/firmware/%s-00A0.dtbo' % overlay), \
    "SPI driver not present"
  cape_manager.load(overlay, auto_unload=False)
  bbio.delay(250) # Give driver time to load

class SPI_Bus(object):
    
  def __init__(self, spi_bus):
      
    self.spi_bus = spi_bus
    assert 0 <= spi_bus < 2, "spi_bus must be 0 or 1"
    self._running = False
    self.spidev_cs0 = _spi.SPI()
    self.spidev_cs1 = _spi.SPI()
    
  def begin(self):
    '''
    SPIx.begin()
    Must be called at the start to initialise the bus.
    Connects the BBB to the SPI Bus specified. 
    Initialises both the devices on the bus.
    '''
    spi_init(self.spi_bus)
    self.spidev_cs0.open(self.spi_bus+1,  0)
    self.spidev_cs1.open(self.spi_bus+1,  1)
    self._running = True

  def end(self):
    '''
    SPIx.end()
    Disconnects the bus from the interface
    ''' 
    self.spidev_cs0.close()
    self.spidev_cs1.close()

     
  def read(self,cs,n_bytes):
    '''
    SPIx.read(chip_select, no_of_bytes_to_be_read)
    chip_select must be either 0 or 1 based on the device to read from.
    Read no_of_bytes_to_be_read bytes from SPI device selected by chip_select.
    Returns the data read from the device 
    as a list whose each element contains 1 byte 
    '''
    assert self._running, "Must call SPIx.begin() before using read()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if cs == 0:
      return self.spidev_cs0.readbytes(n_bytes)
    else:
      return self.spidev_cs1.readbytes(n_bytes)
      

  def write(self,cs,data):
    '''
    SPIx.write(chip_select,[list])
    Writes each element in the list to SPI device specified by the chip_select
    Does not return anything.
    '''
    assert self._running, "Must call SPIx.begin() before using write()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if type(data) == str:
      data = [ord(c) for c in data]
    elif type(data) == int:
      data = [data & 0xff]
    #elif type(data) == list or type(data) == tuple:
    # data = map(lambda x: int(x) & 0xff, data)
    if cs == 0:
      self.spidev_cs0.writebytes(data)
    else:
      self.spidev_cs1.writebytes(data)
      
  def transfer(self,cs,data):
    '''
    SPIx.transfer(chip_select,[list])
    Performs SPI transaction. 
    Writes each element in the list to SPI device given by the chip_select.
    Simultaneously reads from the SPI device specified by the chip_select.
    CS will be held active between blocks.
    Returns the data read from the device as a list
    whose each element contains 1 byte.
    '''
    assert self._running, "Must call SPIx.begin() before using transfer()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if type(data) == str:
      data = [ord(c) for c in data]
    elif type(data) == int:
      data = [data & 0xff]
    elif type(data) == list or type(data) == tuple:
      data = map(lambda x: int(x) & 0xff, data)
    if cs == 0:
      return self.spidev_cs0.xfer2(data)
    else:
      return self.spidev_cs1.xfer2(data)


  def setDataMode(self,cs,mode):
    '''
    SPIx.setDataMode(chip_select,mode)
    Sets the Mode of the SPI device specified by chip_select.
    SPI mode as two bit pattern of Clock Polarity  and Phase [CPOL|CPHA].
	It can take a value between 0<= chip_select <=3.
      Mode 0 : base value of the clock is zero, data are captured on the 
               clock's rising edge and data is propagated on a falling edge.
      Mode 1 : the base value of the clock is zero, data are captured on the 
               clock's falling edge and data is propagated on a rising edge.
      Mode 2 : the base value of the clock is one, data are captured 
               on clock's falling edge and data is propagated on a rising edge.
      Mode 3 : the base value of the clock is one, data are captured on 
               clock's rising edge and data is propagated on a falling edge.
    '''
    assert self._running,"Must call SPIx.begin() before using setDataMode()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    assert 0 <= mode < 4, "Mode must be between 0 and 3"
    if cs == 0:
      self.spidev_cs0.mode=mode
    else:
      self.spidev_cs1.mode=mode
    
  def getDataMode(self,cs):
    '''
    SPIx.getDataMode(chip_select)
    Gets the Mode of the SPI device specified by chip_select.
    SPI mode has two bit pattern of Clock Polarity  and Phase [CPOL|CPHA].
    Mode 0 : base value of the clock is zero, data are captured on the 
             clock's rising edge and data is propagated on a falling edge.
    Mode 1 : the base value of the clock is zero, data are captured on the 
             clock's falling edge and data is propagated on a rising edge.
    Mode 2 : the base value of the clock is one, data are captured on 
             clock's falling edge and data is propagated on a rising edge.
    Mode 3 : the base value of the clock is one, data are captured on 
             clock's rising edge and data is propagated on a falling edge.
    Returns the mode of SPI device.
    '''
    assert self._running, "Must call SPIx.begin() before using getDataMode()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if cs == 0:
      return self.spidev_cs0.mode
    else:
      return self.spidev_cs1.mode
      
  def setBitOrder(self,cs,order):
    '''
    SPIx.setBitOrder(chip_select,order)
    Sets the BitOrder of the SPI device specified 
         by chip_select to LSB First or MSB First.
    order must be either LSBFIRST or MSBFIRST
    Returns the mode of SPI device.    
    '''
    assert self._running, "Must call SPIx.begin() before using setBitOrder()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    assert order == LSBFIRST or order == MSBFIRST, "order has to be \
                 either LSBFIRST or MSBFIRST"
    if order == LSBFIRST: 
      order = False
    else:
      order = True
    if cs == 0:
      self.spidev_cs0.lsbfirst=order
    else:
      self.spidev_cs1.lsbfirst=order
      
  def getBitOrder(self,cs):
    '''
    SPIx.getBitOrder(chip_select)
    Gets the Bit Order of the SPI device specified by 
                chip_select to LSB First or MSB First.
    for LSB first : 1
    for MSB first : 0  
    Returns the Bit Order of SPI device.   
    '''
    assert self._running, \
    "Must call SPIx.begin() before using getBitOrder()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if cs == 0:
      return self.spidev_cs0.lsbfirst
    else:
      return self.spidev_cs1.lsbfirst
    
  def setMaxFreq(self,cs,freq):
    '''
    SPIx.setMaxFreq(chip_select,freq)
    Sets the maximum frequency of the SPI device 
    specified by chip_select to freq in HZ.
    frequency has to be specified in Hz.
    '''
    assert self._running, "Must call SPIx.begin() before using setMaxFreq()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if cs == 0:
      self.spidev_cs0.msh=freq
    else:
      self.spidev_cs1.msh=freq
      
  def getMaxFreq(self,cs):
    '''
    SPIx.getMaxFreq(chip_select)
    Gets the maximum frequency of the SPI device specified by chip_select.
    maximum speed in Hz
    Returns the maximum frequency in Hz.
    '''
    assert self._running,"Must call SPIx.begin() before using getMaxFreq()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if cs == 0:
      return self.spidev_cs0.msh
    else:
      return self.spidev_cs1.msh

  def setCSActiveHigh(self,cs):
    '''
    SPIx.setCSActiveHigh(chip_select)
    Makes Chip Select pin of the SPI device given by chip_select active High
    '''
    assert self._running,"Must call SPIx.begin() before using CShigh()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if cs == 0:
      self.spidev_cs0.cshigh = True
    else:
      self.spidev_cs1.cshigh = True
      
  def setCSActiveLow(self,cs):
    '''
    SPIx.setCSActiveLow(chip_select)
    Makes Chip Select pin of the SPI device given by chip_select Active Low
    '''
    assert self._running, "Must call SPIx.begin() before using CSlow()"
    assert 0 <= cs < 2, "Chip Select must be 0 or 1"
    if cs == 0:
      self.spidev_cs0.cshigh = False
    else:
      self.spidev_cs1.cshigh= False
      

# Initialize the global SPI  instances:
SPI0 = SPI_Bus(0)
SPI1 = SPI_Bus(1)

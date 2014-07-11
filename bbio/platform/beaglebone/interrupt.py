# interrupt.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# MIT License
# 
# Beaglebone GPIO interrupt driver
#
# Most of the code in this file was written and contributed by 
# Alan Christopher Thomas - https://github.com/alanctkc
# Thanks!

from config import GPIO_FILE_BASE, RISING, FALLING, BOTH
import bbio, select, threading, os


INTERRUPT_VALUE_FILES = {}

class EpollListener(threading.Thread):
  def __init__(self):
    self.epoll = select.epoll()
    self.epoll_callbacks = {}
    self.first_interrupt_registered = False
    super(EpollListener, self).__init__()

  def run(self):
    while True:
      if len(self.epoll_callbacks) == 0: 
        if self.first_interrupt_registered:
          # At least one interrupt gas been registered in the past
          # and now all have been unregistered; stop thread:
          break
        else:
          # If we're here then the thread was just created and the
          # first interrupt hasn't been registered yet; wait for it:
          bbio.delay(100)
      events = self.epoll.poll()
      for fileno, event in events:
        if fileno in self.epoll_callbacks:
          if not self.epoll_callbacks[fileno]['has_fired']:
            # This is the first time an event has been reported for this
            # file; there is always an initial false event, so ignore:
            self.epoll_callbacks[fileno]['has_fired'] = True
            continue
          self.epoll_callbacks[fileno]['callback']()
        
  def register(self, gpio_pin, callback):
    """ Register an epoll trigger for the specified fileno, and store
        the callback for that trigger. """
    fileno = INTERRUPT_VALUE_FILES[gpio_pin].fileno()
    self.epoll.register(fileno, select.EPOLLIN | select.EPOLLET)
    self.epoll_callbacks[fileno] = {}
    self.epoll_callbacks[fileno]['callback'] = callback
    self.epoll_callbacks[fileno]['has_fired'] = False
    if not self.first_interrupt_registered:
      self.first_interrupt_registered = True
    
  def unregister(self, gpio_pin):
    fileno = INTERRUPT_VALUE_FILES[gpio_pin].fileno()
    self.epoll.unregister(fileno)
    INTERRUPT_VALUE_FILES[gpio_pin].close()
    del INTERRUPT_VALUE_FILES[gpio_pin]
    del self.epoll_callbacks[fileno]  

EPOLL_LISTENER = None
def _start_epoll_listener():
  global EPOLL_LISTENER
  if not EPOLL_LISTENER or not EPOLL_LISTENER.is_alive():
    EPOLL_LISTENER = EpollListener()
    EPOLL_LISTENER.daemon = True
    EPOLL_LISTENER.start()

def attachInterrupt(gpio_pin, callback, mode=BOTH):
  """ Sets an interrupt on the specified pin. 'mode' can be RISING, FALLING,
      or BOTH. 'callback' is the method called when an event is triggered. """
  # Start the listener thread
  _start_epoll_listener()
  gpio_num = int(gpio_pin[4])*32 + int(gpio_pin[6:])
  value_file = os.path.join(GPIO_FILE_BASE, 'gpio%i' % gpio_num, 'value')
  INTERRUPT_VALUE_FILES[gpio_pin] = open(value_file, 'r')
  _edge(gpio_pin, mode)
  EPOLL_LISTENER.register(gpio_pin, callback)

def detachInterrupt(gpio_pin):
  """ Detaches the interrupt from the given pin if set. """
  gpio_num = int(gpio_pin[4])*32 + int(gpio_pin[6:])
  EPOLL_LISTENER.unregister(gpio_pin)
  
def _edge(gpio_pin, mode):
  """ Sets an edge-triggered interrupt with sysfs /sys/class/gpio
      interface. Returns True if successful, False if unsuccessful. """
  gpio_num = int(gpio_pin[4])*32 + int(gpio_pin[6:])
  gpio_base = os.path.join(GPIO_FILE_BASE, 'gpio%i' % gpio_num)
  if (not os.path.exists(gpio_base)): 
    # Pin not under userspace control
    return False
  edge_file = os.path.join(gpio_base, 'edge')
  with open(edge_file, 'wb') as f:
    if mode == RISING:
      f.write('rising')
    elif mode == FALLING:
      f.write('falling')
    elif mode == BOTH:
      f.write('both')
  return True

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

from config import GPIO_FILE_BASE, RISING, FALLING, BOTH, GPIO
import bbio, select, threading, os, time


INTERRUPT_VALUE_FILES = {}

class EpollListener(threading.Thread):
  CREATION_DEBOUNCE_MS = 15
  def __init__(self):
    self.epoll = select.epoll()
    self.epoll_callbacks = {}
    self.first_interrupt_registered = False
    self.first_interrupt = True
    self.creation_time = time.time()
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
          if self.first_interrupt:
            self.first_interrupt = False
            elapsed = time.time()-self.creation_time
            if elapsed <= self.CREATION_DEBOUNCE_MS:
              # Ignore if interrupt fired within CREATION_DEBOUNCE_MS since
              # the creation of this EpollListener - on 3.8 kernels there is
              # always one false interrupt when first created, this avoids 
              # that
              continue
          self.epoll_callbacks[fileno]()
        
  def register(self, gpio_pin, callback):
    """ Register an epoll trigger for the specified fileno, and store
        the callback for that trigger. """
    fileno = INTERRUPT_VALUE_FILES[gpio_pin].fileno()
    self.epoll.register(fileno, select.EPOLLIN | select.EPOLLET)
    self.epoll_callbacks[fileno] = callback
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
  gpio_num = GPIO[gpio_pin]['gpio_num']
  INTERRUPT_VALUE_FILES[gpio_pin] = open(
    os.path.join(GPIO_FILE_BASE, 'gpio%i' % gpio_num, 'value'), 'r')
  _edge(gpio_pin, mode)
  EPOLL_LISTENER.register(gpio_pin, callback)

def detachInterrupt(gpio_pin):
  """ Detaches the interrupt from the given pin if set. """
  gpio_num = GPIO[gpio_pin]['gpio_num']
  EPOLL_LISTENER.unregister(gpio_pin)
  
def _edge(gpio_pin, mode):
  """ Sets an edge-triggered interrupt with sysfs /sys/class/gpio
      interface. Returns True if successful, False if unsuccessful. """
  gpio_num = GPIO[gpio_pin]['gpio_num']
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

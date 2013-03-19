# interrupt.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone GPIO interrupt driver
#
# The code in this file was written and contributed by 
# Alan Christopher Thomas - https://github.com/alanctkc
# Thanks!

from config import *
from gpio import *
import select, threading

INTERRUPT_VALUE_FILES = {}

class EpollListener(threading.Thread):
  def __init__(self):
    self.epoll = select.epoll()
    self.epoll_callbacks = {}
    super(EpollListener, self).__init__()

  def run(self):
    while True:
      events = self.epoll.poll()
      for fileno, event in events:
        for callback_fileno in self.epoll_callbacks:
          if fileno == callback_fileno:
            self.epoll_callbacks[fileno]()

  def register(self, gpio_pin, callback):
    """ Register an epoll trigger for the specified fileno, and store
        the callback for that trigger. """
    fileno = INTERRUPT_VALUE_FILES[gpio_pin].fileno()
    self.epoll.register(fileno, select.EPOLLIN | select.EPOLLET)
    self.epoll_callbacks[fileno] = callback

EPOLL_LISTENER = EpollListener()
EPOLL_LISTENER.daemon = True

def attachInterrupt(gpio_pin, callback, mode=BOTH):
  """ Sets an interrupt on the specified pin. 'mode' can be RISING, FALLING,
      or BOTH. 'callback' is the method called when an event is triggered. """
  # Start the listener thread
  if not EPOLL_LISTENER.is_alive():
    EPOLL_LISTENER.start()
  gpio_num = int(gpio_pin[4])*32 + int(gpio_pin[6:])
  INTERRUPT_VALUE_FILES[gpio_pin] = open(
    os.path.join(GPIO_FILE_BASE, 'gpio%i' % gpio_num, 'value'), 'r')
  _edge(gpio_pin, mode)
  EPOLL_LISTENER.register(gpio_pin, callback)

def _edge(gpio_pin, mode):
  """ Sets an edge-triggered interrupt with sysfs /sys/class/gpio
      interface. Returns True if successful, False if unsuccessful. """
  gpio_num = int(gpio_pin[4])*32 + int(gpio_pin[6:])
  if (not os.path.exists(GPIO_FILE_BASE + 'gpio%i' % gpio_num)): 
    # Pin not under userspace control
    return False
  edge_file = os.path.join(GPIO_FILE_BASE, 'gpio%i' % gpio_num, 'edge')
  with open(edge_file, 'wb') as f:
    if mode == RISING:
      f.write('rising')
    elif mode == FALLING:
      f.write('falling')
    elif mode == BOTH:
      f.write('both')
  return True

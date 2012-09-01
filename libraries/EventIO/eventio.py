"""
 EventIO - v0.1
 Copyright 2012 - Alexander Hiam <ahiam@marlboro.edu>
 Apache 2.0 license

 Basic multi-process event-driven programming for PyBBIO.
"""

from bbio import *
from SafeProcess import *
import time
from collections import deque
from multiprocessing import Process

# Return value of an event function to put it back into the event loop:
EVENT_CONTINUE = True

class EventLoop(SafeProcess):

  def config(self):
    # deque is better optimized for applications like FIFO queues than 
    # lists are:
    self.events = deque()

  def add_event(self, event):
    """ Adds given Event instance to the queue. """
    self.events.append(event)

  def run(self):
    """ Starts the event loop. Once started, no new events can be added. """
    try:
      while(True):
        event = self.events.popleft()
        if (event.run() == EVENT_CONTINUE):
          self.events.append(event)
        delay(0.1)
    except IndexError:
      # Queue is empty; end loop.
      pass


# This is the most basic event class. Takes two functions; when 'trigger'
# returns True 'event' is called. If 'event' returns EVENT_CONTINUE the event
# is put back in the event loop. Otherwise it will only be triggered once.
class Event(object):
  def __init__(self, trigger, event):
    # The trigger function must return something that will evaluate to True
    # to trigger the event function.
    self.trigger = trigger
    self.event = event

  def run(self):
    if self.trigger():
      # The event loop needs the return value of the event function so it can 
      # signal whether or not to re-add it:
      return self.event()
    # Otherwise re-add it to keep checking the trigger:
    return EVENT_CONTINUE


# This is the same as the basic Event class with the addition of debouncing;
# if an event is triggered and re-added to an event loop, the trigger will be 
# ignored for the given number of milliseconds.
class DebouncedEvent(object):
  def __init__(self, trigger, event, debounce_ms):
    self.trigger = trigger
    self.event = event
    self.debounce_ms = debounce_ms
    self.debouncing = False
    self.last_trigger = 0
  
  def run(self):
    if (self.debouncing):
      if (time.time()*1000-self.last_trigger <= self.debounce_ms):
        return EVENT_CONTINUE
      self.debouncing = False
    if self.trigger():
      self.last_trigger = time.time()*1000
      self.debouncing = True
      return self.event()
    return EVENT_CONTINUE


# This event will be triggered after the given number of milliseconds has
# elapsed. If the event function returns EVENT_CONTINUE the timer will 
# restart.
class TimedEvent(Event):
  def __init__(self, event, event_time_ms):
    self.event = event
    self.event_time_ms = event_time_ms
    self.start_time = millis()

  def trigger(self):
    if (millis() - self.start_time >= self.event_time_ms):
      self.start_time = millis()
      return True
    return False


# This event is based on the debounced event and compares the state of a given
# digital pin to the trigger state and calls the event function if they're the 
# same. Sets the pin to an input when created.
class DigitalTrigger(DebouncedEvent):
  def __init__(self, digital_pin, trigger_state, event, debounce_ms):
    pinMode(digital_pin, INPUT)
    trigger = lambda: digitalRead(digital_pin) == trigger_state
    super(DigitalTrigger, self).__init__(trigger, event, debounce_ms)


# This Event compares the value on the given analog pin to the trigger level
# and calls the event function if direction=1 and the value is above, or if 
# direction=-1 and the value is below. Either looks at a single reading or a 
# running average of size n_points.
class AnalogLevel(Event):
  def __init__(self, analog_pin, threshold, event, direction=1, n_points=4):
    self.analog_pin = analog_pin
    self.threshold = threshold
    self.event = event
    if (n_points < 1): n_points = 1
    # Construct the window regardless of n_points; will only be used if
    # n_points > 1:
    window = [0 if direction > 0 else 2**12 for i in range(n_points)]
    self.window = deque(window)
    self.direction = direction
    self.n_points = n_points

  def trigger(self): 
    if (self.n_points > 1):
      self.window.popleft()
      self.window.append(analogRead(self.analog_pin))
      val = sum(self.window)/self.n_points
    else: 
      val = analogRead(self.analog_pin)
    if (self.direction > 0): 
      return True if val > self.threshold else False
    return True if val < self.threshold else False

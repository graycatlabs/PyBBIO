"""
 SafeProcess - v0.1
 Copyright 2012 - Alexander Hiam <ahiam@marlboro.edu>
 Apache 2.0 license

 Provides a wrapper for Python's mutliprocessing.Process class
 which will be terminated during PyBBIO's cleanup.
"""

from multiprocessing import Process 
from bbio import *


class SafeProcess(Process):
  def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):

    # This is the magic line: 
    addToCleanup(lambda: self.terminate())
    # This way the process will be terminated as part of PyBBIO's 
    # cleanup routine.

    self.config()
    Process.__init__(self, group=group, target=target, name=name, 
                     args=args, kwargs=kwargs)

  def config(self):
    """ This function may be overriden by an inheriting class to handle any
        initialization that does not require any arguments be passed in. """
    pass

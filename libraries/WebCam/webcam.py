#!/usr/bin/env python

import gst,sys
 
 
class WebCam(object):
  def __init__(self,width,height,host="127.0.0.1",port=5000):
    self.width = str(width)
    self.height = str(height)
    self.host = str(host)
    self.port = int(port)
    self.source = gst.element_factory_make("v4l2src", "source")
    self.caps = gst.Caps("image/jpeg,width=640,height=480,framerate=30/1")
    self.capsfilter = gst.element_factory_make("capsfilter", "filter")
    self.jdecoder = gst.element_factory_make("jpegdec", "jdecoder")
    self.theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
    self.video_queue = gst.element_factory_make("queue", "video_queue")
    self.muxogg= gst.element_factory_make("oggmux", "muxogg")
    self.sink = gst.element_factory_make("tcpserversink", "sink")
 
 
  def startStreaming(self):
    # Create the empty pipeline
    pipeline = gst.Pipeline("test-pipeline")
 
    if not self.source or not self.capsfilter or not self.jdecoder or not self.theoraenc or not self.video_queue or not self.muxogg or not self.sink or not pipeline:
      print >> sys.stderr, "Not all elements could be created."
      exit(-1)
     
    # Build the pipeline
    pipeline.add(self.source, self.capsfilter, self.jdecoder, self.theoraenc, self.video_queue, self.muxogg, self.sink)
    if not gst.element_link_many(self.source, self.capsfilter,  self.jdecoder, self.theoraenc, self.video_queue, self.muxogg, self.sink):
      print >> sys.stderr, "Elements could not be linked."
      exit(-1)
     
    self.source.set_property("device","/dev/video0")
    self.capsfilter.set_property("caps", self. caps)
    self.sink.set_property("host",self.host)
    self.sink.set_property("port",self.port)

    ret = pipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      print >> sys.stderr, "Unable to set the pipeline to the playing state."
      exit(-1)

      

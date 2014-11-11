from bbio import *
import gst,sys, gobject, pygtk, gst.video

class WebCam(object):

  def __init__(self,video_device=0):
    '''
    WebCam(video_device_num)
    Initialises the WebCam object. 
    video_device_num corresponds to the /dev/video number 
    This switches on your camera until stopPipeline() is called.
    '''
    self.video_num = video_device
    self.video_dev = "/dev/video%i"%(video_device)
    self.pipeline = gst.Pipeline()
    self.srcbin = self._sourcebin()
    self.videocbin = self._videoconvertbin()
    
    self.fakesink = gst.element_factory_make("fakesink")
    self.fakestreamsink = gst.element_factory_make("fakesink")
    self.streamsink = gst.element_factory_make("tcpserversink")
    self.bufferqueue = gst.element_factory_make("queue")
    
    self.pic_tee = gst.element_factory_make("tee")
    self.pic_queue = gst.element_factory_make("queue")
    self.video_queue = gst.element_factory_make("queue")
    
    self.streaming = 0
    
    if not (self.srcbin and self.videocbin and self.pic_tee and self.pic_queue\
             and self.video_queue and self.fakesink and self.fakestreamsink and \
             self.pipeline and self.bufferqueue):
      raise Exception ("Elements could not be created")
      
    self.pipeline.add(self.srcbin,self.videocbin,self.pic_tee,self.pic_queue,\
                 self.video_queue,self.fakesink,self.fakestreamsink, \
                 self.bufferqueue)
    if (not gst.element_link_many(self.srcbin,self.pic_tee) or \
        not gst.element_link_many(self.pic_queue,self.fakesink) or \
        not gst.element_link_many(self.video_queue,self.videocbin,self.bufferqueue,\
                                  self.fakestreamsink)):
      raise Exception("Elements could not be linked")
      
    self.tee_pic_pad = self.pic_tee.get_request_pad("src%d")
    self.tee_video_pad = self.pic_tee.get_request_pad("src%d")
    self.queue_pic_pad = self.pic_queue.get_static_pad("sink")
    self.queue_video_pad = self.video_queue.get_static_pad("sink")
    
    if (self.tee_pic_pad.link(self.queue_pic_pad) != gst.PAD_LINK_OK or
        self.tee_video_pad.link(self.queue_video_pad) != gst.PAD_LINK_OK):
      raise Exception ("Tee and queues could not be linked")
    
    self.src_stream_pad = self.bufferqueue.get_pad("src")
    self.sink_stream_pad = self.bufferqueue.get_pad("sink")
    self.fake_stream_pad = self.fakestreamsink.get_pad("sink")
    self.stream_sink_pad = self.streamsink.get_pad("sink")
    
    if not (self.src_stream_pad and self.fake_stream_pad and self.stream_sink_pad):
      raise Exception("Pads could not be created") 
      
    ret = self.pipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      raise Exception("Unable to set the pipeline to the playing state.")
    
    self.streamsink.set_state(gst.STATE_NULL)
    addToCleanup(self.stopPipeline)

  def _sourcebin(self):
    bin = gst.Bin("srcbin")
    source = gst.element_factory_make("v4l2src")
    caps = gst.Caps("image/jpeg,width=640,height=480,framerate=30/1")
    capsfilter = gst.element_factory_make("capsfilter")
    jdecoder = gst.element_factory_make("jpegdec")
    source.set_property("device",self.video_dev)
    bin.add(source,capsfilter,jdecoder)
    gst.element_link_many(source,capsfilter,jdecoder)
    # ghostpad 
    pad = jdecoder.get_static_pad("src")
    ghost_pad = gst.GhostPad("src", pad)
    ghost_pad.set_active(True)
    bin.add_pad(ghost_pad)
    return bin
    
  def _videoconvertbin(self):
    bin = gst.Bin("vconvertbin")
    theoraenc = gst.element_factory_make("theoraenc")
    buffer_queue = gst.element_factory_make("queue")
    muxogg= gst.element_factory_make("oggmux")
    bin.add(theoraenc,buffer_queue,muxogg)
    gst.element_link_many(theoraenc,buffer_queue,muxogg)
    
    srcpad = muxogg.get_static_pad("src")
    src_ghost_pad = gst.GhostPad("src", srcpad)
    src_ghost_pad.set_active(True)
    bin.add_pad(src_ghost_pad)
    
    sinkpad = theoraenc.get_static_pad("sink")
    sink_ghost_pad = gst.GhostPad("sink", sinkpad)
    sink_ghost_pad.set_active(True)
    bin.add_pad(sink_ghost_pad)
    return bin
    
  def takeSnapshot(self,filename):
    '''
    takeSnapshot(filename)
    takes a snap shot and stores it in filename.jpeg
    '''
    filename = str(filename)+".jpeg"
    caps=gst.Caps('image/jpeg')
    self.fakesink.set_state(gst.STATE_PAUSED)
    buffer = self.fakesink.get_property ('last-buffer')
    while buffer == None:
      # Make sure gstreamer has finished creating the pipeline
      buffer = self.fakesink.get_property('last-buffer')
    buf = gst.video.video_convert_frame(buffer,"image/jpeg,width=640,height=480",5 * gst.SECOND)

    with file(filename, 'w') as fh:
      fh.write(str(buf))
    self.fakesink.set_state(gst.STATE_PLAYING)
    
    
  def startStreaming(self,port = 5000):
    '''
    startStreaming((optional)port)
    starts streaming video from the webcam to http://your_bbb's_ip_address:port
    port defaults to 5000
    NOTE : Once port no. is set trying to change it will show an error.
    '''
    self.streamsink.set_property("host","127.0.0.1")
    self.streamsink.set_property("port",int(port))
    self.streamsink.set_state(gst.STATE_PLAYING)
    if self.streaming == 0:
      self.pipeline.add(self.streamsink)
      self.streaming = 1
    self.sink_stream_pad.set_blocked(True)
    self.fakestreamsink.set_state(gst.STATE_NULL)
    self.src_stream_pad.unlink(self.fake_stream_pad)
    self.src_stream_pad.link(self.stream_sink_pad)
    self.sink_stream_pad.set_blocked(False)    
   
  def stopStreaming(self):
    '''
    stopStreaming()
    stops the streaming
    '''
    self.fakestreamsink.set_state(gst.STATE_PLAYING)
    self.sink_stream_pad.set_blocked(True)
    self.streamsink.set_state(gst.STATE_NULL)
    self.src_stream_pad.unlink(self.stream_sink_pad)
    self.src_stream_pad.link(self.fake_stream_pad)
    self.sink_stream_pad.set_blocked(False)
    
    
  def stopPipeline(self):
    '''
    stopPipeline()
    Switches off your camera.
    Can't use the same instance to switch ot back on
    '''
    self.pipeline.set_state(gst.STATE_NULL)
    self.streamsink.set_state(gst.STATE_NULL)
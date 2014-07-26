import gst,sys,cv
from bbio import delay, addToCleanup 
class WebCam(object):

  def __init__(self,video_device=0):
    self.video_num = video_device
    self.video_device = "/dev/video%i"%(video_device)
    self.pipeline = gst.Pipeline()
    delay(1000)
    self.pipeline.set_state(gst.STATE_NULL)
    
    #Create elements
    self.source = gst.element_factory_make("v4l2src")
    self.pic_tee = gst.element_factory_make("tee")

    
    #Video elements
    self.video_queue = gst.element_factory_make("queue")
    self.vcaps = gst.Caps("image/jpeg,width=640,height=480,framerate=30/1")
    self.vcapsfilter = gst.element_factory_make("capsfilter")
    self.vjdecoder = gst.element_factory_make("jpegdec")
    self.vtheoraenc = gst.element_factory_make("theoraenc")
    self.vbuffer_queue = gst.element_factory_make("queue")
    self.vmuxogg = gst.element_factory_make("oggmux")
    self.video_tee = gst.element_factory_make("tee")
    
    #Snapshot/Pic elements
    self.pic_queue = gst.element_factory_make("queue")
    self.pffmpeg = gst.element_factory_make("ffmpegcolorspace")
    self.ppngenc = gst.element_factory_make("pngenc")
    self.picsink = gst.element_factory_make("filesink")
    
    #streaming elements
    self.stream_queue = gst.element_factory_make("queue")
    self.stcpsink = gst.element_factory_make("tcpserversink")
    
    #recording elements
    self.record_queue = gst.element_factory_make("queue")
    self.record_sink = gst.element_factory_make("filesink")
    
    if not (self.pipeline and self.source and self.pic_tee and self.video_queue\
            and self.vcaps and self.vcapsfilter and self.vjdecoder and \
            self.vtheoraenc and self.vbuffer_queue and self.vmuxogg and \
            self.pic_queue and self.pffmpeg and self.ppngenc and self.picsink and\
            self.stream_queue and self.stcpsink and self.record_queue and \
            self.record_sink and self.video_tee):
      raise Exception('Not all elements could be created.')
      
    #Partially build pipeline
    self.pipeline.add (self.source, self.pic_tee, self.video_queue, self.vcaps,\
                       self.vcapsfilter, self.vjdecoder, self.vtheoraenc, \
                       self.vbuffer_queue, self.vmuxogg, self.pic_queue, \
                       self.pffmpeg, self.ppngenc, self.picsink, \
                       self.stream_queue, self.stcpsink, self.record_queue, \
                       self.record_sink, self.video_tee)
    if (not gst.element_link_many(self.source, self.pic_tee) or\
        not gst.element_link_many(self.video_queue, self.vcapsfilter, \
        self.vjdecoder, self.vtheoraenc, self.vbuffer_queue, self.vmuxogg, \
        self.video_tee) or\
        not gst.element_link_many(self.pic_queue, self.pffmpeg, self.ppngenc, \
        self.picsink) or\
        not gst.element_link_many(self.stream_queue, self.stcpsink) or\
        not gst.element_link_many(self.record_queue, self.record_sink)):
      raise Exception("Elements could not be linked")
      
    self.source.set_property("device",self.video_device)
    self.vcapsfilter.set_property("caps", self.vcaps)
    
    #Making the pads for the pic/video portion
    self.tee_pic_pad = self.pic_tee.get_request_pad("src%d")
    self.tee_video_pad = self.pic_tee.get_request_pad("src%d")
    self.queue_pic_pad = self.pic_queue.get_static_pad("sink")
    self.queue_video_pad = self.video_queue.get_static_pad("sink")
    
    #Making the pads for the streaming/recording portion
    self.tee_stream_pad = self.video_tee.get_request_pad("src%d")
    self.tee_record_pad = self.video_tee.get_request_pad("src%d")
    self.queue_stream_pad = self.stream_queue.get_static_pad("sink")
    self.queue_record_pad = self.record_queue.get_static_pad("sink")
    
    addTocleanup(self.stopPipeline)
    
  def startStreaming(self,port = 5000):
    self.pipeline.set_state(gst.STATE_NULL)
    self.stcpsink.set_property("host","127.0.0.1")
    self.stcpsink.set_property("port",int(port))
    if (self.tee_stream_pad.link(self.queue_stream_pad) != gst.PAD_LINK_OK and\
        self.tee_video_pad.link(self.queue_video_pad) != gst.PAD_LINK_OK):
      raise Exception("Pads could not be linked")
      
    ret = self.pipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      raise Exception('Unable to set the pipeline to the playing state.')
    else:
      return True
      
  def startRecording(self,filename):
    filename = str(filename)
    self.pipeline.set_state(gst.STATE_NULL)
    self.record_sink.set_property("location",filename+".ogg")
    if (self.tee_record_pad.link(self.queue_record_pad) != gst.PAD_LINK_OK and\
        self.tee_video_pad.link(self.queue_video_pad) != gst.PAD_LINK_OK):
      raise Exception("Pads could not be linked")
      
    ret = self.pipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      raise Exception('Unable to set the pipeline to the playing state.')
    else:
      return True
      
  def takeSnapshot(self,filename):
    filename = str(filename)
    self.pipeline.set_state(gst.STATE_NULL)
    self.record_sink.set_property("location",filename+".png")
    if ( self.tee_pic_pad.link(self.queue_pic_pad) != gst.PAD_LINK_OK ):
      raise Exception("Pads could not be linked")
      
    ret = self.pipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      raise Exception('Unable to set the pipeline to the playing state.')
    else:
      return True
      
  def stopPipeline(self):
    self.spipeline.set_state(gst.STATE_NULL)

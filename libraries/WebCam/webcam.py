import gst,sys,cv
 
class WebCam(object):

  def __init__(self):
    self.pipeline = gst.Pipeline("test-pipeline")
    pass

  def startStreaming(self):
    # Create the elements
    source = gst.element_factory_make("v4l2src", "source")
    caps = gst.Caps("image/jpeg,width=640,height=480,framerate=30/1")
    capsfilter = gst.element_factory_make("capsfilter", "filter")
    jdecoder = gst.element_factory_make("jpegdec", "jdecoder")
    theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
    video_queue = gst.element_factory_make("queue", "video_queue")
    muxogg= gst.element_factory_make("oggmux", "muxogg")
    sink = gst.element_factory_make("tcpserversink", "sink")

 
    # Create the empty pipeline
    self.pipeline = gst.Pipeline("test-pipeline")
 
    if not source or not capsfilter or not jdecoder or not theoraenc or not video_queue or not muxogg or not sink or not self.pipeline:
      print >> sys.stderr, "Not all elements could be created."
      exit(-1)
     
    # Build the pipeline
    self.pipeline.add(source, capsfilter, jdecoder, theoraenc, video_queue, muxogg, sink)
    if not gst.element_link_many(source, capsfilter,  jdecoder, theoraenc, video_queue, muxogg, sink):
      print >> sys.stderr, "Elements could not be linked."
      exit(-1)
     
    source.set_property("device","/dev/video0")
    capsfilter.set_property("caps", caps)
    sink.set_property("host","127.0.0.1")
    sink.set_property("port",5000)

    ret = self.pipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      print >> sys.stderr, "Unable to set the pipeline to the playing state."
      exit(-1)

    # Wait until error or EOS
    bus = self.pipeline.get_bus()

    # Parse message
    while True:
      message = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE, gst.MESSAGE_STATE_CHANGED | gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
      if message.type == gst.MESSAGE_ERROR:
         err, debug = message.parse_error()
         print >> sys.stderr, "Error received from element %s: %s"% (message.src.get_name(), err)
         print >> sys.stderr, "Debugging information: %s"% debug
         break
      elif message.type == gst.MESSAGE_EOS:
         print "End-Of-Stream reached."
         break
      elif message.type == gst.MESSAGE_STATE_CHANGED:
         if isinstance(message.src, gst.Pipeline):
             old_state, new_state, pending_state = message.parse_state_changed()
             print ("Pipeline state changed from %s to %s."% 
                    (gst.element_state_get_name(old_state), gst.element_state_get_name (new_state)))
      else:
         print >> sys.stderr, "Unexpected message received."

    self.pipeline.set_state(gst.STATE_NULL)
    
  
    
  def stopPipeline(self):
    self.pipeline.set_state(gst.STATE_STOPPING)
    
  def capturePic(self,filename)
    filename = str(filename)
    capture = cv.CaptureFromCAM(-1) #-1 will select the first camera available, usually /dev/video0 on linux
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
    im = cv.QueryFrame(capture)
    cv.SaveImage(filename+".jpg")
    
  def startRecording(self,filename):
    filename = str(filename)
     # Create the elements
    source = gst.element_factory_make("v4l2src", "source")
    caps = gst.Caps("image/jpeg,width=640,height=480,framerate=30/1")
    capsfilter = gst.element_factory_make("capsfilter", "filter")
    jdecoder = gst.element_factory_make("jpegdec", "jdecoder")
    theoraenc = gst.element_factory_make("theoraenc", "theoraenc")
    video_queue = gst.element_factory_make("queue", "video_queue")
    muxogg= gst.element_factory_make("oggmux", "muxogg")
    sink = gst.element_factory_make("filesink", "sink")

 
    # Create the empty pipeline
    self.pipeline = gst.Pipeline("test-pipeline")
 
    if not source or not capsfilter or not jdecoder or not theoraenc or not video_queue or not muxogg or not sink or not self.pipeline:
      print >> sys.stderr, "Not all elements could be created."
      exit(-1)
     
    # Build the pipeline
    self.pipeline.add(source, capsfilter, jdecoder, theoraenc, video_queue, muxogg, sink)
    if not gst.element_link_many(source, capsfilter,  jdecoder, theoraenc, video_queue, muxogg, sink):
      print >> sys.stderr, "Elements could not be linked."
      exit(-1)
     
    source.set_property("device","/dev/video0")
    capsfilter.set_property("caps", caps)
    sink.set_property("location",filename+".ogg")

    ret = self.pipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      print >> sys.stderr, "Unable to set the pipeline to the playing state."
      exit(-1)

    # Wait until error or EOS
    bus = self.pipeline.get_bus()

    # Parse message
    while True:
      message = bus.timed_pop_filtered(gst.CLOCK_TIME_NONE, gst.MESSAGE_STATE_CHANGED | gst.MESSAGE_ERROR | gst.MESSAGE_EOS)
      if message.type == gst.MESSAGE_ERROR:
         err, debug = message.parse_error()
         print >> sys.stderr, "Error received from element %s: %s"% (message.src.get_name(), err)
         print >> sys.stderr, "Debugging information: %s"% debug
         break
      elif message.type == gst.MESSAGE_EOS:
         print "End-Of-Stream reached."
         break
      elif message.type == gst.MESSAGE_STATE_CHANGED:
         if isinstance(message.src, gst.Pipeline):
             old_state, new_state, pending_state = message.parse_state_changed()
             print ("Pipeline state changed from %s to %s."% 
                    (gst.element_state_get_name(old_state), gst.element_state_get_name (new_state)))
      else:
         print >> sys.stderr, "Unexpected message received."

    self.pipeline.set_state(gst.STATE_NULL)   
    
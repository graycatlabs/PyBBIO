import gst,sys,cv
 
class WebCam(object):

  def __init__(self):
    self.spipeline = gst.Pipeline("test-pipeline")
    self.rpipeline = gst.Pipeline("test-pipeline")

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

 
 
    if not source or not capsfilter or not jdecoder or not theoraenc or not video_queue or not muxogg or not sink or not self.spipeline:
      print >> sys.stderr, "Not all elements could be created."
      exit(-1)
     
    # Build the pipeline
    self.spipeline.add(source, capsfilter, jdecoder, theoraenc, video_queue, muxogg, sink)
    if not gst.element_link_many(source, capsfilter,  jdecoder, theoraenc, video_queue, muxogg, sink):
      print >> sys.stderr, "Elements could not be linked."
      exit(-1)
     
    source.set_property("device","/dev/video0")
    capsfilter.set_property("caps", caps)
    sink.set_property("host","127.0.0.1")
    sink.set_property("port",5000)

    ret = self.spipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      print >> sys.stderr, "Unable to set the pipeline to the playing state."
      exit(-1)
    else:
      return True

  
  def stopStreaming(self):
    self.spipeline.set_state(gst.STATE_NULL)
    
  def stopRecording(self):
    self.rpipeline.set_state(gst.STATE_NULL)
    
  def captureSnapshot(self,filename):
    filename = str(filename)
    capture = cv.CaptureFromCAM(-1) #-1 will select the first camera available, usually /dev/video0 on linux
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320)
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
    im = cv.QueryFrame(capture)
    cv.SaveImage(filename+".jpg",im)
    
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

    if not source or not capsfilter or not jdecoder or not theoraenc or not video_queue or not muxogg or not sink or not self.rpipeline:
      print >> sys.stderr, "Not all elements could be created."
      exit(-1)
     
    # Build the pipeline
    self.rpipeline.add(source, capsfilter, jdecoder, theoraenc, video_queue, muxogg, sink)
    if not gst.element_link_many(source, capsfilter,  jdecoder, theoraenc, video_queue, muxogg, sink):
      print >> sys.stderr, "Elements could not be linked."
      exit(-1)
     
    source.set_property("device","/dev/video0")
    capsfilter.set_property("caps", caps)
    sink.set_property("location",filename+".ogg")

    ret = self.rpipeline.set_state(gst.STATE_PLAYING)
    if ret ==  gst.STATE_CHANGE_FAILURE:
      print >> sys.stderr, "Unable to set the pipeline to the playing state."
      exit(-1)
    else:
      return True
    
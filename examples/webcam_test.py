from bbio import *
from WebCam import *

cam = WebCam()
cam.startStreaming()
cam.startRecording("sample")
delay(30000)
cam.stopStreaming()
cam.stopRecording()
cam.captureSnapshot("sam")

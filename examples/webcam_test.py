from bbio import *
from WebCam import WebCam

cam = WebCam()

cam.startStreaming()
cam.startRecording("sample1")
cam.takeSnapshot("sam1")
delay(30000)
cam.stopStreaming()
cam.stopRecording()
cam.takeSnapshot("sam2")
delay(10000)
cam.startStreaming()
cam.startRecording("sample2")
delay(30000)
cam.stopStreaming()
cam.stopRecording()
cam.takeSnapshot("sam3")

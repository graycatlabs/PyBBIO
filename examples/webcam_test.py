'''
 webcam_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the WebCam library
 for PyBBIO.

 This example program is in the public domain.
'''

from bbio import *
from WebCam import WebCam

cam = WebCam()


cam.startStreaming(5001)
cam.takeSnapshot("sam1")
delay(30000)
cam.stopStreaming()
delay(30000)
cam.startStreaming(5001)
cam.takeSnapshot("../sam2")
cam.stopStreaming()

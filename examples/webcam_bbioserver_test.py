'''
 webcam_bbioserver_test.py 
 Rekha Seethamraju

 An example to demonstrate the use of the WebCam and BBIOServer libraries for PyBBIO.

 This example program is in the public domain.
'''
from bbio import *
from bbio.libraries.WebCam import WebCam

from BBIOServer import *

cam = WebCam()
delay(10000)
server = BBIOServer()
cam.startStreaming()

vid = Page("Webcam Video")
vid.add_video("192.168.7.2","5000")
server.start(vid)

cam.stopStreaming()

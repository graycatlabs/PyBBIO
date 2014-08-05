from bbio import *
from WebCam import WebCam

from BBIOServer import *

cam = WebCam()
server = BBIOServer()

vid = Page("Webcam Video")
vid.add_video("192.168.2.95","5000")
server.start(vid)

cam.startStreaming()

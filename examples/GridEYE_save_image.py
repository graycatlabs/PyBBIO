"""
 GridEYE_test.py 
 Alexander Hiam <alex@graycat.io>
 
 Example program for PyBBIO's GridEYE library. Reads the current
 thermal sensor data and saves to thermal-image.png in the current
 directory.

 Requires the Python Imaging Library:
  # pip install PIL

 This example program is in the public domain.
"""

from bbio import *
from bbio.libraries.GridEYE import GridEYE
from PIL import Image
import colorsys

# Width and height of final image, 8x8 thermal image scaled to this size:
WIDTH = 600
HEIGHT = 600

I2C1.open()
grideye = GridEYE(I2C1)
# Enable the GridEYE's built-in moving average:
grideye.enableAveraging()


def generateImage(frame):
  min_temp = min(frame)
  max_temp = max(frame)
  
  for i in range(64):
    # Map temperature value to ratio of min and max temp:
    frame[i] -= min_temp
    frame[i] /= (max_temp - min_temp)

    # Convert ratio to (R, G, B):
    frame[i] = colorsys.hsv_to_rgb(1-frame[i], 1, 1)
    frame[i] = tuple(map(lambda x: int(255*x), frame[i]))

  image = Image.new("RGB", (8, 8))
  image.putdata(frame)
  image = image.resize((WIDTH,HEIGHT), Image.BILINEAR)
  image.save("thermal-image.png")

def setup():
  pass

def loop():
  frame = grideye.getFrame()
  generateImage(frame)
  stop()


run(setup, loop)

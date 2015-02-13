"""
 generate_overlays.py
 Part of PyBBIO
 github.com/alexanderhiam/PyBBIO
 MIT license

 Generates and installs device tree overlays used for pinmuxing on 
 BeagleBones running a 3.8 or newer kernel.
"""

import sys, os, glob, shutil

cwd = os.path.dirname(os.path.realpath(__file__))

config_path = os.path.realpath('%s/../bbio/platform/beaglebone' % cwd)
dts_path = '%s/overlays' % cwd
dtbo_path = '%s/overlays/compiled' % cwd
dtc_compile = ' dtc -O dtb -o %s.dtbo -b 0 -@ %s.dts'


sys.path = [config_path] + sys.path
from config import GPIO, ADC

with open('%s/overlays/gpio-template.txt' % cwd, 'rb') as f:
  gpio_template = f.read()

with open('%s/overlays/adc-template.txt' % cwd, 'rb') as f:
  adc_template = f.read()


header = \
"""
/* This file was generated as part of PyBBIO
 * github.com/alexanderhiam/PyBBIO
 * 
 * This file is in the Public Domain.
 */

"""

def compileOverlays():
  print "Compiling all overlays..."
  overlays = glob.glob('%s/*.dts' % dts_path)
  for overlay in overlays:
    name = os.path.splitext(os.path.basename(overlay))[0]
    os.system(dtc_compile % ('%s/%s' % (dtbo_path, name),
                             '%s/%s' % (dts_path, name)))

def generateOverlays():
  print "Generating GPIO overlays..."
  version = '00A0'
  for pin, config in GPIO.items():
    gpio_pin = pin.lower()
    register_name = config['signal']
    offset = str(config['offset'])
    overlay_name = 'PyBBIO-%s' % gpio_pin
    dts = gpio_template.replace('{gpio_pin}', gpio_pin)\
                       .replace('{name}', register_name)\
                       .replace('{overlay_name}', overlay_name)\
                       .replace('{version}', version)\
                       .replace('{offset}', offset)
    with open('%s/%s-%s.dts' % (dts_path, overlay_name, version), 'wb') as f:
      f.write(dts)
      
  print "Generating ADC overlays..."
  version = '00A0'
  adc_scale = '100'
  for adc_ch, config in ADC.items():
    overlay_name = 'PyBBIO-%s' % adc_ch
    header_pin = config[2]
    dts = adc_template.replace('{adc_ch}', adc_ch)\
                      .replace('{header_pin}', header_pin)\
                      .replace('{overlay_name}', overlay_name)\
                      .replace('{adc_scale}', adc_scale)\
                      .replace('{version}', version)
    with open('%s/%s-%s.dts' % (dts_path, overlay_name, version), 'wb') as f:
      f.write(dts)

      
if __name__ == '__main__':
  if not os.path.exists(dts_path):
    os.makedirs(dts_path)
  if not os.path.exists(dtbo_path):
    os.makedirs(dtbo_path)

  generateOverlays()
  compileOverlays()

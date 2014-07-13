"""
 install-overlays.py
 Part of PyBBIO
 github.com/alexanderhiam/PyBBIO
 MIT license

 Generates and installs device tree overlays used for pinmuxing on 
 BeagleBones running a 3.8 or newer kernel.
"""

import sys, os, glob, shutil

cwd = os.path.dirname(os.path.realpath(__file__))

config_path = os.path.realpath('%s/../bbio/platform/beaglebone' % cwd)
firmware_path = '/lib/firmware'
firmware_source_path = '%s/PyBBIO-src' % firmware_path
dtc_compile = ' dtc -O dtb -o %s.dtbo -b 0 -@ %s.dts'

overlays_to_copy = [
  '%s/overlays/PyBBIO-ADC-00A0.dts' % cwd,

  '%s/overlays/PyBBIO-epwmss0-00A0.dts' % cwd,
  '%s/overlays/PyBBIO-ecap0-00A0.dts' % cwd,

  '%s/overlays/PyBBIO-epwmss1-00A0.dts' % cwd,
  '%s/overlays/PyBBIO-ehrpwm1-00A0.dts' % cwd,
  '%s/overlays/PyBBIO-ecap1-00A0.dts' % cwd,

  '%s/overlays/PyBBIO-epwmss2-00A0.dts' % cwd,
  '%s/overlays/PyBBIO-ehrpwm2-00A0.dts' % cwd,

  '%s/overlays/PyBBIO-eqep0-00A0.dts' % cwd,
  '%s/overlays/PyBBIO-eqep1-00A0.dts' % cwd,
  '%s/overlays/PyBBIO-eqep2-00A0.dts' % cwd,
  '%s/overlays/PyBBIO-eqep2b-00A0.dts' % cwd,
]

sys.path = [config_path] + sys.path
from config_common import GPIO

sys.path = ["%s/bone_3_8" % config_path] + sys.path
from config import ADC

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

def copyOverlays():
  print "Copying and compiling static overlays...",
  for overlay in overlays_to_copy:
    if not os.path.exists(overlay):
      print "*Couldn't find static overlay %s!" % overlay
      continue
    shutil.copy2(overlay, firmware_source_path)
    name = os.path.splitext(os.path.basename(overlay))[0]
    os.system(dtc_compile % ('%s/%s' % (firmware_path, name),
                             '%s/%s' % (firmware_source_path, name)))

  print "Done!"

def generateOverlays():
  print "Generating and compiling GPIO overlays...",
  version = '00A0'
  for pin, config in GPIO.items():
    gpio_pin = pin.lower()
    register_name = config[0]
    offset = str(config[1])
    overlay_name = 'PyBBIO-%s' % gpio_pin
    dts = gpio_template.replace('{gpio_pin}', gpio_pin)\
                       .replace('{name}', register_name)\
                       .replace('{overlay_name}', overlay_name)\
                       .replace('{version}', version)\
                       .replace('{offset}', offset)
    with open('%s/%s-%s.dts' % (firmware_source_path, overlay_name, version), 'wb') as f:
      f.write(dts)
    os.system(dtc_compile % ('%s/%s-%s' % (firmware_path, overlay_name, version),
                             '%s/%s-%s' % (firmware_source_path, overlay_name, 
                                           version)))

  #print "Generating and compiling PWM overlays...",
  #version = '00A0'
  print "Done!"

  print "Generating and compiling ADC overlays...",
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
    with open('%s/%s-%s.dts' % (firmware_source_path, overlay_name, version), 'wb') as f:
      f.write(dts)
    os.system(dtc_compile % ('%s/%s-%s' % (firmware_path, overlay_name, version),
                             '%s/%s-%s' % (firmware_source_path, overlay_name, 
                                           version)))
                                           
  print "Done!"
      
if __name__ == '__main__':
  if not os.path.exists(firmware_source_path):
    print "PyBBIO device tree overlay directory not found, creating..."
    os.makedirs(firmware_source_path)
  else:
    print "Old PyBBIO device tree overlay directory found, overwriting..."

  generateOverlays()
  copyOverlays()

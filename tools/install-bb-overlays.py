"""
 install-overlays.py
 Part of PyBBIO
 github.com/alexanderhiam/PyBBIO
 Apache 2.0 license

 Generates and installs device tree overlays used for pinmuxing on 
 BeagleBones running a 3.8 or newer kernel.
"""

import sys, os, glob

cwd = os.path.dirname(os.path.realpath(__file__))

config_path = os.path.realpath('%s/../bbio/platform/beaglebone' % cwd)
firmware_path = '/lib/firmware'
firmware_source_path = '%s/PyBBIO-src' % firmware_path
dtc_compile = ' dtc -O dtb -o %s.dtbo -b 0 -@ %s.dts'

sys.path.append(config_path)

from config_common import GPIO

template = \
"""
/* 
 This file was generated as part of PyBBIO
 github.com/alexanderhiam/PyBBIO
 
 This file is in the Public Domain.
*/

/dts-v1/;
/plugin/;

/{
  compatible = "ti,beaglebone", "ti,beaglebone-black";

  part-number = "{overlay_name}";
  version = "{version}";

  /* state the resources this cape uses */
  exclusive-use =
    /* the pin header uses */

    /* the hardware IP uses */
    "{gpio_pin}";

  fragment@0 {
    target = <&am33xx_pinmux>;
    __overlay__ {

      pybbio_{gpio_pin}_rxactive_nopull: pinmux_pybbio_{gpio_pin}_rxactive_nopull {
        pinctrl-single,pins = <
          {offset} 0x2f  /* {name} - rx active | no pull | MODE7 ({gpio_pin}) */
        >;
      };
      pybbio_{gpio_pin}_rxactive_pullup: pinmux_pybbio_{gpio_pin}_rxactive_pullup {
        pinctrl-single,pins = <
          {offset} 0x37  /* {name} - rx active | pull up | MODE7 ({gpio_pin}) */
        >;
      };
      pybbio_{gpio_pin}_rxactive_pulldown: pinmux_pybbio_{gpio_pin}_rxactive_pulldown {
        pinctrl-single,pins = <
          {offset} 0x27  /* {name} - rx active | pull down | MODE7 ({gpio_pin}) */
        >;
      };
      
      pybbio_{gpio_pin}_nopull: pinmux_pybbio_{gpio_pin}_nopull {
        pinctrl-single,pins = <
          {offset} 0x0f  /* {name} - rx active | no pull | MODE7 ({gpio_pin}) */
        >;
      };
      pybbio_{gpio_pin}_pullup: pinmux_pybbio_{gpio_pin}_pullup {
        pinctrl-single,pins = <
          {offset} 0x17  /* {name} - rx active | pull up | MODE7 ({gpio_pin}) */
        >;
      };
      pybbio_{gpio_pin}_pulldown: pinmux_pybbio_{gpio_pin}_pulldown {
        pinctrl-single,pins = <
          {offset} 0x07  /* {name} - rx active | pull down | MODE7 ({gpio_pin}) */
        >;
      };
      
    };
  };

  fragment@1 {
    target = <&ocp>; /* On-Chip Peripherals */
    __overlay__ {
      {overlay_name} {
        compatible = "bone-pinmux-helper"; /* Use the pinmux helper */
        status="okay";
        /* Define custom names for indexes in pinctrl array: */ 
        pinctrl-names = "mode_0b00101111", "mode_0b00110111", "mode_0b00100111",
                        "mode_0b00001111", "mode_0b00010111", "mode_0b00000111";
        /* Set the elements of the pinctrl array to the pinmux overlays
           defined above: */
        pinctrl-0 = <&pybbio_{gpio_pin}_rxactive_nopull>; 
        pinctrl-1 = <&pybbio_{gpio_pin}_rxactive_pullup>; 
        pinctrl-2 = <&pybbio_{gpio_pin}_rxactive_pulldown>;
        pinctrl-3 = <&pybbio_{gpio_pin}_nopull>; 
        pinctrl-4 = <&pybbio_{gpio_pin}_pullup>; 
        pinctrl-5 = <&pybbio_{gpio_pin}_pulldown>;
      };
    };
  };
};
"""
  
def generateOverlays():
  if not os.path.exists(firmware_source_path):
    print "PyBBIO device tree overlay directory not found, creating..."
    os.makedirs(firmware_source_path)
  else:
    print "Old PyBBIO device tree overlay directory found, overwriting..."

  print "Generating and compiling overlays...",
  version = '00A0'
  for pin, config in GPIO.items():
    gpio_pin = pin.lower()
    register_name = config[2]
    offset = str(config[3])
    overlay_name = 'PyBBIO-%s' % gpio_pin
    dts = template.replace('{gpio_pin}', gpio_pin)\
                  .replace('{name}', register_name)\
                  .replace('{overlay_name}', overlay_name)\
                  .replace('{version}', version)\
                  .replace('{offset}', offset)
    with open('%s/%s-%s.dts' % (firmware_source_path, overlay_name, version), 'wb') as f:
      f.write(dts)
    os.system(dtc_compile % ('%s/%s-%s' % (firmware_path, overlay_name, version),
                             '%s/%s-%s' % (firmware_source_path, overlay_name, 
                                           version)))
  print "Done!"
      
if __name__ == '__main__': 
  generateOverlays()
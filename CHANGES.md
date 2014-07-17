###Changelog for PyBBIO  
http://github.com/alexanderhiam/PyBBIO   

#### version 0.9
  * Added SPI library with example for ADT7310 temp sensor
  * Added library for phant.io with example
  * Added eQEP library with example
  * Moved to C extensions for reading/writing Kernel driver files
  * Reorganized package structure and updated install process to support pip and apt-get distribution
  * Changed from Apache 2.0 license to MIT license
  * Fixed false interrupt firing on first attachInterrupt() call
  * Various minor bug fixes

#### version 0.8.5
 * Dropped mmap GPIO, use Kernel drivers
 * PWM fully working
 * I2C support
 * Fixed USR LEDs

#### version 0.8
 * Added tools/ directory for install helpers
 * Support for Kernel >= 3.8:
   * GPIO
   * Serial
   * ADC
   * Added tool to generate and compile DT overlays
 * misc. fixes

#### version 0.6
 * Moved to multi-file package structure
 * New structure and install method can now easily support platforms besides 
   the Beaglbone
 * Swithed to setuptools instead of distutils for setup.py
 * All memory access moved to C extension to increase speed
 * Created this changelog!

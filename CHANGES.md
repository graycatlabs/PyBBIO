###Changelog for PyBBIO  
http://github.com/graycatlabs/PyBBIO   

#### version 0.10
 * Added library and exampes for Panasonic Grid-EYE 8x8 thermal sensor array
 * Updated MAX31855 library to use SPI module instead of soft SPI
 * Switched to using separate [serbus](https://github.com/graycatlabs/serbus) package for SPI and I2C
 * Standardized [version numbering](https://github.com/graycatlabs/PyBBIO/wiki#version-numbering)

#### version 0.9.5.3
 * Added ADXL345 3-axis accelerometer library and example
 * Only allow I2C, SPI and UART initialization one time
 * Better error handling in interrupt routines

#### version 0.9.5.2
 * Fixed incorrect I2C bus initialization (which caused I2C2 not to work)
 * Updated to Contributor Covenant Code of Conduct 1.2.0
 * Added requests package to dependencies

#### version 0.9.5.1
 * Install examples to /usr/local/lib/PyBBIO/examples/
 * Implemented proper bus number detection for SPI and I2C

#### version 0.9.5
 * New libraries
   * BMP183 SPI pressure sensor
   * HTU21D I2C RH sensor
   * IoT
     * Phant
     * ThingSpeak
 * Added I2C1/I2C2 alternative names for Wire1/Wire2
 * Fixed a memory leak in the SPI and I2C C extensions

#### version 0.9.4
  * Created a new C SPI driver and C extension for it to replace the old 
    spimodule code. Should be a good performance improvement
  * Fixed a couple memory leaks in C extensions 
  * Fixed a missing type check in sysfs C extension. Was causing RotaryEncoder 
    library to fail
  * Fixed the tests/library_test.py example file

#### version 0.9.3
  * Moved all GPIO code to C extension
  * Added LiquidCrystal character LCD library
  * Improved sysfs interface for faster kernel driver file access 
  * Removed 3.2 support, use 0.9.2 if you're still running 3.2 for some reason...
  * Libraries are now contained within the bbio package. This changes importing a bit, user code will need updating
  * Simplifies setup.py
    * Examples are no longer copied
    * DT overlays are distributed compiled and copied with setuptool as data_files
  * BBIOServer now serves from ~/.BBIOServer instead of from inside the package
  * Started adding stubs for universion-io support, not yet implemented

#### version 0.9.2
  * Added WebCam library from rseetham
  * BBIOServer updates
    * Slider from Ikario
    * JQuery -> v1.11.1
  * I2C library improvement from ycoroneos

#### version 0.9.1
  * Added MMA7660 3-axis accelerometer library
  * Removed smbus from pip requirements since there's no smbus package in PyPI
  * Fixes a couple typos

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

### PyBBIO v0.8
http://github.com/alexanderhiam/PyBBIO  
Copyright (c) 2012, 2013 - Alexander Hiam - hiamalexander@gmail.com    

PyBBIO is a Python library for Arduino-style hardware IO support on the TI 
Beaglebone. It currently supports basic digital IO through digitalRead() 
and digitalWrite() functions, ADC support through analogRead(), PWM support 
analogWrite() as well as a few utility functions for changing PWM frequency
etc., and an Arduino-style UART interface. SPI and I2C are on the way, so 
keep checking the Github page for updates.  

### Documentation can be found at http://github.com/alexanderhiam/PyBBIO/wiki  

***PyBBIO is not yet fully working with the 3.8 kernel which comes with the BeagleBone
Black and newer Angstrom images. Currently only GPIO, ADC, serial are working.***

#License

    PyBBIO is licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

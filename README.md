### PyBBIO v0.6
http://github.com/alexanderhiam/PyBBIO  
Copyright (c) 2012, 2013 - Alexander Hiam - hiamalexander@gmail.com    

PyBBIO is a Python library for Arduino-style hardware IO support on the TI 
Beaglebone. It currently supports basic digital IO through digitalRead() 
and digitalWrite() functions, ADC support through analogRead(), PWM support 
analogWrite() as well as a few utility functions for changing PWM frequency
etc., and an Arduino-style UART interface. SPI and I2C are on the way, so 
keep checking the Github page for updates.  
#### Documentation at http://github.com/alexanderhiam/PyBBIO/wiki

***PyBBIO is not yet fully working with the 3.8 kernel which comes with the BeagleBone
Black and newer Angstrom images. Currently only GPIO and serial are working.***

#Installing

It is assumed that your Beaglebone is already set up and configured on your network, 
and that you have already SSHed onto it. 

Note that these instructions assume you want PyBBIO/ to live in your home 
directory. This is not a requirement and can be changed as desired. 

The first step is to install the dependencies: 

On Angstrom:

    # opkg update && opkg install curl gcc python-pyserial python-dev
    # curl http://python-distribute.org/distribute_setup.py | python

On Ubuntu:

    # apt-get update && apt-get install curl gcc python-serial python-dev
    # curl http://python-distribute.org/distribute_setup.py | python

Then you'll need to get the code:

    # cd ~
    # git clone git://github.com/alexanderhiam/PyBBIO.git

Now run the install script:

    # cd PyBBIO
    # python setup.py install

PyBBIO should now be installed correctly. Run the blink example to make sure 
all is well:

    # cd examples
    # python blink.py

And confirm that the LEDs next to the Ethernet jack labelled USR2 and USR3 
are blinking back and forth. 

#Updating
I am working as fast as I can to add support for many of the features that 
the Beablebone's AM3359 processor has to offer, so you'll want to make sure 
your version is up to date. Thanks to git this is a very simple process:

    # cd ~/PyBBIO
    # git pull
    # python setup.py install


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

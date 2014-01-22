# PyBBIO config file for BeagleBones with 3.8 kernels. 

#---------------------------------------------------#
# Changes to this file may lead to permanent damage #
# to you Beaglebone, edit with care.                #
#---------------------------------------------------#

# Load the common beaglebone configuration:
from config_common import *
import glob

########################################
##--- Start device tree: ---##

SLOTS_FILE = glob.glob('/sys/devices/bone_capemgr.*/slots')[0]
OCP_PATH = glob.glob('/sys/devices/ocp.*')[0]

##--- End device tree config ------##
########################################

##############################
##--- Start GPIO config: ---##
GPIO_FILE_BASE = '/sys/class/gpio/'
EXPORT_FILE = GPIO_FILE_BASE + 'export'
UNEXPORT_FILE = GPIO_FILE_BASE + 'unexport'


##--- End GPIO config ------## 
##############################


#############################
##--- Start ADC config: ---##

ADC_ENABLE_DTS_OVERLAY = 'PyBBIO-ADC'

# ADC pins should be in the form:
#          ['path/to/adc-file', 'Channel-enable-overlay', 'header_pin'] 

ADC = {
  'AIN0' : ['%s/PyBBIO-AIN0.*/AIN0' % OCP_PATH, 'PyBBIO-AIN0', 'P9.39'],
  'AIN1' : ['%s/PyBBIO-AIN1.*/AIN1' % OCP_PATH, 'PyBBIO-AIN1', 'P9.40'],
  'AIN2' : ['%s/PyBBIO-AIN2.*/AIN2' % OCP_PATH, 'PyBBIO-AIN2', 'P9.37'],
  'AIN3' : ['%s/PyBBIO-AIN3.*/AIN3' % OCP_PATH, 'PyBBIO-AIN3', 'P9.38'],
  'AIN4' : ['%s/PyBBIO-AIN4.*/AIN4' % OCP_PATH, 'PyBBIO-AIN4', 'P9.33'],
  'AIN5' : ['%s/PyBBIO-AIN5.*/AIN5' % OCP_PATH, 'PyBBIO-AIN5', 'P9.36'],
  'AIN6' : ['%s/PyBBIO-AIN6.*/AIN6' % OCP_PATH, 'PyBBIO-AIN6', 'P9.35'],
  'AIN7' : ['%s/PyBBIO-AIN7.*/AIN7' % OCP_PATH, 'PyBBIO-AIN7', 'vsys'],
}

# And some constants so the user doesn't need to use strings:

AIN0 = A0 = 'AIN0'
AIN1 = A1 = 'AIN1'
AIN2 = A2 = 'AIN2'
AIN3 = A3 = 'AIN3'
AIN4 = A4 = 'AIN4'
AIN5 = A5 = 'AIN5'
AIN6 = A6 = 'AIN6'
AIN7 = A7 = VSYS = 'AIN7'


##--- End ADC config ------##
#############################



##############################
##--- Start UART config: ---##

# UART ports must be in form: 
#    [port, uart-overlay-name]

UART = {
  'UART1' : ['/dev/ttyO1', 'BB-UART1'],
  'UART2' : ['/dev/ttyO2', 'BB-UART2'],
  'UART4' : ['/dev/ttyO4', 'BB-UART4'],
  'UART5' : ['/dev/ttyO5', 'BB-UART5']
}


##--- End UART config ------##
##############################


PWM_PINS = {}

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
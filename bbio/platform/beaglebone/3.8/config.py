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

PWM_PINS = {}
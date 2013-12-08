# PyBBIO config file for BeagleBones with pre-3.8 kernels. 

#---------------------------------------------------#
# Changes to this file may lead to permanent damage #
# to you Beaglebone, edit with care.                #
#---------------------------------------------------#

# Load the common beaglebone configuration:
from config_common import *


########################################
##--- Start control module config: ---##

PINMUX_PATH = '/sys/kernel/debug/omap_mux/'

CONF_UART_TX     = CONF_PULL_DISABLE
CONF_UART_RX     = CONF_PULLUP | CONF_RX_ACTIVE

##--- End control module config ------##
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
#    [port, tx_pinmux_filename, tx_pinmux_mode, 
#           rx_pinmux_filename, rx_pinmux_mode]

UART = {
  'UART1' : ['/dev/ttyO1', 'uart1_txd', 0,  'uart1_rxd', 0],
  'UART2' : ['/dev/ttyO2',   'spi0_d0', 1,  'spi0_sclk', 1],
  'UART4' : ['/dev/ttyO4',  'gpmc_wpn', 6, 'gpmc_wait0', 6],
  'UART5' : ['/dev/ttyO5', 'lcd_data8', 4,  'lcd_data9', 4]
}


##--- End UART config ------##
##############################


##############################
##--- Start PWM config: ----##

PWM_CTRL_DIR = "/sys/class/pwm/"

# EHRPWM pinmux config dict in form:
#  [mux_file, mux_mode, pwm_ctrl_dir]

PWM_PINS = {
  'PWM1A' : [ 'gpmc_a2', 0x06, 'ehrpwm.1:0/'],
  'PWM1B' : [ 'gpmc_a3', 0x06, 'ehrpwm.1:1/']
}
PWM1A = 'PWM1A'
PWM1B = 'PWM1B'


import os
if (os.path.exists(PWM_CTRL_DIR+'ehrpwm.2:0/')):
  PWM_PINS['PWM2A'] = ['gpmc_ad8', 0x04, 'ehrpwm.2:0/']
  PWM_PINS['PWM2B'] = ['gpmc_ad9', 0x04, 'ehrpwm.2:1/']
  PWM2A = 'PWM2A'
  PWM2B = 'PWM2B'


PWM_FILES = dict(\
  (i, [open(PWM_CTRL_DIR+PWM_PINS[i][2]+'request', 'r+'),
       open(PWM_CTRL_DIR+PWM_PINS[i][2]+'run', 'r+'),
       open(PWM_CTRL_DIR+PWM_PINS[i][2]+'duty_ns', 'r+'),
       open(PWM_CTRL_DIR+PWM_PINS[i][2]+'period_freq', 'r+') ])\
  for i in PWM_PINS.keys())

##--- End PWM config: ------##
##############################

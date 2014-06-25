# PyBBIO config file for BeagleBones with pre-3.8 kernels. 

#---------------------------------------------------#
# Changes to this file may lead to permanent damage #
# to you Beaglebone, edit with care.                #
#---------------------------------------------------#

# Load the common beaglebone configuration:
from bbio.platform.beaglebone.config_common import *


##############################
##--- Start PRCM config: ---##
## Power Management and Clock Module

#--- Module clock control: ---
CM_PER = 0x44e00000-MMAP_OFFSET
CM_WKUP = 0x44e00400-MMAP_OFFSET

CM_PER_EPWMSS0_CLKCTRL = 0xd4+CM_PER
CM_PER_EPWMSS1_CLKCTRL = 0xcc+CM_PER
CM_PER_EPWMSS2_CLKCTRL = 0xd8+CM_PER

CM_WKUP_ADC_TSC_CLKCTRL = 0xbc+CM_WKUP

MODULEMODE_ENABLE = 0x02
IDLEST_MASK = 0x03<<16
# To enable module clock:
#  _setReg(CM_WKUP_module_CLKCTRL, MODULEMODE_ENABLE)
#  while (_getReg(CM_WKUP_module_CLKCTRL) & IDLEST_MASK): pass
# To disable module clock:
#  _andReg(CM_WKUP_module_CLKCTRL, ~MODULEMODE_ENABLE)
#-----------------------------

##--- End PRCM config ------##
##############################


########################################
##--- Start control module config: ---##

PINMUX_PATH = '/sys/kernel/debug/omap_mux/'

CONF_UART_TX     = CONF_PULL_DISABLE
CONF_UART_RX     = CONF_PULLUP | CONF_RX_ACTIVE

##--- End control module config ------##
########################################


##############################
##--- Start ADC config: ----##

ADC_TSC = 0x44e0d000-MMAP_OFFSET

## Registers:

ADC_SYSCONFIG = ADC_TSC+0x10

ADC_SOFTRESET = 0x01


#--- ADC_CTRL ---
ADC_CTRL = ADC_TSC+0x40

ADC_STEPCONFIG_WRITE_PROTECT_OFF = 0x01<<2
# Write protect default on, must first turn off to change stepconfig:
#  _setReg(ADC_CTRL, ADC_STEPCONFIG_WRITE_PROTECT_OFF)
# To set write protect on:
#  _clearReg(ADC_CTRL, ADC_STEPCONFIG_WRITE_PROTECT_OFF)
 
TSC_ADC_SS_ENABLE = 0x01 
# To enable:
# _setReg(ADC_CTRL, TSC_ADC_SS_ENABLE)
#  This will turn STEPCONFIG write protect back on 
# To keep write protect off:
# _orReg(ADC_CTRL, TSC_ADC_SS_ENABLE)
#----------------

ADC_CLKDIV = ADC_TSC+0x4c  # Write desired value-1

#--- ADC_STEPENABLE ---
ADC_STEPENABLE = ADC_TSC+0x54

ADC_ENABLE = lambda AINx: 0x01<<(ADC[AINx]+1)
#----------------------

ADC_IDLECONFIG = ADC_TSC+0x58

#--- ADC STEPCONFIG ---
ADCSTEPCONFIG1 = ADC_TSC+0x64
ADCSTEPDELAY1  = ADC_TSC+0x68
ADCSTEPCONFIG2 = ADC_TSC+0x6c
ADCSTEPDELAY2  = ADC_TSC+0x70
ADCSTEPCONFIG3 = ADC_TSC+0x74
ADCSTEPDELAY3  = ADC_TSC+0x78
ADCSTEPCONFIG4 = ADC_TSC+0x7c
ADCSTEPDELAY4  = ADC_TSC+0x80
ADCSTEPCONFIG5 = ADC_TSC+0x84
ADCSTEPDELAY5  = ADC_TSC+0x88
ADCSTEPCONFIG6 = ADC_TSC+0x8c
ADCSTEPDELAY6  = ADC_TSC+0x90
ADCSTEPCONFIG7 = ADC_TSC+0x94
ADCSTEPDELAY7  = ADC_TSC+0x98
ADCSTEPCONFIG8 = ADC_TSC+0x9c
ADCSTEPDELAY8  = ADC_TSC+0xa0
# Only need the first 8 steps - 1 for each AIN pin


ADC_RESET = 0x00 # Default value of STEPCONFIG

ADC_AVG2  = 0x01<<2
ADC_AVG4  = 0x02<<2
ADC_AVG8  = 0x03<<2
ADC_AVG16 = 0x04<<2

#SEL_INP = lambda AINx: (ADC[AINx]+1)<<19
# Set input with _orReg(ADCSTEPCONFIGx, SEL_INP(AINx))
# ADC[AINx]+1 because positive AMUX input 0 is VREFN 
#  (see user manual section 12.3.7)
SEL_INP = lambda AINx: (ADC[AINx])<<19

SAMPLE_DELAY = lambda cycles: (cycles&0xff)<<24
# SAMPLE_DELAY is the number of cycles to sample for
# Set delay with _orReg(ADCSTEPDELAYx, SAMPLE_DELAY(cycles))

#----------------------
 
#--- ADC FIFO ---
ADC_FIFO0DATA = ADC_TSC+0x100

ADC_FIFO_MASK = 0xfff
# ADC result = _getReg(ADC_FIFO0DATA)&ADC_FIFO_MASK
#----------------

## ADC pins:

ADC = {
  'AIN0' : 0x00,
  'AIN1' : 0x01,
  'AIN2' : 0x02,
  'AIN3' : 0x03,
  'AIN4' : 0x04,
  'AIN5' : 0x05,
  'AIN6' : 0x06,
  'AIN7' : 0x07,
  'VSYS' : 0x07
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

##--- End ADC config -------##
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


# Indexes in PWM_FILES lists:
PWM_REQUEST = 0
PWM_ENABLE  = 1
PWM_DUTY    = 2
PWM_FREQ    = 3

##--- End PWM config: ------##
##############################

##############################
##--- Start I2C config: ---##

# I2C bus address must be in form: 
#    [dev-entry, I2C-overlay-name]

I2C = {
  'i2c1' : ['/dev/i2c-2', 'BB-I2C1'],
  'i2c2' : ['/dev/i2c-1', 'BB-I2C2'],
}

##--- End I2C config ------##
##############################


# Config file for PyBBIO 

#---------------------------------------------------#
# Changes to this file may lead to permanent damage #
# to you Beaglebone, edit with care.                #
#---------------------------------------------------#


LIBRARIES_PATH = """Do not edit!"""
# This will be replaced in installed config file with
# the correct path to the libraries folder. Do not edit
# this line.

MMAP_OFFSET = 0x44c00000 
MMAP_SIZE   = 0x48ffffff-MMAP_OFFSET

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

CONF_SLEW_SLOW    = 1<<6
CONF_RX_ACTIVE    = 1<<5
CONF_PULLUP       = 1<<4
CONF_PULLDOWN     = 0x00
CONF_PULL_DISABLE = 1<<3

CONF_GPIO_MODE   = 0x07 
CONF_GPIO_OUTPUT = CONF_GPIO_MODE
CONF_GPIO_INPUT  = CONF_GPIO_MODE | CONF_RX_ACTIVE
CONF_ADC_PIN     = CONF_RX_ACTIVE | CONF_PULL_DISABLE

CONF_UART_TX     = CONF_PULL_DISABLE
CONF_UART_RX     = CONF_PULLUP | CONF_RX_ACTIVE

##--- End control module config ------##
########################################

##############################
##--- Start GPIO config: ---##
GPIO0 = 0x44e07000-MMAP_OFFSET
GPIO1 = 0x4804c000-MMAP_OFFSET
GPIO2 = 0x481ac000-MMAP_OFFSET
GPIO3 = 0x481ae000-MMAP_OFFSET

GPIO_OE           = 0x134
GPIO_DATAIN       = 0x138
GPIO_DATAOUT      = 0x13c
GPIO_CLEARDATAOUT = 0x190
GPIO_SETDATAOUT   = 0x194

# Digital IO keywords:
INPUT    =  1
OUTPUT   =  0
HIGH     =  1
LOW      =  0
RISING   =  1
FALLING  = -1
MSBFIRST =  1
LSBFIRST = -1

## GPIO pins:

# GPIO pins must be in form: 
#             [GPIO_mux, bit_value, pinmux_filename], e.g.:
# "GPIO1_4" = [   GPIO1,      1<<4,      'gpmc_ad4']  

GPIO = {
      "USR0" : [GPIO1, 1<<21,           'gpmc_a5'],
      "USR1" : [GPIO1, 1<<22,           'gpmc_a6'],
      "USR2" : [GPIO1, 1<<23,           'gpmc_a7'],
      "USR3" : [GPIO1, 1<<24,           'gpmc_a8'],
   "GPIO0_7" : [GPIO0,  1<<7, 'ecap0_in_pwm0_out'],
  "GPIO0_26" : [GPIO0, 1<<26,         'gpmc_ad10'],
  "GPIO0_27" : [GPIO0, 1<<27,         'gpmc_ad11'],
   "GPIO1_0" : [GPIO1,     1,          'gpmc_ad0'],
   "GPIO1_1" : [GPIO1,  1<<1,          'gpmc_ad1'],
   "GPIO1_2" : [GPIO1,  1<<2,          'gpmc_ad2'],
   "GPIO1_3" : [GPIO1,  1<<3,          'gpmc_ad3'],
   "GPIO1_4" : [GPIO1,  1<<4,          'gpmc_ad4'],
   "GPIO1_5" : [GPIO1,  1<<5,          'gpmc_ad5'],
   "GPIO1_6" : [GPIO1,  1<<6,          'gpmc_ad6'],
   "GPIO1_7" : [GPIO1,  1<<7,          'gpmc_ad7'],
  "GPIO1_12" : [GPIO1, 1<<12,         'gpmc_ad12'],
  "GPIO1_13" : [GPIO1, 1<<13,         'gpmc_ad13'],
  "GPIO1_14" : [GPIO1, 1<<14,         'gpmc_ad14'],
  "GPIO1_15" : [GPIO1, 1<<15,         'gpmc_ad15'],
  "GPIO1_16" : [GPIO1, 1<<16,           'gpmc_a0'],
  "GPIO1_17" : [GPIO1, 1<<17,           'gpmc_a1'],
  "GPIO1_28" : [GPIO1, 1<<28,         'gpmc_ben1'],
  "GPIO1_29" : [GPIO1, 1<<29,         'gpmc_csn0'],
  "GPIO1_30" : [GPIO1, 1<<30,         'gpmc_csn1'],
  "GPIO1_31" : [GPIO1, 1<<31,         'gpmc_csn2'],
   "GPIO2_1" : [GPIO2,  1<<1,          'gpmc_clk'],
   "GPIO2_6" : [GPIO2,  1<<6,         'lcd_data0'],
   "GPIO2_7" : [GPIO2,  1<<7,         'lcd_data1'],
   "GPIO2_8" : [GPIO2,  1<<8,         'lcd_data2'],
   "GPIO2_9" : [GPIO2,  1<<9,         'lcd_data3'],
  "GPIO2_10" : [GPIO2, 1<<10,         'lcd_data4'],
  "GPIO2_11" : [GPIO2, 1<<11,         'lcd_data5'],
  "GPIO2_12" : [GPIO2, 1<<12,         'lcd_data6'],
  "GPIO2_13" : [GPIO2, 1<<13,         'lcd_data7'],
  "GPIO2_22" : [GPIO2, 1<<22,         'lcd_vsync'],
  "GPIO2_23" : [GPIO2, 1<<23,         'lcd_hsync'],
  "GPIO2_24" : [GPIO2, 1<<24,          'lcd_pclk'],
  "GPIO2_25" : [GPIO2, 1<<25,    'lcd_ac_bias_en'],
  "GPIO3_19" : [GPIO3, 1<<19,        'mcasp0_fsr'],
  "GPIO3_21" : [GPIO3, 1<<21,     'mcasp0_ahclkx']
}

# Having available pins in a dictionary makes it easy to
# check for invalid pins, but it's nice not to have to pass
# around strings, so here's some friendly constants:
USR0     = "USR0"
USR1     = "USR1"
USR2     = "USR2"
USR3     = "USR3"
GPIO0_7  = "GPIO0_7"
GPIO0_26 = "GPIO0_26"
GPIO0_27 = "GPIO0_27"
GPIO1_0  = "GPIO1_0"
GPIO1_1  =  "GPIO1_1"
GPIO1_2  = "GPIO1_2"
GPIO1_3  = "GPIO1_3"
GPIO1_4  = "GPIO1_4"
GPIO1_5  = "GPIO1_5"
GPIO1_6  = "GPIO1_6"
GPIO1_7  = "GPIO1_7"
GPIO1_12 = "GPIO1_12"
GPIO1_13 = "GPIO1_13"
GPIO1_14 = "GPIO1_14"
GPIO1_15 = "GPIO1_15"
GPIO1_16 = "GPIO1_16"
GPIO1_17 = "GPIO1_17"
GPIO1_28 = "GPIO1_28"
GPIO1_29 =  "GPIO1_29"
GPIO1_30 = "GPIO1_30"
GPIO1_31 =  "GPIO1_31"
GPIO2_1  = "GPIO2_1"
GPIO2_6  = "GPIO2_6"
GPIO2_7  = "GPIO2_7"
GPIO2_8  = "GPIO2_8"
GPIO2_9  = "GPIO2_9"
GPIO2_10 = "GPIO2_10"
GPIO2_11 =  "GPIO2_11"
GPIO2_12 = "GPIO2_12"
GPIO2_13 = "GPIO2_13"
GPIO2_22 = "GPIO2_22"
GPIO2_23 = "GPIO2_23" 
GPIO2_24 = "GPIO2_24"
GPIO2_25 = "GPIO2_25"
GPIO3_19 = "GPIO3_19"
GPIO3_21 = "GPIO3_21"


##--- End GPIO config ------##
##############################

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

# Formatting constants to mimic Arduino's serial.print() formatting:
DEC = 'DEC'
BIN = 'BIN'
OCT = 'OCT'
HEX = 'HEX'

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

# Predefined resolutions for analogWrite():
RES_16BIT = 2**16
RES_8BIT  = 2**8
PERCENT   = 100

# Default frequency in Hz of PWM modules (must be >0):
PWM_DEFAULT_FREQ = 100000

##--- End PWM config: ------##
##############################

# PyBBIO config file for bealebone

#---------------------------------------------------#
# Changes to this file may lead to permanent damage #
# to you Beaglebone, edit with care.                #
#---------------------------------------------------#

import glob

########################################
##--- Start control module config: ---##

CONF_SLEW_SLOW    = 1<<6
CONF_RX_ACTIVE    = 1<<5
CONF_PULLUP       = 1<<4
CONF_PULLDOWN     = 0x00
CONF_PULL_DISABLE = 1<<3

CONF_GPIO_MODE   = 0x07 
CONF_GPIO_OUTPUT = CONF_GPIO_MODE
CONF_GPIO_INPUT  = CONF_GPIO_MODE | CONF_RX_ACTIVE
CONF_ADC_PIN     = CONF_RX_ACTIVE | CONF_PULL_DISABLE

##--- End control module config ------##
########################################

########################################
##--- Start device tree: ---##

SLOTS_FILE = glob.glob('/sys/devices/bone_capemgr.*/slots')
SLOTS_FILE = SLOTS_FILE[0] if len(SLOTS_FILE) else None
OCP_PATH = glob.glob('/sys/devices/ocp.*')[0]

##--- End device tree config ------##
########################################

##############################
##--- Start GPIO config: ---##

GPIO_FILE_BASE = '/sys/class/gpio'
EXPORT_FILE = GPIO_FILE_BASE + '/export'
UNEXPORT_FILE = GPIO_FILE_BASE + '/unexport'

GET_USR_LED_DIRECTORY = lambda USRX : \
  "/sys/class/leds/beaglebone:green:%s" % USRX.lower()

# Digital IO keywords:
INPUT    =  1
OUTPUT   =  0
PULLDOWN = -1
NOPULL   =  0
PULLUP   =  1
HIGH     =  1
LOW      =  0
RISING   =  1
FALLING  = -1
BOTH     =  0
MSBFIRST =  1
LSBFIRST = -1

## GPIO pins:

# GPIO pins must be in form: 
#             [signal_name, dt_offset, gpio_num], where 'dt_offset' is 
# the control module register offset from 44e10800 as used in the device 
# tree, and 'gpio_num' is the pin number used by the kernel driver,  e.g.:
# "GPIO1_4" = [ 'gpmc_ad4',      0x10, 32*1 + 4]

GPIO = {
  "USR0" : {
    'signal' : 'gpmc_a5', 
    'offset' : 0x054, 
    'gpio_num' : 1*32+21,
    'header_pin' : None
  },
  "USR1" : {
    'signal' : 'gpmc_a6', 
    'offset' : 0x058, 
    'gpio_num' : 1*32+22,
    'header_pin' : None
  },
  "USR2" : {
    'signal' : 'gpmc_a7', 
    'offset' : 0x05c, 
    'gpio_num' : 1*32+23,
    'header_pin' : None
  },
  "USR3" : {
    'signal' : 'gpmc_a8', 
    'offset' : 0x060, 
    'gpio_num' : 1*32+24,
    'header_pin' : None
  },
  "GPIO0_2" : {
    'signal' : 'spi0_sclk', 
    'offset' : 0x150, 
    'gpio_num' : 0*32+2,
    'header_pin' : 'P9_22'
  },
  "GPIO0_3" : {
    'signal' : 'spi0_d0', 
    'offset' : 0x154, 
    'gpio_num' : 0*32+3,
    'header_pin' : 'P9_21'
  },
  "GPIO0_4" : {
    'signal' : 'spi0_d1', 
    'offset' : 0x158, 
    'gpio_num' : 0*32+4,
    'header_pin' : 'P9_18'
  },
  "GPIO0_5" : {
    'signal' : 'spi0_cs0', 
    'offset' : 0x15c, 
    'gpio_num' : 0*32+5,
    'header_pin' : 'P9_17'
  },
  "GPIO0_7" : {
    'signal' : 'ecap0_in_pwm0_out', 
    'offset' : 0x164, 
    'gpio_num' : 0*32+7,
    'header_pin' : 'P9_42'
  },
  "GPIO0_8" : {
    'signal' : 'lcd_data12', 
    'offset' : 0x0d0, 
    'gpio_num' : 0*32+8,
    'header_pin' : 'P8_35'
  },
  "GPIO0_9" : {
    'signal' : 'lcd_data13', 
    'offset' : 0x0d4, 
    'gpio_num' : 0*32+9,
    'header_pin' : 'P8_33'
  },
  "GPIO0_10" : {
    'signal' : 'lcd_data14', 
    'offset' : 0x0d8, 
    'gpio_num' : 0*32+10,
    'header_pin' : 'P8_31'
  },
  "GPIO0_11" : {
    'signal' : 'lcd_data15', 
    'offset' : 0x0dc, 
    'gpio_num' : 0*32+11,
    'header_pin' : 'P8_32'
  },
  "GPIO0_12" : {
    'signal' : 'uart1_ctsn', 
    'offset' : 0x178, 
    'gpio_num' : 0*32+12,
    'header_pin' : 'P9_20'
  },
    "GPIO0_13" : {
    'signal' : 'uart1_rtsn', 
    'offset' : 0x17c, 
    'gpio_num' : 0*32+13,
    'header_pin' : 'P9_19'
  },
  "GPIO0_14" : {
    'signal' : 'uart1_rxd', 
    'offset' : 0x180, 
    'gpio_num' : 0*32+14,
    'header_pin' : 'P9_26'
  },
  "GPIO0_15" : {
    'signal' : 'uart1_txd', 
    'offset' : 0x184, 
    'gpio_num' : 0*32+15,
    'header_pin' : 'P9_24'
  },
  "GPIO0_20" : {
    'signal' : 'xdma_event_intr1', 
    'offset' : 0x1b4, 
    'gpio_num' : 0*32+20,
    'header_pin' : 'P9_41'
  },
  "GPIO0_22" : {
    'signal' : 'gpmc_ad8', 
    'offset' : 0x020, 
    'gpio_num' : 0*32+22,
    'header_pin' : 'P8_19'
  },
  "GPIO0_23" : {
    'signal' : 'gpmc_ad9', 
    'offset' : 0x024, 
    'gpio_num' : 0*32+23,
    'header_pin' : 'P8_13'
  },
  "GPIO0_26" : {
    'signal' : 'gpmc_ad10', 
    'offset' : 0x028, 
    'gpio_num' : 0*32+26,
    'header_pin' : 'P8_14'
  },
  "GPIO0_27" : {
    'signal' : 'gpmc_ad11', 
    'offset' : 0x02c, 
    'gpio_num' : 0*32+27,
    'header_pin' : 'P8_17'
  },
  "GPIO0_30" : {
    'signal' : 'gpmc_wait0', 
    'offset' : 0x070, 
    'gpio_num' : 0*32+30,
    'header_pin' : 'P9_11'
  },
  "GPIO0_31" : {
    'signal' : 'gpmc_wpn', 
    'offset' : 0x074, 
    'gpio_num' : 0*32+31,
    'header_pin' : 'P9_13'
  },
  "GPIO1_0" : {
    'signal' : 'gpmc_ad0', 
    'offset' : 0x000, 
    'gpio_num' : 1*32+0,
    'header_pin' : 'P8_25'
  },
  "GPIO1_1" : {
    'signal' : 'gpmc_ad1', 
    'offset' : 0x004, 
    'gpio_num' : 1*32+1,
    'header_pin' : 'P8_24'
  },
  "GPIO1_2" : {
    'signal' : 'gpmc_ad2', 
    'offset' : 0x008, 
    'gpio_num' : 1*32+2,
    'header_pin' : 'P8_5'
  },
  "GPIO1_3" : {
    'signal' : 'gpmc_ad3', 
    'offset' : 0x00c, 
    'gpio_num' : 1*32+3,
    'header_pin' : 'P8_6'
  },
  "GPIO1_4" : {
    'signal' : 'gpmc_ad4', 
    'offset' : 0x010, 
    'gpio_num' : 1*32+4,
    'header_pin' : 'P8_23'
  },
  "GPIO1_5" : {
    'signal' : 'gpmc_ad5', 
    'offset' : 0x014, 
    'gpio_num' : 1*32+ 5,
    'header_pin' : 'P8_22'
  },
  "GPIO1_6" : {
    'signal' : 'gpmc_ad6', 
    'offset' : 0x018, 
    'gpio_num' : 1*32+6,
    'header_pin' : 'P8_3'
  },
  "GPIO1_7" : {
    'signal' : 'gpmc_ad7', 
    'offset' : 0x01c, 
    'gpio_num' : 1*32+7,
    'header_pin' : 'P8_4'
  },
  "GPIO1_12" : {
    'signal' : 'gpmc_ad12', 
    'offset' : 0x030, 
    'gpio_num' : 1*32+12,
    'header_pin' : 'P8_12'
  },
  "GPIO1_13" : {
    'signal' : 'gpmc_ad13', 
    'offset' : 0x034, 
    'gpio_num' : 1*32+13,
    'header_pin' : 'P8_11'
  },
  "GPIO1_14" : {
    'signal' : 'gpmc_ad14', 
    'offset' : 0x038, 
    'gpio_num' : 1*32+14,
    'header_pin' : 'P8_16'
  },
  "GPIO1_15" : {
    'signal' : 'gpmc_ad15', 
    'offset' : 0x03c, 
    'gpio_num' : 1*32+15,
    'header_pin' : 'P8_15'
  },
  "GPIO1_16" : {
    'signal' : 'gpmc_a0', 
    'offset' : 0x040, 
    'gpio_num' : 1*32+16,
    'header_pin' : 'P9_15'
  },
  "GPIO1_17" : {
    'signal' : 'gpmc_a1', 
    'offset' : 0x044, 
    'gpio_num' : 1*32+17,
    'header_pin' : 'P9_23'
  },
  "GPIO1_18" : {
    'signal' : 'gpmc_a2', 
    'offset' : 0x048, 
    'gpio_num' : 1*32+18,
    'header_pin' : 'P9_14'
  },
  "GPIO1_19" : {
    'signal' : 'gpmc_a3', 
    'offset' : 0x04c, 
    'gpio_num' : 1*32+19,
    'header_pin' : 'P9_16'
  },
  "GPIO1_28" : {
    'signal' : 'gpmc_ben1', 
    'offset' : 0x078, 
    'gpio_num' : 1*32+28,
    'header_pin' : 'P9_12'
  },
  "GPIO1_29" : {
    'signal' : 'gpmc_csn0', 
    'offset' : 0x07c, 
    'gpio_num' : 1*32+29,
    'header_pin' : 'P8_26'
  },
  "GPIO1_30" : {
    'signal' : 'gpmc_csn1', 
    'offset' : 0x080, 
    'gpio_num' : 1*32+30,
    'header_pin' : 'P8_21'
  },
  "GPIO1_31" : {
    'signal' : 'gpmc_csn2', 
    'offset' : 0x084, 
    'gpio_num' : 1*32+31,
    'header_pin' : 'P8_20'
  },
  "GPIO2_1" : {
    'signal' : 'gpmc_clk', 
    'offset' : 0x08c, 
    'gpio_num' : 2*32+1,
    'header_pin' : 'P8_18'
  },
  "GPIO2_2" : {
    'signal' : 'gpmc_advn_ale', 
    'offset' : 0x090, 
    'gpio_num' : 2*32+2,
    'header_pin' : 'P8_7'
  },
  "GPIO2_3" : {
    'signal' : 'gpmc_oen_ren', 
    'offset' : 0x094, 
    'gpio_num' : 2*32+3,
    'header_pin' : 'P8_8'
  },
  "GPIO2_4" : {
    'signal' : 'gpmc_wen', 
    'offset' : 0x098, 
    'gpio_num' : 2*32+4,
    'header_pin' : 'P8_10'
  },
  "GPIO2_5" : {
    'signal' : 'gpmc_ben0_cle', 
    'offset' : 0x09c, 
    'gpio_num' : 2*32+5,
    'header_pin' : 'P8_9'
  },
  "GPIO2_6" : {
    'signal' : 'lcd_data0', 
    'offset' : 0x0a0, 
    'gpio_num' : 2*32+6,
    'header_pin' : 'P8_45'
  },
  "GPIO2_7" : {
    'signal' : 'lcd_data1', 
    'offset' : 0x0a4, 
    'gpio_num' : 2*32+7,
    'header_pin' : 'P8_46'
  },
  "GPIO2_8" : {
    'signal' : 'lcd_data2', 
    'offset' : 0x0a8, 
    'gpio_num' : 2*32+8,
    'header_pin' : 'P8_43'
  },
  "GPIO2_9" : {
    'signal' : 'lcd_data3', 
    'offset' : 0x0ac, 
    'gpio_num' : 2*32+9,
    'header_pin' : 'P8_44'
  },
  "GPIO2_10" : {
    'signal' : 'lcd_data4', 
    'offset' : 0x0b0, 
    'gpio_num' : 2*32+10,
    'header_pin' : 'P8_41'
  },
  "GPIO2_11" : {
    'signal' : 'lcd_data5', 
    'offset' : 0x0b4, 
    'gpio_num' : 2*32+11,
    'header_pin' : 'P8_42'
  },
  "GPIO2_12" : {
    'signal' : 'lcd_data6', 
    'offset' : 0x0b8, 
    'gpio_num' : 2*32+12,
    'header_pin' : 'P8_39'
  },
  "GPIO2_13" : {
    'signal' : 'lcd_data7', 
    'offset' : 0x0bc, 
    'gpio_num' : 2*32+13,
    'header_pin' : 'P8_40'
  },
  "GPIO2_14" : {
    'signal' : 'lcd_data8', 
    'offset' : 0x0c0, 
    'gpio_num' : 2*32+14,
    'header_pin' : 'P8_37'
  }, 
  "GPIO2_15" : {
    'signal' : 'lcd_data9', 
    'offset' : 0x0c4, 
    'gpio_num' : 2*32+15,
    'header_pin' : 'P8_38'
  },
  "GPIO2_16" : {
    'signal' : 'lcd_data10', 
    'offset' : 0x0c8, 
    'gpio_num' : 2*32+16,
    'header_pin' : 'P8_36'
  },
  "GPIO2_17" : {
    'signal' : 'lcd_data11', 
    'offset' : 0x0cc, 
    'gpio_num' : 2*32+17,
    'header_pin' : 'P8_34'
  },
  "GPIO2_22" : {
    'signal' : 'lcd_vsync', 
    'offset' : 0x0e0, 
    'gpio_num' : 2*32+22,
    'header_pin' : 'P8_27'
  },
  "GPIO2_23" : {
    'signal' : 'lcd_hsync', 
    'offset' : 0x0e4, 
    'gpio_num' : 2*32+23,
    'header_pin' : 'P8_29'
  },
  "GPIO2_24" : {
    'signal' : 'lcd_pclk', 
    'offset' : 0x0e8, 
    'gpio_num' : 2*32+24,
    'header_pin' : 'P8_28'
  },
  "GPIO2_25" : {
    'signal' : 'lcd_ac_bias_en', 
    'offset' : 0x0ec, 
    'gpio_num' : 2*32+25,
    'header_pin' : 'P8_30'
  },
  "GPIO3_14" : {
    'signal' : 'mcasp0_aclkx', 
    'offset' : 0x190, 
    'gpio_num' : 3*32+14,
    'header_pin' : 'P9_31'
  },
  "GPIO3_15" : {
    'signal' : 'mcasp0_fsx', 
    'offset' : 0x194, 
    'gpio_num' : 3*32+15,
    'header_pin' : 'P9_29'
  },
  "GPIO3_16" : {
    'signal' : 'mcasp0_axr0', 
    'offset' : 0x198, 
    'gpio_num' : 3*32+16,
    'header_pin' : 'P9_30'
  },
  "GPIO3_17" : {
    'signal' : 'mcasp0_ahclkr', 
    'offset' : 0x19c, 
    'gpio_num' : 3*32+17,
    'header_pin' : 'P9_28'
  },
  "GPIO3_19" : {
    'signal' : 'mcasp0_fsr', 
    'offset' : 0x1a4, 
    'gpio_num' : 3*32+19,
    'header_pin' : 'P9_27'
  },
  "GPIO3_21" : {
    'signal' : 'mcasp0_ahclkx', 
    'offset' : 0x1ac, 
    'gpio_num' : 3*32+21,
    'header_pin' : 'P9_25'
  },
}

def getGPIODirectory(gpio_pin):
  """ Returns the sysfs kernel driver base directory for the given pin. """
  if 'USR' in gpio_pin:
    # USR LEDs use a different driver
    return GET_USR_LED_DIRECTORY(gpio_pin)
  gpio_num = GPIO[gpio_pin]['gpio_num']
  return '%s/gpio%i' % (GPIO_FILE_BASE, gpio_num)


def getGPIODirectionFile(gpio_pin):
  """ Returns the absolute path to the state control file for the given pin. """
  if 'USR' in gpio_pin:
    # USR LED driver doesn't have a direction file
    return ''
  d = getGPIODirectory(gpio_pin)
  return '%s/direction' % d


def getGPIOStateFile(gpio_pin):
  """ Returns the absolute path to the state control file for the given pin. """
  d = getGPIODirectory(gpio_pin)
  if 'USR' in gpio_pin:
    # USR LEDs use a different driver
    return '%s/brightness' % d
  return '%s/value' % d
  
for pin in GPIO.keys():
  GPIO[pin]['direction_file'] = getGPIODirectionFile(pin)
  GPIO[pin]['state_file'] = getGPIOStateFile(pin)

# Having available pins in a dictionary makes it easy to
# check for invalid pins, but it's nice not to have to pass
# around strings, so here's some friendly constants:
USR0 = "USR0"
USR1 = "USR1"
USR2 = "USR2"
USR3 = "USR3"
GPIO0_2  = "GPIO0_2"
GPIO0_3  = "GPIO0_3"
GPIO0_4  = "GPIO0_4"
GPIO0_5  = "GPIO0_5"
GPIO0_7  = "GPIO0_7"
GPIO0_8  = "GPIO0_8"
GPIO0_9  = "GPIO0_9"
GPIO0_10 = "GPIO0_10"
GPIO0_11 = "GPIO0_11"
GPIO0_12 = "GPIO0_12"
GPIO0_13 = "GPIO0_13"
GPIO0_14 = "GPIO0_14"
GPIO0_15 = "GPIO0_15"
GPIO0_20 = "GPIO0_20"
GPIO0_22 = "GPIO0_22"
GPIO0_23 = "GPIO0_23"
GPIO0_26 = "GPIO0_26"
GPIO0_27 = "GPIO0_27"
GPIO0_30 = "GPIO0_30"
GPIO0_31 = "GPIO0_31"
GPIO1_0  = "GPIO1_0"
GPIO1_1  = "GPIO1_1"
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
GPIO1_18 = "GPIO1_18"
GPIO1_19 = "GPIO1_19"
GPIO1_28 = "GPIO1_28"
GPIO1_29 = "GPIO1_29"
GPIO1_30 = "GPIO1_30"
GPIO1_31 = "GPIO1_31"
GPIO2_1  = "GPIO2_1"
GPIO2_2  = "GPIO2_2"
GPIO2_3  = "GPIO2_3"
GPIO2_4  = "GPIO2_4"
GPIO2_5  = "GPIO2_5"
GPIO2_6  = "GPIO2_6"
GPIO2_7  = "GPIO2_7"
GPIO2_8  = "GPIO2_8"
GPIO2_9  = "GPIO2_9"
GPIO2_10 = "GPIO2_10"
GPIO2_11 = "GPIO2_11"
GPIO2_12 = "GPIO2_12"
GPIO2_13 = "GPIO2_13"
GPIO2_14 = "GPIO2_14"
GPIO2_15 = "GPIO2_15"
GPIO2_16 = "GPIO2_16"
GPIO2_17 = "GPIO2_17"
GPIO2_22 = "GPIO2_22"
GPIO2_23 = "GPIO2_23" 
GPIO2_24 = "GPIO2_24"
GPIO2_25 = "GPIO2_25"
GPIO3_14 = "GPIO3_14"
GPIO3_15 = "GPIO3_15"
GPIO3_16 = "GPIO3_16"
GPIO3_17 = "GPIO3_17"
GPIO3_19 = "GPIO3_19"
GPIO3_21 = "GPIO3_21"


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

# Formatting constants to mimic Arduino's serial.print() formatting:
DEC = 'DEC'
BIN = 'BIN'
OCT = 'OCT'
HEX = 'HEX'

UART = {
  'UART1' : ['/dev/ttyO1', 'BB-UART1'],
  'UART2' : ['/dev/ttyO2', 'BB-UART2'],
  'UART4' : ['/dev/ttyO4', 'BB-UART4'],
  'UART5' : ['/dev/ttyO5', 'BB-UART5']
}

##--- End UART config ------##
##############################


##############################
##--- Start PWM config: ----##

# Predefined resolutions for analogWrite():
RES_16BIT = 2**16
RES_8BIT  = 2**8
PERCENT   = 100

# Default frequency in Hz of PWM modules (must be >0):
PWM_DEFAULT_FREQ = 100000

# PWM config dict in form:
#  ['overlay_file', 'path/to/ocp_helper_dir', ['required', 'overlays']]

PWM_PINS = {
  'PWM1A' : ['bone_pwm_P9_14', '%s/pwm_test_P9_14.*' % OCP_PATH, 
             ['PyBBIO-epwmss1', 'PyBBIO-ehrpwm1']],
  'PWM1B' : ['bone_pwm_P9_16', '%s/pwm_test_P9_16.*' % OCP_PATH, 
             ['PyBBIO-epwmss1', 'PyBBIO-ehrpwm1']],

  'PWM2A' : ['bone_pwm_P8_19', '%s/pwm_test_P8_19.*' % OCP_PATH, 
             ['PyBBIO-epwmss2', 'PyBBIO-ehrpwm2']],
  'PWM2B' : ['bone_pwm_P8_13', '%s/pwm_test_P8_13.*' % OCP_PATH, 
             ['PyBBIO-epwmss2', 'PyBBIO-ehrpwm2']],

  'ECAP0' : ['bone_pwm_P9_42', '%s/pwm_test_P9_42.*' % OCP_PATH, 
             ['PyBBIO-epwmss0', 'PyBBIO-ecap0']],
  'ECAP1' : ['bone_pwm_P9_28', '%s/pwm_test_P9_28.*' % OCP_PATH, 
             ['PyBBIO-epwmss1', 'PyBBIO-ecap1']],

}
# Using the built-in pin overlays for now, I see no need for custom ones 

PWM1A = 'PWM1A'
PWM1B = 'PWM1B'
PWM2A = 'PWM2A'
PWM2B = 'PWM2B'
ECAP0 = 'ECAP0'
ECAP1 = 'ECAP1'

# ocp helper filenames:
PWM_RUN      = 'run'
PWM_DUTY     = 'duty'
PWM_PERIOD   = 'period'
PWM_POLARITY = 'polarity'

PWM_DEFAULT_PERIOD = int(1e9/PWM_DEFAULT_FREQ)

##--- End PWM config: ------##
##############################


##############################
##--- Start I2C config: ---##

# I2C bus address must be in form: 
#    [dev-entry, I2C-overlay-name]
# rather confusing bus address and dev-entry don't exactly match
# i2c0, i2c2 buses are activated by default i.e. /dev/12c-0 and /dev/i2c-1
# more info - http://datko.net/2013/11/03/bbb_i2c/
# NOTE : 1st I2C bus - i2c0 is used to read eeproms of capes - Don't use that for other purposes


I2C = {
  'i2c0' : ['/dev/i2c-0', 'BB-I2C0'],
  'i2c1' : ['/dev/i2c-2', 'BB-I2C1'],
  'i2c2' : ['/dev/i2c-1', 'BB-I2C2'],
}

##--- End I2C config ------##
##############################

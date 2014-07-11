# PyBBIO config file for bealebone

#---------------------------------------------------#
# Changes to this file may lead to permanent damage #
# to you Beaglebone, edit with care.                #
#---------------------------------------------------#


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

##############################
##--- Start GPIO config: ---##

GPIO_FILE_BASE = '/sys/class/gpio'
EXPORT_FILE = GPIO_FILE_BASE + '/export'
UNEXPORT_FILE = GPIO_FILE_BASE + '/unexport'


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
      "USR0" : [          'gpmc_a5', 0x054, 1*32+21],
      "USR1" : [          'gpmc_a6', 0x058, 1*32+22],
      "USR2" : [          'gpmc_a7', 0x05c, 1*32+23],
      "USR3" : [          'gpmc_a8', 0x060, 1*32+24],
   "GPIO0_2" : [        'spi0_sclk', 0x150, 0*32+ 2],
   "GPIO0_3" : [          'spi0_d0', 0x154, 0*32+ 3],
   "GPIO0_4" : [          'spi0_d1', 0x158, 0*32+ 4],
   "GPIO0_5" : [         'spi0_cs0', 0x15c, 0*32+ 5],
   "GPIO0_7" : ['ecap0_in_pwm0_out', 0x164, 0*32+ 7],
   "GPIO0_8" : [       'lcd_data12', 0x0d0, 0*32+ 8],
   "GPIO0_9" : [       'lcd_data13', 0x0d4, 0*32+ 9],
  "GPIO0_10" : [       'lcd_data14', 0x0d8, 0*32+10],
  "GPIO0_11" : [       'lcd_data15', 0x0dc, 0*32+11],
  "GPIO0_12" : [       'uart1_ctsn', 0x178, 0*32+12],
  "GPIO0_13" : [       'uart1_rtsn', 0x17c, 0*32+13],
  "GPIO0_14" : [        'uart1_rxd', 0x180, 0*32+14],
  "GPIO0_15" : [        'uart1_txd', 0x184, 0*32+15],
  "GPIO0_20" : [ 'xdma_event_intr1', 0x1b4, 0*32+20],
  "GPIO0_22" : [         'gpmc_ad8', 0x020, 0*32+22],
  "GPIO0_23" : [         'gpmc_ad9', 0x024, 0*32+23],
  "GPIO0_26" : [        'gpmc_ad10', 0x028, 0*32+26],
  "GPIO0_27" : [        'gpmc_ad11', 0x02c, 0*32+27],
  "GPIO0_30" : [       'gpmc_wait0', 0x070, 0*32+30],
  "GPIO0_31" : [         'gpmc_wpn', 0x074, 0*32+31],
   "GPIO1_0" : [         'gpmc_ad0', 0x000, 1*32+ 0],
   "GPIO1_1" : [         'gpmc_ad1', 0x004, 1*32+ 1],
   "GPIO1_2" : [         'gpmc_ad2', 0x008, 1*32+ 2],
   "GPIO1_3" : [         'gpmc_ad3', 0x00c, 1*32+ 3],
   "GPIO1_4" : [         'gpmc_ad4', 0x010, 1*32+ 4],
   "GPIO1_5" : [         'gpmc_ad5', 0x014, 1*32+ 5],
   "GPIO1_6" : [         'gpmc_ad6', 0x018, 1*32+ 6],
   "GPIO1_7" : [         'gpmc_ad7', 0x01c, 1*32+ 7],
  "GPIO1_12" : [        'gpmc_ad12', 0x030, 1*32+12],
  "GPIO1_13" : [        'gpmc_ad13', 0x034, 1*32+13],
  "GPIO1_14" : [        'gpmc_ad14', 0x038, 1*32+14],
  "GPIO1_15" : [        'gpmc_ad15', 0x03c, 1*32+15],
  "GPIO1_16" : [          'gpmc_a0', 0x040, 1*32+16],
  "GPIO1_17" : [          'gpmc_a1', 0x044, 1*32+17],
  "GPIO1_18" : [          'gpmc_a2', 0x048, 1*32+18],
  "GPIO1_19" : [          'gpmc_a3', 0x04c, 1*32+19],
  "GPIO1_28" : [        'gpmc_ben1', 0x078, 1*32+28],
  "GPIO1_29" : [        'gpmc_csn0', 0x07c, 1*32+29],
  "GPIO1_30" : [        'gpmc_csn1', 0x080, 1*32+30],
  "GPIO1_31" : [        'gpmc_csn2', 0x084, 1*32+31],
   "GPIO2_1" : [         'gpmc_clk', 0x08c, 2*32+ 1],
   "GPIO2_2" : [    'gpmc_advn_ale', 0x090, 2*32+ 2],
   "GPIO2_3" : [     'gpmc_oen_ren', 0x094, 2*32+ 3],
   "GPIO2_4" : [         'gpmc_wen', 0x098, 2*32+ 4],
   "GPIO2_5" : [    'gpmc_ben0_cle', 0x09c, 2*32+ 5],
   "GPIO2_6" : [        'lcd_data0', 0x0a0, 2*32+ 6],
   "GPIO2_7" : [        'lcd_data1', 0x0a4, 2*32+ 7],
   "GPIO2_8" : [        'lcd_data2', 0x0a8, 2*32+ 8],
   "GPIO2_9" : [        'lcd_data3', 0x0ac, 2*32+ 9],
  "GPIO2_10" : [        'lcd_data4', 0x0b0, 2*32+10],
  "GPIO2_11" : [        'lcd_data5', 0x0b4, 2*32+11],
  "GPIO2_12" : [        'lcd_data6', 0x0b8, 2*32+12],
  "GPIO2_13" : [        'lcd_data7', 0x0bc, 2*32+13],
  "GPIO2_14" : [        'lcd_data8', 0x0c0, 2*32+14],
  "GPIO2_15" : [        'lcd_data9', 0x0c4, 2*32+15],
  "GPIO2_16" : [       'lcd_data10', 0x0c8, 2*32+16],
  "GPIO2_17" : [       'lcd_data11', 0x0cc, 2*32+17],
  "GPIO2_22" : [        'lcd_vsync', 0x0e0, 2*32+22],
  "GPIO2_23" : [        'lcd_hsync', 0x0e4, 2*32+23],
  "GPIO2_24" : [         'lcd_pclk', 0x0e8, 2*32+24],
  "GPIO2_25" : [   'lcd_ac_bias_en', 0x0ec, 2*32+25],
  "GPIO3_14" : [     'mcasp0_aclkx', 0x190, 3*32+14],
  "GPIO3_15" : [       'mcasp0_fsx', 0x194, 3*32+15],
  "GPIO3_16" : [      'mcasp0_axr0', 0x198, 3*32+16],
  "GPIO3_17" : [    'mcasp0_ahclkr', 0x19c, 3*32+17],
  "GPIO3_19" : [       'mcasp0_fsr', 0x1a4, 3*32+19],
  "GPIO3_21" : [    'mcasp0_ahclkx', 0x1ac, 3*32+21]
}

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


##############################
##--- Start UART config: ---##

# Formatting constants to mimic Arduino's serial.print() formatting:
DEC = 'DEC'
BIN = 'BIN'
OCT = 'OCT'
HEX = 'HEX'

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

##--- End PWM config: ------##
##############################

#
#

from bbio.driver import *

def digitalRead(pin):
  return driver.digitalRead(GPIO[pin])


GPIO = {
      "USR0" : [GPIO1, 1<<21,           'gpmc_a5'],
      "USR1" : [GPIO1, 1<<22,           'gpmc_a6'],
      "USR2" : [GPIO1, 1<<23,           'gpmc_a7'],
      "USR3" : [GPIO1, 1<<24,           'gpmc_a8'],
   "GPIO0_2" : [GPIO0,  1<<2,         'spi0_sclk'],
   "GPIO0_3" : [GPIO0,  1<<3,           'spi0_d0'],
   "GPIO0_4" : [GPIO0,  1<<4,           'spi0_d1'],
   "GPIO0_5" : [GPIO0,  1<<5,          'spi0_cs0'],
   "GPIO0_7" : [GPIO0,  1<<7, 'ecap0_in_pwm0_out'],
   "GPIO0_8" : [GPIO0,  1<<8,        'lcd_data12'],
   "GPIO0_9" : [GPIO0,  1<<9,        'lcd_data13'],
  "GPIO0_10" : [GPIO0, 1<<10,        'lcd_data14'],
  "GPIO0_11" : [GPIO0, 1<<11,        'lcd_data15'],
  "GPIO0_12" : [GPIO0, 1<<12,        'uart1_ctsn'],
  "GPIO0_13" : [GPIO0, 1<<13,        'uart1_rtsn'],
  "GPIO0_14" : [GPIO0, 1<<14,         'uart1_rxd'],
  "GPIO0_15" : [GPIO0, 1<<15,         'uart1_txd'],
  "GPIO0_20" : [GPIO0, 1<<20,  'xdma_event_intr1'],
  "GPIO0_22" : [GPIO0, 1<<22,          'gpmc_ad8'],
  "GPIO0_23" : [GPIO0, 1<<23,          'gpmc_ad9'],
  "GPIO0_26" : [GPIO0, 1<<26,         'gpmc_ad10'],
  "GPIO0_27" : [GPIO0, 1<<27,         'gpmc_ad11'],
  "GPIO0_30" : [GPIO0, 1<<30,        'gpmc_wait0'],
  "GPIO0_31" : [GPIO0, 1<<31,          'gpmc_wpn'],
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
  "GPIO1_18" : [GPIO1, 1<<18,           'gpmc_a2'],
  "GPIO1_19" : [GPIO1, 1<<19,           'gpmc_a3'],
  "GPIO1_28" : [GPIO1, 1<<28,         'gpmc_ben1'],
  "GPIO1_29" : [GPIO1, 1<<29,         'gpmc_csn0'],
  "GPIO1_30" : [GPIO1, 1<<30,         'gpmc_csn1'],
  "GPIO1_31" : [GPIO1, 1<<31,         'gpmc_csn2'],
   "GPIO2_1" : [GPIO2,  1<<1,          'gpmc_clk'],
   "GPIO2_2" : [GPIO2,  1<<2,     'gpmc_advn_ale'],
   "GPIO2_3" : [GPIO2,  1<<3,      'gpmc_oen_ren'],
   "GPIO2_4" : [GPIO2,  1<<4,          'gpmc_wen'],
   "GPIO2_5" : [GPIO2,  1<<5,     'gpmc_ben0_cle'],
   "GPIO2_6" : [GPIO2,  1<<6,         'lcd_data0'],
   "GPIO2_7" : [GPIO2,  1<<7,         'lcd_data1'],
   "GPIO2_8" : [GPIO2,  1<<8,         'lcd_data2'],
   "GPIO2_9" : [GPIO2,  1<<9,         'lcd_data3'],
  "GPIO2_10" : [GPIO2, 1<<10,         'lcd_data4'],
  "GPIO2_11" : [GPIO2, 1<<11,         'lcd_data5'],
  "GPIO2_12" : [GPIO2, 1<<12,         'lcd_data6'],
  "GPIO2_13" : [GPIO2, 1<<13,         'lcd_data7'],
  "GPIO2_14" : [GPIO2, 1<<14,         'lcd_data8'],
  "GPIO2_15" : [GPIO2, 1<<15,         'lcd_data9'],
  "GPIO2_16" : [GPIO2, 1<<16,        'lcd_data10'],
  "GPIO2_17" : [GPIO2, 1<<17,        'lcd_data11'],
  "GPIO2_22" : [GPIO2, 1<<22,         'lcd_vsync'],
  "GPIO2_23" : [GPIO2, 1<<23,         'lcd_hsync'],
  "GPIO2_24" : [GPIO2, 1<<24,          'lcd_pclk'],
  "GPIO2_25" : [GPIO2, 1<<25,    'lcd_ac_bias_en'],
  "GPIO3_14" : [GPIO3, 1<<14,      'mcasp0_aclkx'],
  "GPIO3_15" : [GPIO3, 1<<15,        'mcasp0_fsx'],
  "GPIO3_16" : [GPIO3, 1<<16,       'mcasp0_axr0'],
  "GPIO3_17" : [GPIO3, 1<<17,     'mcasp0_ahclkr'],
  "GPIO3_19" : [GPIO3, 1<<19,        'mcasp0_fsr'],
  "GPIO3_21" : [GPIO3, 1<<21,     'mcasp0_ahclkx']
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



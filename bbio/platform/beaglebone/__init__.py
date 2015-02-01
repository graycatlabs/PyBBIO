# initialization for beaglebone

from gpio import pinMode, digitalWrite, digitalRead, toggle, pinState, \
                 shiftIn, shiftOut
from interrupt import attachInterrupt, detachInterrupt
from adc import analogRead, inVolts
from pwm import analogWrite, pwmFrequency, pwmEnable, pwmDisable
from serial_port import Serial1, Serial2, Serial4, Serial5
from i2c import Wire1, Wire2
from spi import SPI0, SPI1

from config import USR0, USR1, USR2, USR3, GPIO0_2, GPIO0_3, GPIO0_4, GPIO0_5,\
                   GPIO0_7, GPIO0_8, GPIO0_9, GPIO0_10, GPIO0_11, GPIO0_12,\
                   GPIO0_13, GPIO0_14, GPIO0_15, GPIO0_20, GPIO0_22, GPIO0_23,\
                   GPIO0_26, GPIO0_27, GPIO0_30, GPIO0_31, GPIO1_0, GPIO1_1,\
                   GPIO1_2, GPIO1_3, GPIO1_4, GPIO1_5, GPIO1_6, GPIO1_7,\
                   GPIO1_12, GPIO1_13, GPIO1_14, GPIO1_15, GPIO1_16, GPIO1_17,\
                   GPIO1_18, GPIO1_19, GPIO1_28, GPIO1_29, GPIO1_30, GPIO1_31,\
                   GPIO2_1, GPIO2_2, GPIO2_3, GPIO2_4, GPIO2_5, GPIO2_6, GPIO2_7,\
                   GPIO2_8, GPIO2_9, GPIO2_10, GPIO2_11, GPIO2_12, GPIO2_13,\
                   GPIO2_14, GPIO2_15 ,GPIO2_16, GPIO2_17 ,GPIO2_22 ,GPIO2_23,\
                   GPIO2_24, GPIO2_25, GPIO3_14, GPIO3_15, GPIO3_16, GPIO3_17,\
                   GPIO3_19, GPIO3_21
from config import INPUT, OUTPUT, PULLDOWN, NOPULL, PULLUP, HIGH, LOW, RISING,\
                   FALLING, BOTH, MSBFIRST, LSBFIRST

from config import AIN0, AIN1, AIN2, AIN3, AIN4, AIN5, AIN6, AIN7,\
                   A0, A1, A2, A3, A4, A5, A6, A7, VSYS

from config import PWM1A, PWM1B, PWM2A, PWM2B
from config import RES_16BIT, RES_8BIT, PERCENT

from config import ECAP0, ECAP1

from config import DEC, BIN, OCT, HEX

from api import platform_init, platform_cleanup

__all__ = [
  'pinMode', 'digitalWrite', 'digitalRead', 'toggle', 'pinState', 'shiftIn', 
  'shiftOut', 'attachInterrupt', 'detachInterrupt', 
  'analogRead', 'inVolts', 'analogWrite', 
  'pwmFrequency', 'pwmEnable', 'pwmDisable', 
  'Serial1', 'Serial2', 'Serial4', 'Serial5', 
  'Wire1', 'Wire2', 
  'SPI0', 'SPI1', 
  'platform_init', 'platform_cleanup',
  'USR0', 'USR1', 'USR2', 'USR3', 'GPIO0_2', 'GPIO0_3', 'GPIO0_4', 'GPIO0_5', 
  'GPIO0_7', 'GPIO0_8', 'GPIO0_9', 'GPIO0_10', 'GPIO0_11', 'GPIO0_12', 
  'GPIO0_13', 'GPIO0_14', 'GPIO0_15', 'GPIO0_20', 'GPIO0_22', 'GPIO0_23', 
  'GPIO0_26', 'GPIO0_27', 'GPIO0_30', 'GPIO0_31', 'GPIO1_0', 'GPIO1_1',
  'GPIO1_2', 'GPIO1_3', 'GPIO1_4', 'GPIO1_5', 'GPIO1_6', 'GPIO1_7', 'GPIO1_12', 
  'GPIO1_13', 'GPIO1_14', 'GPIO1_15', 'GPIO1_16', 'GPIO1_17', 'GPIO1_18', 
  'GPIO1_19', 'GPIO1_28', 'GPIO1_29', 'GPIO1_30', 'GPIO1_31', 'GPIO2_1', 
  'GPIO2_2', 'GPIO2_3', 'GPIO2_4', 'GPIO2_5', 'GPIO2_6', 'GPIO2_7', 'GPIO2_8', 
  'GPIO2_9', 'GPIO2_10', 'GPIO2_11', 'GPIO2_12', 'GPIO2_13', 'GPIO2_14', 
  'GPIO2_15', 'GPIO2_16', 'GPIO2_17','GPIO2_22', 'GPIO2_23', 'GPIO2_24', 
  'GPIO2_25', 'GPIO3_14', 'GPIO3_15', 'GPIO3_16', 'GPIO3_17', 'GPIO3_19', 
  'GPIO3_21', 'INPUT', 'OUTPUT', 'PULLDOWN', 'NOPULL', 'PULLUP', 'HIGH', 'LOW', 
  'RISING', 'FALLING', 'BOTH', 
  'MSBFIRST', 'LSBFIRST',
  'AIN0', 'AIN1', 'AIN2', 'AIN3', 'AIN4', 'AIN5', 'AIN6', 'AIN7', 'A0', 'A1', 
  'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'VSYS',
  'PWM1A', 'PWM1B', 'PWM2A', 'PWM2B', 'RES_16BIT', 'RES_8BIT', 'PERCENT', 
  'ECAP0', 'ECAP1',
  'DEC', 'BIN', 'OCT', 'HEX',
]
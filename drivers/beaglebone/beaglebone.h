/* beaglebone.h
 * Part of PyBBIO
 * Apache 2.0 License
 * 
 * PyBBIO configuration for Beaglebone driver.
 */

#ifndef _BEAGLEBONE_CONFIG_H
#define _BEAGLEBONE_CONFIG_H


#define MMAP_FILE   "/dev/mem"
#define MMAP_OFFSET 0x44c00000 
#define MMAP_SIZE   (0x48ffffff-MMAP_OFFSET)


/*--- Start PRCM config: ---*/
// Power Management and Clock Module

#define CM_PER  (0x44e00000-MMAP_OFFSET)
#define CM_WKUP (0x44e00400-MMAP_OFFSET)

#define CM_PER_EPWMSS0_CLKCTRL (0xd4+CM_PER)
#define CM_PER_EPWMSS1_CLKCTRL (0xcc+CM_PER)
#define CM_PER_EPWMSS2_CLKCTRL (0xd8+CM_PER)

#define CM_WKUP_ADC_TSC_CLKCTRL (0xbc+CM_WKUP)

#define MODULEMODE_ENABLE (0x02)
#define IDLEST_MASK (0x03<<16)
// To enable module clock:
//   _setReg(CM_WKUP_module_CLKCTRL, MODULEMODE_ENABLE)
//   while (_getReg(CM_WKUP_module_CLKCTRL) & IDLEST_MASK): pass
// To disable module clock:
//   _andReg(CM_WKUP_module_CLKCTRL, ~MODULEMODE_ENABLE)

/*--- End PRCM config ------*/

/*--- Start control module config: ---*/

#define PINMUX_PATH "/sys/kernel/debug/omap_mux/"

#define CONF_SLEW_SLOW    (1<<6)
#define CONF_RX_ACTIVE    (1<<5)
#define CONF_PULLUP       (1<<4)
#define CONF_PULLDOWN     0x00
#define CONF_PULL_DISABLE (1<<3)

#define CONF_GPIO_MODE   0x07 
#define CONF_GPIO_OUTPUT CONF_GPIO_MODE
#define CONF_GPIO_INPUT  (CONF_GPIO_MODE | CONF_RX_ACTIVE)
#define CONF_ADC_PIN     (CONF_RX_ACTIVE | CONF_PULL_DISABLE)

#define CONF_UART_TX     (CONF_PULL_DISABLE)
#define CONF_UART_RX     (CONF_PULLUP | CONF_RX_ACTIVE)

/*--- End control module config ------*/

/*--- Start GPIO config: ---*/
#define GPIO_FILE_BASE "/sys/class/gpio/"
#define EXPORT_FILE    (GPIO_FILE_BASE "export")
#define UNEXPORT_FILE  (GPIO_FILE_BASE "unexport")

#define GPIO0 (0x44e07000-MMAP_OFFSET)
#define GPIO1 (0x4804c000-MMAP_OFFSET)
#define GPIO2 (0x481ac000-MMAP_OFFSET)
#define GPIO3 (0x481ae000-MMAP_OFFSET)

#define GPIO_OE           0x134
#define GPIO_DATAIN       0x138
#define GPIO_DATAOUT      0x13c
#define GPIO_CLEARDATAOUT 0x190
#define GPIO_SETDATAOUT   0x194

// Digital IO keywords:
#define INPUT     1
#define OUTPUT    0
#define HIGH      1
#define LOW       0
#define RISING    1
#define FALLING  -1
#define BOTH      0
#define MSBFIRST  1
#define LSBFIRST -1


#endif

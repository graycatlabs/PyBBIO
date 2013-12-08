# 3.2/uart.py 
# Part of PyBBIO
# github.com/alexanderhiam/PyBBIO
# Apache 2.0 license
# 
# Beaglebone pinmux driver
# For Beaglebones with 3.2 kernel

from config import UART, CONF_UART_TX, CONF_UART_RX
import pinmux


def uartInit(uart):
  """ Muxes given serial port's header pins for use. Returns True
      if successful, False otherwise. """
  tx_pinmux_filename = UART[self.config][1]
  tx_pinmux_mode     = UART[self.config][2] | CONF_UART_TX
  pinmux.pinMux(tx_pinmux_filename, tx_pinmux_mode)

  rx_pinmux_filename = UART[self.config][3]
  rx_pinmux_mode     = UART[self.config][4] | CONF_UART_RX
  pinmux.pinMux(rx_pinmux_filename, rx_pinmux_mode)    
  # Not catching errors for now, not sure what could go wrong here...
  return True
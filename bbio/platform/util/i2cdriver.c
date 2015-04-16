 /* i2cdriver.c
 *
 * Copyright (c) 2015 - Gray Cat Labs
 * Alexander Hiam <alex@graycat.io>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <stdint.h>
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <linux/i2c-dev.h>
#include "i2cdriver.h"

#define I2C_PATH_LEN   20 // > "/dev/i2c-N"

int I2C_open(uint8_t bus) {
  char device[I2C_PATH_LEN];
  sprintf(device, "/dev/i2c-%d", bus);
  return open(device, O_RDWR, 0);
}

void I2C_close(int i2c_fd) {
  close(i2c_fd);
}

int I2C_enable10BitAddressing(int i2c_fd) {
  int ret;
  ret = ioctl(i2c_fd, I2C_TENBIT, 1);
  if (ret < 0) return ret;
  return 0;
}

int I2C_disable10BitAddressing(int i2c_fd) {
  int ret;
  ret = ioctl(i2c_fd, I2C_TENBIT, 0);
  if (ret < 0) return ret;
  return 0;
}

int setSlaveAddress(int i2c_fd, int addr) {
  int ret;
  ret = ioctl(i2c_fd, I2C_SLAVE, addr);
  if (ret < 0) return ret;
  return 0;
}

int I2C_read(int i2c_fd, void *rx_buffer, int n_bytes) {
  int ret;
  ret = read(i2c_fd, rx_buffer, n_bytes);
  if (ret < 0) return ret;
  return 0;
}

int I2C_readTransaction(int i2c_fd, uint8_t command, void *rx_buffer, 
                        int n_bytes) {
  int ret;
  ret = write(i2c_fd, &command, 1);
  if (ret < 0) return ret;

  ret = read(i2c_fd, rx_buffer, n_bytes);
  if (ret < 0) return ret;
  return 0;
}

int I2C_write(int i2c_fd, void *tx_buffer, int n_bytes) {
  int ret;
  ret = write(i2c_fd, tx_buffer, n_bytes);
  if (ret < 0) return ret;
  return 0;
}
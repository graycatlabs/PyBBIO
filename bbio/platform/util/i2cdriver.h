/* i2cdriver.h
 *
 * A very slim driver for controlling Linux I2C interfaces. Requires an I2C
 * Kernel driver be loaded to expose /dev/i2c-N interfaces which provide 
 * the standard Linux I2C ioctls. This is really just an ioctl wrapper.
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

#ifndef _I2C_DRIVER_H_
#define _I2C_DRIVER_H_

#include <stdint.h>

/**
 * @brief Opens the /dev/i2c-[bus] interface.
 *
 * @param bus I2C bus number
 * @return Returns the file descriptor for the I2C bus.
 */
int I2C_open(uint8_t bus);

/**
 * @brief Closes the given I2C interface.
 *
 * @param i2c_fd I2C bus file descriptor to close
 */
void I2C_close(int i2c_fd);

/**
 * @brief Enables 10-bit addressing the given I2C interface.
 *
 * @param i2c_fd I2C file descriptor
 * @return Returns 0 if successful, ioctl error code otherwise
 */
int I2C_enable10BitAddressing(int i2c_fd);

/**
 * @brief Disables 10-bit addressing the given I2C interface.
 *
 * @param i2c_fd I2C file descriptor
 * @return Returns 0 if successful, ioctl error code otherwise
 */
int I2C_disable10BitAddressing(int i2c_fd);

/**
 * @brief Reads a block from the given I2C interface.
 *
 * Reads n_bytes reads n_bytes from the current slave address on the given I2C 
 * interface. and puts them into the given 
 * buffer.
 * @param i2c_fd I2C file descriptor
 * @param rx_buffer pointer to an array, already initialized to the required size
 * @return Returns 0 if successful, ioctl error code otherwise
 */
int setSlaveAddress(int i2c_fd, int addr);

/**
 * @brief Reads a block from the given I2C interface.
 *
 * Reads n_bytes reads n_bytes from the current slave address on the given I2C 
 * interface. and puts them into the given 
 * buffer.
 * @param i2c_fd I2C file descriptor
 * @param rx_buffer pointer to an array, already initialized to the required size
 * @return Returns 0 if successful, file access error code otherwise
 */
int I2C_read(int i2c_fd, void *rx_buffer, int n_bytes);

/**
 * @brief Writes the given command then reads a block from the given I2C 
 * interface.
 *
 * Writes the given byte, then immediately reads n_bytes bytes from the current
 * slave address on the given I2C interface.
 * @param rx_buffer pointer to an array, already initialized to the required size
 * @return Returns 0 if successful, file access error code otherwise
 */
int I2C_readTransaction(int i2c_fd, uint8_t byte, void *rx_buffer, int n_bytes);

/**
 * @brief Writes a block to the given I2C interface.
 *
 * Writes n_bytes bytes from the given buffer to the current slave address on 
 * the given I2C interface.
 * @param i2c_fd I2C file descriptor
 * @param tx_buffer pointer to an array containing the words to be transmitted
 * @return Returns 0 if successful, file access error code otherwise
 */
int I2C_write(int i2c_fd, void *tx_buffer, int n_bytes);

#endif
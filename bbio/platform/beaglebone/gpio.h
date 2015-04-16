/* gpio.h
 *
 * Provides Python functions for GPIO, as well as a C API which can be used
 * in other C extensions.
 *
 * Part of PyBBIO - https://github.com/graycatlabs/PyBBIO
 * Copyright (c) 2014 - Alexander Hiam <alex@graycat.io>
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

#ifndef _PyBBIO_GPIO_H_
#define _PyBBIO_GPIO_H_

#include "Python.h"
#include <stdint.h>

#define CONF_SLEW_SLOW    (1<<6)
#define CONF_RX_ACTIVE    (1<<5)
#define CONF_PULLUP       (1<<4)
#define CONF_PULLDOWN     (0x00)
#define CONF_PULL_DISABLE (1<<3)

#define CONF_GPIO_MODE   (0x07)
#define CONF_GPIO_OUTPUT (CONF_GPIO_MODE)
#define CONF_GPIO_INPUT  (CONF_GPIO_MODE | CONF_RX_ACTIVE)
#define CONF_ADC_PIN     (CONF_RX_ACTIVE | CONF_PULL_DISABLE)

#define INPUT     1
#define OUTPUT    0
#define PULLDOWN -1
#define NOPULL    0
#define PULLUP    1
#define HIGH      1
#define LOW       0
#define RISING    1
#define FALLING  -1
#define BOTH      0
#define MSBFIRST  1
#define LSBFIRST -1

// Highest GPIO number by kernel numbering is GPIO3_31 = 3*32 + 31
#define MAX_GPIO_NUM 127

#define EXCEPTION_STRING_LEN 256
#define STATE_STR_BUFFER_LEN 16

// Defines for the Capsule C API:
#define PyGPIO_pinMode_NUM 0
#define PyGPIO_pinMode_RETURN void
#define PyGPIO_pinMode_PROTO (const char *gpio_pin, int direction, int pull, \
                              int preserve_mode_on_exit)

#define PyGPIO_digitalRead_NUM 1
#define PyGPIO_digitalRead_RETURN int
#define PyGPIO_digitalRead_PROTO (const char *gpio_pin)

#define PyGPIO_digitalWrite_NUM 2
#define PyGPIO_digitalWrite_RETURN void
#define PyGPIO_digitalWrite_PROTO (const char *gpio_pin, int state)

#define PyGPIO_toggle_NUM 3
#define PyGPIO_toggle_RETURN void
#define PyGPIO_toggle_PROTO (const char *gpio_pin)

#define PyGPIO_pinState_NUM 4
#define PyGPIO_pinState_RETURN int
#define PyGPIO_pinState_PROTO (const char *gpio_pin)

#define PyGPIO_shiftIn_NUM 5
#define PyGPIO_shiftIn_RETURN void
#define PyGPIO_shiftIn_PROTO (const char *data_pin, const char *clk_pin, \
                               int bit_order, char *data, int n_bytes, int edge)

#define PyGPIO_shiftOut_NUM 6
#define PyGPIO_shiftOut_RETURN void
#define PyGPIO_shiftOut_PROTO (const char *data_pin, const char *clk_pin, \
                               int bit_order, const char *data, int n_bytes, \
                               int edge)

#define PyGPIO_getGPIONum_NUM 7
#define PyGPIO_getGPIONum_RETURN int
#define PyGPIO_getGPIONum_PROTO (const char *gpio_pin)

#define PyGPIO_getStateFile_NUM 8
#define PyGPIO_getStateFile_RETURN FILE*
#define PyGPIO_getStateFile_PROTO (const char *gpio_pin)

#define PyGPIO_getStateFileLock_NUM 9
#define PyGPIO_getStateFileLock_RETURN FILE*
#define PyGPIO_getStateFileLock_PROTO (const char *gpio_pin)

#define PyGPIO_unlockStateFile_NUM 10
#define PyGPIO_unlockStateFile_RETURN void
#define PyGPIO_unlockStateFile_PROTO (const char *gpio_pin)
/* Total number of C API pointers */
#define PyGPIO_API_pointers 11


#ifdef _GPIO_MODULE_

static PyGPIO_pinMode_RETURN PyGPIO_pinMode PyGPIO_pinMode_PROTO;
static PyGPIO_digitalRead_RETURN PyGPIO_digitalRead PyGPIO_digitalRead_PROTO;
static PyGPIO_digitalWrite_RETURN PyGPIO_digitalWrite PyGPIO_digitalWrite_PROTO;
static PyGPIO_toggle_RETURN PyGPIO_toggle PyGPIO_toggle_PROTO;
static PyGPIO_pinState_RETURN PyGPIO_pinState PyGPIO_pinState_PROTO;
static PyGPIO_shiftIn_RETURN PyGPIO_shiftIn PyGPIO_shiftIn_PROTO;
static PyGPIO_shiftOut_RETURN PyGPIO_shiftOut PyGPIO_shiftOut_PROTO;
static PyGPIO_getGPIONum_RETURN PyGPIO_getGPIONum PyGPIO_getGPIONum_PROTO;
static PyGPIO_getStateFile_RETURN PyGPIO_getStateFile PyGPIO_getStateFile_PROTO;
static PyGPIO_getStateFileLock_RETURN PyGPIO_getStateFileLock PyGPIO_getStateFileLock_PROTO;
static PyGPIO_unlockStateFile_RETURN PyGPIO_unlockStateFile PyGPIO_unlockStateFile_PROTO;

#else

static void **PyGPIO_API;

#define PyGPIO_pinMode \
 (*(PyGPIO_pinMode_RETURN (*)PyGPIO_pinMode_PROTO) \
 PyGPIO_API[PyGPIO_pinMode_NUM])
 
#define PyGPIO_digitalRead \
 (*(PyGPIO_digitalRead_RETURN (*)PyGPIO_digitalRead_PROTO) \
 PyGPIO_API[PyGPIO_digitalRead_NUM])
 
#define PyGPIO_digitalWrite \
 (*(PyGPIO_digitalWrite_RETURN (*)PyGPIO_digitalWrite_PROTO) \
 PyGPIO_API[PyGPIO_digitalWrite_NUM])
 
#define PyGPIO_toggle \
 (*(PyGPIO_toggle_RETURN (*)PyGPIO_toggle_PROTO) \
 PyGPIO_API[PyGPIO_toggle_NUM])

#define PyGPIO_pinState \
 (*(PyGPIO_pinState_RETURN (*)PyGPIO_pinState_PROTO) \
 PyGPIO_API[PyGPIO_pinState_NUM])
 
#define PyGPIO_shiftIn \
 (*(PyGPIO_shiftIn_RETURN (*)PyGPIO_shiftIn_PROTO) \
 PyGPIO_API[PyGPIO_shiftIn_NUM])

#define PyGPIO_shiftOut \
 (*(PyGPIO_shiftOut_RETURN (*)PyGPIO_shiftOut_PROTO) \
 PyGPIO_API[PyGPIO_shiftOut_NUM])
 
#define PyGPIO_getGPIONum \
 (*(PyGPIO_getGPIONum_RETURN (*)PyGPIO_getGPIONum_PROTO) \
 PyGPIO_API[PyGPIO_getGPIONum_NUM])
 
#define PyGPIO_getStateFile \
 (*(PyGPIO_getStateFile_RETURN (*)PyGPIO_getStateFile_PROTO) \
 PyGPIO_API[PyGPIO_getStateFile_NUM])
 
#define PyGPIO_getStateFileLock \
 (*(PyGPIO_getStateFileLock_RETURN (*)PyGPIO_getStateFileLock_PROTO) \
 PyGPIO_API[PyGPIO_getStateFileLock_NUM])
 
#define PyGPIO_unlockStateFile \
 (*(PyGPIO_unlockStateFile_RETURN (*)PyGPIO_unlockStateFile_PROTO) \
 PyGPIO_API[PyGPIO_unlockStateFile_NUM])

static int import_gpio(void) {
    PyGPIO_API = (void **)PyCapsule_Import("bbio.platform.beaglebone.gpio._GPIO_C_API", 0);
    return (PyGPIO_API != NULL) ? 0 : -1;
}

#endif // _GPIO_MODULE_

#endif // _PyBBIO_GPIO_H_
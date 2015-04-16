/* gpio.c
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

#include "Python.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include "sysfs.h"

#define _GPIO_MODULE_
#include "gpio.h"

static PyObject *_config_module_dict;
static PyObject *_gpio_dict;
static PyObject *_pinmux_module_dict;
static PyObject *_common_module_dict;
static FILE *_state_files[MAX_GPIO_NUM];
static uint8_t _state_file_locks[MAX_GPIO_NUM];


/* PyGPIO_pinMode
 * C API function - sets the pinMode of the given pin.
 *
 * @gpio_pin: pin to set, e.g. "GPIO1_28"
 * @direction: INPUT or OUTPUT
 * @direction: INPUT or OUTPUT
 * @pull: PULLDOWN, PULLUP or NOPULL
 * @preserve_mode_on_exit: 1 to leave setting pinMux when program exits, 
 *                         0 to undo it.
 */
static void PyGPIO_pinMode(const char *gpio_pin, int direction, int pull, 
                           int preserve_mode_on_exit) {
  PyObject *export, *exported;
  PyObject *pinMux;
  PyObject *pin_dict, *direction_file_obj;
  char *direction_file;
  FILE *direction_fd;
  int pull_config;
    
  export = PyDict_GetItemString(_pinmux_module_dict, "export");
  exported = PyEval_CallFunction(export, "si", gpio_pin, 
                                 !preserve_mode_on_exit);
  if (!exported || !PyBool_Check(exported)) {
    printf("warning: could not export pin '%s', skipping pinMode()", gpio_pin);
  }
  pin_dict = PyDict_GetItemString(_gpio_dict, gpio_pin);
  direction_file_obj = PyDict_GetItemString(pin_dict, "direction_file");
  direction_file = PyString_AsString(direction_file_obj);
  
  pinMux = PyDict_GetItemString(_pinmux_module_dict, "pinMux");
  
  direction_fd = fopen(direction_file, "w");
  if(!direction_fd) return; 
  
  if (direction == INPUT) {
    pull_config = CONF_GPIO_INPUT;
    if (pull > 0) pull_config |= CONF_PULLUP;
    else if (pull < 0) pull_config |= CONF_PULLDOWN;
    else pull_config |= CONF_PULL_DISABLE;
    
    PyEval_CallFunction(pinMux, "sii", gpio_pin, pull_config, 
                        preserve_mode_on_exit);
    fprintf(direction_fd, "in");
  }
  else {
    PyEval_CallFunction(pinMux, "sii", gpio_pin, CONF_GPIO_OUTPUT, 
                        preserve_mode_on_exit);
    fprintf(direction_fd, "out");
  }
  fclose(direction_fd);
}

/* pinMode
 * Python function for setting the pinMode of a pin.
 */
static PyObject *pinMode(PyObject *self, PyObject *args) {
  const char *gpio_pin;
  char error_msg[EXCEPTION_STRING_LEN];
  int direction, pull, preserve_mode_on_exit;
  PyObject *gpio_pin_obj;
  pull = 0;
  preserve_mode_on_exit = 0;
  if(!PyArg_ParseTuple(args, "si|ii", &gpio_pin, &direction, &pull, 
                        &preserve_mode_on_exit)) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  gpio_pin_obj = PyString_FromString(gpio_pin);
  if (!PyDict_Contains(_gpio_dict, gpio_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", gpio_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(gpio_pin_obj);
    return NULL;
  }
  PyGPIO_pinMode(gpio_pin, direction, pull, preserve_mode_on_exit);
  Py_DECREF(gpio_pin_obj);
  Py_INCREF(Py_None);
  return Py_None;
}

/* PyGPIO_digitalRead
 * C API function - read and return the current state of a pin.
 *
 * @gpio_pin: pin to read, e.g. "GPIO1_28"
 *
 * Returns either HIGH or LOW.
 */
static int PyGPIO_digitalRead(const char *gpio_pin) {
  FILE *state_fd;
  char state_str[STATE_STR_BUFFER_LEN];
  
  state_fd = PyGPIO_getStateFile(gpio_pin);
  if(!state_fd) return -1;
  rewind(state_fd);
  fgets(state_str, STATE_STR_BUFFER_LEN, state_fd);
  fflush(state_fd);
  return atoi(state_str);
}

/* digitalRead
 * Python function to read and return the current state of a pin.
 */
static PyObject *digitalRead(PyObject *self, PyObject *args) {\
  const char *gpio_pin;
  char error_msg[EXCEPTION_STRING_LEN];
  PyObject *gpio_pin_obj;
  
  if(!PyArg_ParseTuple(args, "s", &gpio_pin)) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  gpio_pin_obj = PyString_FromString(gpio_pin);
  if (!PyDict_Contains(_gpio_dict, gpio_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", gpio_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(gpio_pin_obj);
    return NULL;
  }
  Py_DECREF(gpio_pin_obj);
  return Py_BuildValue("i", PyGPIO_digitalRead(gpio_pin));
}

/* PyGPIO_digitalWrite
 * C API function - set the state of a pin.
 *
 * @gpio_pin: pin to set, e.g. "GPIO1_28"
 * @state: the state to set it to, either HIGH or LOW
 */
static void PyGPIO_digitalWrite(const char *gpio_pin, int state) {
  FILE *state_fd;
  char state_str[STATE_STR_BUFFER_LEN];
  state_fd = PyGPIO_getStateFile(gpio_pin);
  if(!state_fd) return;
  fseek(state_fd, 0, SEEK_SET);
  snprintf(state_str, STATE_STR_BUFFER_LEN, "%i", state);
  fprintf(state_fd, "%s", state_str);
  fflush(state_fd);
}

/* digitalWrite
 * Python function to set the state of a pin.
 */
static PyObject *digitalWrite(PyObject *self, PyObject *args) {
  const char *gpio_pin;
  int state;
  char error_msg[EXCEPTION_STRING_LEN];
  PyObject *gpio_pin_obj;
  if(!PyArg_ParseTuple(args, "si", &gpio_pin, &state)) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  gpio_pin_obj = PyString_FromString(gpio_pin);
  if (!PyDict_Contains(_gpio_dict, gpio_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", gpio_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(gpio_pin_obj);
    return NULL;
  }
  PyGPIO_digitalWrite(gpio_pin, state);
  Py_DECREF(gpio_pin_obj);
  Py_INCREF(Py_None);
  return Py_None;
}

/* PyGPIO_toggle
 * C API function - toggle the state of a pin.
 *
 * @gpio_pin: pin to toggle, e.g. "GPIO1_28"
 */
static void PyGPIO_toggle(const char *gpio_pin) {
  FILE *state_fd;
  int state;
  char state_str[STATE_STR_BUFFER_LEN];
 
  state_fd = PyGPIO_getStateFile(gpio_pin);
  if(!state_fd) return;
  fseek(state_fd, 0, SEEK_SET);
  
  fgets(state_str, STATE_STR_BUFFER_LEN, state_fd);
  state = atoi(state_str);
  snprintf(state_str, STATE_STR_BUFFER_LEN, "%i", state^1);
  fseek(state_fd, 0, SEEK_SET);
  fprintf(state_fd, "%s", state_str);
  fflush(state_fd);
}

/* toggle
 * Python function to toggle the state of a pin.
 */
static PyObject *toggle(PyObject *self, PyObject *args) {
  const char *gpio_pin;
  char error_msg[EXCEPTION_STRING_LEN];
  PyObject *gpio_pin_obj;
  if(!PyArg_ParseTuple(args, "s", &gpio_pin)) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  gpio_pin_obj = PyString_FromString(gpio_pin);
  if (!PyDict_Contains(_gpio_dict, gpio_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", gpio_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(gpio_pin_obj);
    return NULL;
  }
  PyGPIO_toggle(gpio_pin);
  Py_DECREF(gpio_pin_obj);
  Py_INCREF(Py_None);
  return Py_None;
}

/* PyGPIO_pinState
 * C API function - return the current state of the given output pin.
 *
 * @gpio_pin: pin to read, e.g. "GPIO1_28"
 */
static int PyGPIO_pinState(const char *gpio_pin) {
  return PyGPIO_digitalRead(gpio_pin);
}

/* pinState
 * Python function to return the current state of the given output pin.
 */
static PyObject *pinState(PyObject *self, PyObject *args) {
  const char *gpio_pin;
  char error_msg[EXCEPTION_STRING_LEN];
  PyObject *gpio_pin_obj;
  if(!PyArg_ParseTuple(args, "s", &gpio_pin)) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  gpio_pin_obj = PyString_FromString(gpio_pin);
  if (!PyDict_Contains(_gpio_dict, gpio_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", gpio_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(gpio_pin_obj);
    return NULL;
  }
  Py_DECREF(gpio_pin_obj);
  return Py_BuildValue("i", PyGPIO_pinState(gpio_pin));
}

/* PyGPIO_shiftIn
 * C API function - perform a bitbanged SPI read.
 *
 * @data_pin: pin to read the data on (MISO)
 * @clk_pin: pin to use for the clock signal (SCK)
 * @bit_order: order to pack the received bits into each byte, either MSBFIRST
 *             orLSBFIRST. 
 * @data: a pointer to the char array where the data will be put. Must have 
 *        allocated been allocated for a length of at least n_bytes.
 * @n_bytes: the number of bytes to receive.
 * @edge: the clock edge on which the bits are clocked out by the remote device,
 *        either RISING or FALLING.
 */
static void PyGPIO_shiftIn(const char *data_pin, const char *clk_pin, 
                           int bit_order, char *data, int n_bytes, int edge) {
  uint32_t byte;
  uint8_t bit, state;
  PyGPIO_digitalWrite(clk_pin, (edge == FALLING) ? HIGH : LOW);
  for (byte=0; byte<n_bytes; byte++) {
    data[byte] = 0;
    for (bit=0; bit<8; bit++) {
      PyGPIO_digitalWrite(clk_pin, (edge == FALLING) ? LOW : HIGH);
      PyGPIO_digitalWrite(clk_pin, (edge == FALLING) ? HIGH : LOW);
      state = PyGPIO_digitalRead(data_pin);
      if (bit_order == MSBFIRST) data[byte] |= (state << (7-bit));
      else data[byte] |= (state << bit);
    }
  }
}

/* shiftIn
 * Python function to perform a bitbanged SPI read.
 */
static PyObject *shiftIn(PyObject *self, PyObject *args) {
  const char *data_pin, *clk_pin;
  int bit_order, edge, n_bytes;
  char data[n_bytes];
  char error_msg[EXCEPTION_STRING_LEN];
  PyObject *data_pin_obj, *clk_pin_obj;
  n_bytes = 1;
  edge = FALLING;
  if(!PyArg_ParseTuple(args, "ssi|ii", &data_pin, &clk_pin, &bit_order, 
                       &n_bytes, &edge)) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  data_pin_obj = PyString_FromString(data_pin);
  if (!PyDict_Contains(_gpio_dict, data_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", data_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(data_pin_obj);
    return NULL;
  }
  Py_DECREF(data_pin_obj);
  clk_pin_obj = PyString_FromString(clk_pin);
  if (!PyDict_Contains(_gpio_dict, clk_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", clk_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(clk_pin_obj);
    return NULL;
  }
  Py_DECREF(clk_pin_obj);
  PyGPIO_shiftIn(data_pin, clk_pin, bit_order, data, n_bytes, edge);

  return Py_BuildValue("s#", data, n_bytes);
}

/* PyGPIO_shiftOut
 * C API function - perform a bitbanged SPI transmission of the given data.
 *
 * @data_pin: pin to use for the clock signal (SCK)
 * @clk_pin: pin on which to transmit the data (MOSI)
 * @bit_order: order to transmit the bits of each byte, either MSBFIRST or
 *             LSBFIRST. Note the bytes will always be transmitted 
 *             left-to-right.
 * @data: a pointer to a char array of data to transmit.
 * @n_bytes: the number of bytes to transmit from data.
 * @edge: the clock edge on which the bits are read by the remote device,
 *        either RISING or FALLING.
 */
static void PyGPIO_shiftOut(const char *data_pin, const char *clk_pin, 
                            int bit_order, const char *data, int n_bytes, 
                            int edge) {
  uint32_t byte;
  uint8_t bit, state;
  PyGPIO_digitalWrite(clk_pin, (edge == FALLING) ? HIGH : LOW);
  for (byte=0; byte<n_bytes; byte++) {
    for (bit=0; bit<8; bit++) {
      if (bit_order == MSBFIRST) state = 0x1 & (data[byte] >> (7-bit));
      else state = 0x1 & (data[byte] >> bit);
      PyGPIO_digitalWrite(data_pin, state);
      
      PyGPIO_digitalWrite(clk_pin, (edge == FALLING) ? LOW : HIGH);
      PyGPIO_digitalWrite(clk_pin, (edge == FALLING) ? HIGH : LOW);
    }
  }
}

/* shiftOut
 * Python function to perform a bitbanged SPI transmission of the given data.
 */
static PyObject *shiftOut(PyObject *self, PyObject *args) {
  const char *data_pin, *clk_pin, *data;
  int bit_order, edge;
  Py_ssize_t n_bytes;
  char error_msg[EXCEPTION_STRING_LEN];
  PyObject *data_pin_obj, *clk_pin_obj;
  edge = FALLING;
  if(!PyArg_ParseTuple(args, "ssis#|i", &data_pin, &clk_pin, &bit_order, &data, 
                       &n_bytes, &edge)) {
    Py_INCREF(Py_None);
    return Py_None;
  }
  data_pin_obj = PyString_FromString(data_pin);
  if (!PyDict_Contains(_gpio_dict, data_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", data_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(data_pin_obj);
    return NULL;
  }
  Py_DECREF(data_pin_obj);
  clk_pin_obj = PyString_FromString(clk_pin);
  if (!PyDict_Contains(_gpio_dict, clk_pin_obj)) {
    snprintf(error_msg, EXCEPTION_STRING_LEN, "Invalid GPIO pin: %s", clk_pin);
    PyErr_SetString(PyExc_ValueError, error_msg);
    Py_DECREF(clk_pin_obj);
    return NULL;
  }
  Py_DECREF(clk_pin_obj);
  PyGPIO_shiftOut(data_pin, clk_pin, bit_order, data, (int) n_bytes, edge);  
  Py_INCREF(Py_None);
  return Py_None;
}

/* PyGPIO_getGPIONum
 * C API function - get the kernel driver's GPIO number for the given
 * pin. Typically only for internal use.
 *
 * @gpio_pin: pin to calculate the driver number for, e.g. "GPIO1_28"
 *
 * Returns the driver GPIO number in an int. 
 */
static int PyGPIO_getGPIONum(const char *gpio_pin) {
  PyObject *pin_dict, *gpio_num_obj;
  long gpio_num;
  pin_dict = PyDict_GetItemString(_gpio_dict, gpio_pin);
  if (!pin_dict) return -1;
  gpio_num_obj = PyDict_GetItemString(pin_dict, "gpio_num");
  gpio_num = PyInt_AsLong(gpio_num_obj);
  return gpio_num;
}

/* PyGPIO_getStateFile
 * C API function - open the state file for the given GPIO pin and return the
 * open file descriptor. The file will remain open until the program exits.
 *
 * @gpio_pin: pin whose file will be opened, e.g. "GPIO1_28"
 *
 * Returns the open file descriptor if successful, null pointer otherwise. 
 */
static FILE *PyGPIO_getStateFile(const char *gpio_pin) {
  PyObject *pin_dict, *state_file_obj;
  char *state_file;
  long gpio_num;
  pin_dict = PyDict_GetItemString(_gpio_dict, gpio_pin);
  gpio_num = PyGPIO_getGPIONum(gpio_pin);
  if (gpio_num < 0) return NULL;
  if (_state_file_locks[gpio_num]) {
    // File descriptor is locked
    return NULL;
  }
  if (_state_files[gpio_num] <= 0) {
    state_file_obj = PyDict_GetItemString(pin_dict, "state_file");
    state_file = PyString_AsString(state_file_obj);
    _state_files[gpio_num] = fopen(state_file, "r+");
    if(!_state_files[gpio_num]) {
      _state_files[gpio_num] = 0;
      return NULL;
    }
  }
  return _state_files[gpio_num];
}

/* PyGPIO_getStateFileLock
 * C API function - same as PyGPIO_getStateFile, but locks the file descriptor
 * so subsequent calls to get the same descriptor will fail until it is 
 * unlocked with PyGPIO_unlockStateFile(). This is useful when using a GPIO pin
 * if a thread not created by Python.
 *
 * @gpio_pin: pin whose file will be opened, e.g. "GPIO1_28"
 *
 * Returns the open file descriptor if successful, null pointer otherwise. 
 */
static FILE *PyGPIO_getStateFileLock(const char *gpio_pin) {
  PyObject *pin_dict, *state_file_obj;
  char *state_file;
  long gpio_num;
  pin_dict = PyDict_GetItemString(_gpio_dict, gpio_pin);
  gpio_num = PyGPIO_getGPIONum(gpio_pin);
  if (gpio_num < 0) return NULL;
  if (_state_file_locks[gpio_num]) {
    // File descriptor is already locked
    return NULL;
  }
  // Lock the file before getting the file descriptor to avoid race condition:
  _state_file_locks[gpio_num] = 1;
  if (_state_files[gpio_num] <= 0) {
    state_file_obj = PyDict_GetItemString(pin_dict, "state_file");
    state_file = PyString_AsString(state_file_obj);
    _state_files[gpio_num] = fopen(state_file, "r+");
    if(!_state_files[gpio_num]) {
      // Couldn't open the file, should probably raise an error here...
      _state_file_locks[gpio_num] = 0;
      _state_files[gpio_num] = 0;
      return NULL;
    }
  }
  return _state_files[gpio_num];
}

/* PyGPIO_unlockStateFile
 * C API function - unlock a file descriptor that had previously been locked 
 * with PyGPIO_getStateFileLock. 
 *
 * @gpio_pin: pin whose file descriptor will be unlocked, e.g. "GPIO1_28"
 */
static void PyGPIO_unlockStateFile(const char *gpio_pin) {
  long gpio_num;
  gpio_num = PyGPIO_getGPIONum(gpio_pin);
  if (gpio_num < 0) return;
  _state_file_locks[gpio_num] = 0;
}

/* gpioCleanup
 * Called automatically when a PyBBIO program exits to perform cleanup.
 */
static PyObject *gpioCleanup(PyObject *self, PyObject *args) {
  Py_ssize_t i;
  for (i=0; i<MAX_GPIO_NUM; i++) {
    if (_state_files[i] > 0) fclose(_state_files[i]);
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static PyMethodDef gpioMethods[]= {
	{ "pinMode", pinMode, METH_VARARGS, "" },
  { "digitalRead", digitalRead, METH_VARARGS, "" },
  { "digitalWrite", digitalWrite, METH_VARARGS, "" },
  { "toggle", toggle, METH_VARARGS, "" },
  { "pinState", pinState, METH_VARARGS, "" },
  { "shiftIn", shiftIn, METH_VARARGS, "" },
  { "shiftOut", shiftOut, METH_VARARGS, "" },
  { "gpioCleanup", gpioCleanup, METH_VARARGS, "" },
	{ NULL, NULL },
};

PyMODINIT_FUNC initgpio(void) {
  PyObject *m, *c_api_object;
  PyObject *config_module, *pinmux_module, *common_module;
  static void *PyGPIO_API[PyGPIO_API_pointers];
  int i;
  
  m = Py_InitModule("gpio", gpioMethods);
  if (m == NULL) return;

  /* Initialize the C API pointer array */
  PyGPIO_API[PyGPIO_pinMode_NUM] = (void *)PyGPIO_pinMode;
  PyGPIO_API[PyGPIO_digitalRead_NUM] = (void *)PyGPIO_digitalRead;
  PyGPIO_API[PyGPIO_digitalWrite_NUM] = (void *)PyGPIO_digitalWrite;
  PyGPIO_API[PyGPIO_toggle_NUM] = (void *)PyGPIO_toggle;
  PyGPIO_API[PyGPIO_pinState_NUM] = (void *)PyGPIO_pinState;
  PyGPIO_API[PyGPIO_shiftIn_NUM] = (void *)PyGPIO_shiftIn;
  PyGPIO_API[PyGPIO_shiftOut_NUM] = (void *)PyGPIO_shiftOut;
  PyGPIO_API[PyGPIO_getGPIONum_NUM] = (void *)PyGPIO_getGPIONum;
  PyGPIO_API[PyGPIO_getStateFile_NUM] = (void *)PyGPIO_getStateFile;
  PyGPIO_API[PyGPIO_getStateFileLock_NUM] = (void *)PyGPIO_getStateFileLock;
  PyGPIO_API[PyGPIO_unlockStateFile_NUM] = (void *)PyGPIO_unlockStateFile;
  
  /* Create a Capsule containing the API pointer array's address */
  c_api_object = PyCapsule_New((void *)PyGPIO_API, "bbio.platform.beaglebone.gpio._GPIO_C_API", NULL);
  
  if (c_api_object != NULL) PyModule_AddObject(m, "_GPIO_C_API", c_api_object);

  config_module = PyImport_ImportModule("bbio.platform.beaglebone.config");
  _config_module_dict = PyModule_GetDict(config_module);
  _gpio_dict = PyDict_GetItemString(_config_module_dict, "GPIO");

  pinmux_module = PyImport_ImportModule("bbio.platform.beaglebone.pinmux");
  _pinmux_module_dict = PyModule_GetDict(pinmux_module);
  
  common_module = PyImport_ImportModule("bbio.common");
  _common_module_dict = PyModule_GetDict(common_module);
  
  for (i=0; i<MAX_GPIO_NUM; i++) {
    _state_files[i] = 0;
    _state_file_locks[i] = 0;
  }
}
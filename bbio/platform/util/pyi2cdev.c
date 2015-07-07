/* pyi2cdev.c
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

#include "Python.h"
#include <stdint.h>
 #include <stdio.h>
 #include "i2cdriver.h"

PyDoc_STRVAR(I2CDev_module__doc__,
  "This module provides the I2CDev class for controlling I2C interfaces on\n"
  "Linux platforms. The appropriated Linux kernel drivers for your platform\n"
  "must already be loaded to provide a /dev/i2c-N interface to control.\n"
  "To control /dev/i2c-0 you would instantiate with I2CDev(0).");

 typedef struct {
   PyObject_HEAD
   int i2c_fd;
   int slave_addr;
   uint8_t bus_num;
} I2CDev;


static PyObject *I2CDev_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
  I2CDev *self;
  self = (I2CDev *)type->tp_alloc(type, 0);
  return (PyObject *)self;
}

static void I2CDev_dealloc(I2CDev *self) {
  self->ob_type->tp_free((PyObject*)self);
}

static PyObject *I2CDev_init(I2CDev *self, PyObject *args, PyObject *kwds) {
  uint8_t bus;
  if(!PyArg_ParseTuple(args, "b", &bus)) {
    return NULL;
  }
  self->bus_num = bus;
  self->i2c_fd = 0;
  self->slave_addr = -1;
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(I2CDev_open__doc__,
  "I2CDev.open(use_10bit_address=False) -> None\n\n"
  "Initialize the I2C bus interface.\n"
  "If use_10bit_address=True the bus will use 10-bit slave addresses\n"
  "instead of 7-bit addresses.\n");
static PyObject *I2CDev_open(I2CDev *self, PyObject *args, PyObject *kwds) {
  uint8_t use_10bit_address;
  static char *kwlist[] = {"use_10bit_address", NULL};
  use_10bit_address = 0;
  if(!PyArg_ParseTupleAndKeywords(args, kwds, "|b", kwlist, 
                                  &use_10bit_address)) {
    return NULL;
  }

  if (self->i2c_fd > 0) I2C_close(self->i2c_fd);
  self->i2c_fd = I2C_open(self->bus_num);
  if (self->i2c_fd < 0) {
    PyErr_SetString(PyExc_IOError, "could not open I2C interface");
    return NULL;
  }
  
  if (use_10bit_address) {
    if (I2C_enable10BitAddressing(self->i2c_fd) < 0) {
      PyErr_SetString(PyExc_IOError, 
          "could not set I2C interface to 10-bit address mode");
      return NULL;
    }
  }
  else {
    if (I2C_disable10BitAddressing(self->i2c_fd) < 0) {
      PyErr_SetString(PyExc_IOError, 
          "could not set I2C interface to 10-bit address mode");
      return NULL;
    }
  }

  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(I2CDev_close__doc__,
  "I2CDev.close() -> None\n\n"
  "Close the I2C bus interface.\n");

static PyObject *I2CDev_close(I2CDev *self, PyObject *args, PyObject *kwds) {
  if (self->i2c_fd > 0) I2C_close(self->i2c_fd);
  Py_INCREF(Py_None);
  return Py_None;
}


PyDoc_STRVAR(I2CDev_read__doc__,
  "I2CDev.read(slave_addr, n_bytes) -> list\n\n"
  "Reads n_bytes words from the I2C slave device with the given address\n"
  "and returns them as a list.\n");
static PyObject *I2CDev_read(I2CDev *self, PyObject *args, PyObject *kwds) {
  uint32_t n_bytes, i, addr;
  PyObject *data, *byte_obj;
  uint8_t *rxbuf; 
  if(!PyArg_ParseTuple(args, "II", &addr, &n_bytes)) {
    return NULL;
  }

  if (self->slave_addr != addr) {
    if (setSlaveAddress(self->i2c_fd, addr) < 0) {
      PyErr_SetString(PyExc_IOError, "could not configure I2C interface");
      return NULL;
    }
    self->slave_addr = addr;
  }

  rxbuf = malloc(n_bytes);
  if (I2C_read(self->i2c_fd, (void *) rxbuf, n_bytes) < 0) {
    PyErr_SetString(PyExc_IOError, "could not read from I2C device");
    free(rxbuf);
    return NULL;
  }

  data = PyList_New(0);
  for (i=0; i<n_bytes; i++) {
    byte_obj = PyInt_FromLong((long) rxbuf[i]);
    PyList_Append(data, byte_obj);
    Py_DECREF(byte_obj);
  }
  free(rxbuf);
  return data;
}

PyDoc_STRVAR(I2CDev_readTransaction__doc__,
  "I2CDev.readTransaction(slave_addr, tx_byte, n_bytes) -> list\n\n"
  "Writes tx_byte then immediately reads n_bytes words from the I2C slave\n"
  "device with the given address and returns them as a list.\n");
static PyObject *I2CDev_readTransaction(I2CDev *self, PyObject *args, 
                                        PyObject *kwds) {
  uint32_t n_bytes, i, addr;
  uint8_t byte;
  PyObject *data, *byte_obj;
  uint8_t *rxbuf; 
  if(!PyArg_ParseTuple(args, "IbI", &addr, &byte, &n_bytes)) {
    return NULL;
  }

  if (self->slave_addr != addr) {
    if (setSlaveAddress(self->i2c_fd, addr) < 0) {
      PyErr_SetString(PyExc_IOError, "could not configure I2C interface");
      return NULL;
    }
    self->slave_addr = addr;
  }

  rxbuf = malloc(n_bytes);

  if (I2C_write(self->i2c_fd, (void *) &byte, 1) < 0) {
    PyErr_SetString(PyExc_IOError, "could not write to I2C device");
    free(rxbuf);
    return NULL;
  }
  if (I2C_read(self->i2c_fd, (void *) rxbuf, n_bytes) < 0) {
    PyErr_SetString(PyExc_IOError, "could not read from I2C device");
    free(rxbuf);
    return NULL;
  }

  data = PyList_New(0);
  for (i=0; i<n_bytes; i++) {
    byte_obj = PyInt_FromLong((long) rxbuf[i]);
    PyList_Append(data, byte_obj);
    Py_DECREF(byte_obj);
  }
  free(rxbuf);
  return data;
}

PyDoc_STRVAR(I2CDev_write__doc__,
  "I2CDev.write(slave_addr, [bytes]) -> None\n\n"
  "Writes the given list of bytes to the I2C slave device with the\n"
  "given address. Only integers in the range [0,255] are valid.\n");
static PyObject *I2CDev_write(I2CDev *self, PyObject *args, PyObject *kwds) {
  uint32_t n_bytes, i, addr;
  long byte;
  PyObject *data, *byte_obj;
  uint8_t *txbuf; 
  if(!PyArg_ParseTuple(args, "IO!", &addr, &PyList_Type, &data)) {
    return NULL;
  }

  if (self->slave_addr != addr) {
    if (setSlaveAddress(self->i2c_fd, addr) < 0) {
      PyErr_SetString(PyExc_IOError, "could not configure I2C interface");
      return NULL;
    }
    self->slave_addr = addr;
  }

  n_bytes = PyList_Size(data);
  txbuf = malloc(n_bytes);

  for (i=0; i<n_bytes; i++) {
    byte_obj = PyList_GetItem(data, i);
    if (!PyInt_Check(byte_obj)) {
      PyErr_SetString(PyExc_ValueError, 
        "data list to transmit can only contain integers");
      free(txbuf);
      return NULL;
    }
    byte = PyInt_AsLong(byte_obj);
    if (byte < 0) {
      // Check for error from PyInt_AsLong:
      if (PyErr_Occurred() != NULL) return NULL;
      // Negative numbers are set to 0:
      byte = 0;
    }
    // Just send the LSB if value longer than 1 byte:
    byte &= 255;
    txbuf[i] = (uint8_t) byte;
  }

  if (I2C_write(self->i2c_fd, (void *) txbuf, n_bytes) < 0) {
    PyErr_SetString(PyExc_IOError, "could not write to I2C device");
    free(txbuf);
    return NULL;
  }
  free(txbuf);
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *I2CDev_get_i2c_fd(I2CDev *self, void *closure) {
    PyObject *i2c_fd;
    i2c_fd = Py_BuildValue("i", self->i2c_fd);
    Py_INCREF(i2c_fd);
    return i2c_fd;
}

static int I2CDev_set_i2c_fd(I2CDev *self, PyObject *value, void *closure) {
  return 0;
}

static PyObject *I2CDev_get_bus_num(I2CDev *self, void *closure) {
    PyObject *bus_num;
    bus_num = Py_BuildValue("b", self->bus_num);
    Py_INCREF(bus_num);
    return bus_num;
}

static int I2CDev_set_bus_num(I2CDev *self, PyObject *value, void *closure) {
  long int bus_num;
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete bus_num attribute");
    return -1;
  }
  if (!PyInt_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "bus_num must be an integer");
    return -1;
  }

  bus_num = PyInt_AsLong(value);
  if (bus_num < 0 || bus_num > 255) {
    PyErr_SetString(PyExc_TypeError, "bus_num must be in range [0,255]");
    return -1;
  }

  self->bus_num = (uint8_t) bus_num;
  return 0;
}



static PyGetSetDef I2CDev_getseters[] = {
  {"i2c_fd", (getter)I2CDev_get_i2c_fd, (setter)I2CDev_set_i2c_fd, 
   "I2C device file descriptor", NULL},
  {"bus_num", (getter)I2CDev_get_bus_num, (setter)I2CDev_set_bus_num, 
   "I2C bus number", NULL},
  {NULL}
};

static PyMethodDef I2CDev_methods[] = {
  {"open", (PyCFunction)I2CDev_open, METH_KEYWORDS,
    I2CDev_open__doc__},
  {"close", (PyCFunction)I2CDev_close, METH_NOARGS,
    I2CDev_close__doc__},

  {"read", (PyCFunction)I2CDev_read, METH_VARARGS,
    I2CDev_read__doc__},
  {"readTransaction", (PyCFunction)I2CDev_readTransaction, METH_VARARGS,
    I2CDev_readTransaction__doc__},
  {"write", (PyCFunction)I2CDev_write, METH_VARARGS,
    I2CDev_write__doc__},

  {NULL},
};

static PyTypeObject I2CDev_type = {
  PyObject_HEAD_INIT(NULL)
  0,                                        /*ob_size*/
  "i2cdev.I2CDev",                          /*tp_name*/
  sizeof(I2CDev),                           /*tp_basicsize*/
  0,                                        /*tp_itemsize*/
  (destructor)I2CDev_dealloc,               /*tp_dealloc*/
  0,                                        /*tp_print*/
  0,                                        /*tp_getattr*/
  0,                                        /*tp_setattr*/
  0,                                        /*tp_compare*/
  0,                                        /*tp_repr*/
  0,                                        /*tp_as_number*/
  0,                                        /*tp_as_sequence*/
  0,                                        /*tp_as_mapping*/
  0,                                        /*tp_hash */
  0,                                        /*tp_call*/
  0,                                        /*tp_str*/
  0,                                        /*tp_getattro*/
  0,                                        /*tp_setattro*/
  0,                                        /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
  "I2CDev object",                          /* tp_doc */
  0,                                        /* tp_traverse */
  0,                                        /* tp_clear */
  0,                                        /* tp_richcompare */
  0,                                        /* tp_weaklistoffset */
  0,                                        /* tp_iter */
  0,                                        /* tp_iternext */
  I2CDev_methods,                           /* tp_methods */
  0,                                        /* tp_members */
  I2CDev_getseters,                         /* tp_getset */
  0,                                        /* tp_base */
  0,                                        /* tp_dict */
  0,                                        /* tp_descr_get */
  0,                                        /* tp_descr_set */
  0,                                        /* tp_dictoffset */
  (initproc)I2CDev_init,                    /* tp_init */
  0,                                        /* tp_alloc */
  I2CDev_new,                               /* tp_new */
};


#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC initi2cdev(void) {
  PyObject* m;

  I2CDev_type.tp_new = PyType_GenericNew;
  if (PyType_Ready(&I2CDev_type) < 0) return;

  m = Py_InitModule3("i2cdev", I2CDev_methods, I2CDev_module__doc__);
  Py_INCREF(&I2CDev_type);
  PyModule_AddObject(m, "I2CDev", (PyObject *)&I2CDev_type);
}
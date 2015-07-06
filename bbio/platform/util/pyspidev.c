/* pyspidev.c
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
#include "spidriver.h"

PyDoc_STRVAR(SPIDev_module__doc__,
  "This module provides the SPIDev class for controlling SPI interfaces on\n"
  "Linux platforms. The appropriated Linux kernel drivers for your platform\n"
  "must already be loaded to provide a spidev interface to control, i.e.\n"
  "/dev/spidevB.C (where B is the bus and C is the chip select).\n"
  "To control /dev/spidev0.0 you would instantiate with SPIDev(0,0).");

#define SPIDev_MAX_CS_PER_BUS 8

typedef struct {
   PyObject_HEAD
   int *spidev_fd;
   uint8_t bus;
   uint8_t bits_per_word;
   uint8_t bytes_per_word;
   uint8_t mode_3wire;
} SPIDev;


static PyObject *SPIDev_new(PyTypeObject *type, PyObject *args, PyObject *kwds) {
  SPIDev *self;
  self = (SPIDev *)type->tp_alloc(type, 0);
  return (PyObject *)self;
}

static void SPIDev_dealloc(SPIDev* self) {
  free(self->spidev_fd);
  self->ob_type->tp_free((PyObject*)self);
}

static PyObject *SPIDev_init(SPIDev *self, PyObject *args, PyObject *kwds) {
  uint8_t bus, mode_3wire, i;
  mode_3wire = 0;
  static char *kwlist[] = {"bus", "mode_3wire", NULL};
  if(!PyArg_ParseTupleAndKeywords(args, kwds, "b|b", kwlist, &bus,
                                  &mode_3wire)) {
    return NULL;
  }
  self->spidev_fd = malloc(sizeof(int) * SPIDev_MAX_CS_PER_BUS);
  for (i=0; i<SPIDev_MAX_CS_PER_BUS; i++) {
    self->spidev_fd[i] = -1;
  }
  self->mode_3wire = mode_3wire ? 1 : 0;
  self->bus = bus;
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_open__doc__,
  "SPIDev.open() -> None\n\n"
  "Initialize the SPI interface.\n");
static PyObject *SPIDev_open(SPIDev *self, PyObject *args, PyObject *kwds) {
  self->spidev_fd[0] = SPI_open(self->bus, 0);
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, "could not open spidev");
    return NULL;
  }
  self->bits_per_word = SPI_getBitsPerWord(self->spidev_fd[0]);
  if (self->bits_per_word <= 8) {
    self->bytes_per_word = 1;
  }
  else if (self->bits_per_word <= 16) {
    self->bytes_per_word = 2;
  }
  else if (self->bits_per_word <= 32) {
    self->bytes_per_word = 4;
  }
  if (self->mode_3wire) {
    SPI_enable3Wire(self->spidev_fd[0]);
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_close__doc__,
  "SPIDev.close() -> None\n\n"
  "Close the SPI interface.\n");

static PyObject *SPIDev_close(SPIDev *self, PyObject *args, PyObject *kwds) {
  int i;
  for (i=0; i<SPIDev_MAX_CS_PER_BUS; i++) {
    if (self->spidev_fd[i] > 0) {
      SPI_close(self->spidev_fd[i]);
      self->spidev_fd[i] = -1;
    }
  }
  Py_INCREF(Py_None);
  return Py_None;
}

int SPIDev_activateCS(SPIDev *self, uint8_t cs) {
  if (cs > SPIDev_MAX_CS_PER_BUS) {
    PyErr_SetString(PyExc_IOError, "invalid chip select");
    return -1;
  }
  if (self->spidev_fd[cs] < 0) {
    if (cs == 0) {
      PyErr_SetString(PyExc_IOError, 
        "must call SPIDev.open() first to initialize the SPI interface");
      return -1;
    }
    self->spidev_fd[cs] = SPI_open(self->bus, cs);
    if (self->spidev_fd[cs] < 0) {
      PyErr_SetString(PyExc_IOError, "could not access given SPI chip select");
      return -1;
    }
  }
  return 0;
}

PyDoc_STRVAR(SPIDev_read__doc__,
  "SPIDev.read(cs, n_words) -> list\n\n"
  "Reads n_words words from the SPI interface and returns them as a list.\n"
  "Uses the given chip select.\n"
  "Will only read up to a maximum of 4096 byts.\n");
static PyObject *SPIDev_read(SPIDev *self, PyObject *args, PyObject *kwds) {
  uint8_t cs;
  uint32_t n_bytes, n_words, i, word;
  PyObject *data, *word_obj;
  void *rxbuf; 
  if(!PyArg_ParseTuple(args, "bI", &cs, &n_words)) {
    return NULL;
  }

  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  n_bytes = (uint32_t) (((float) (self->bits_per_word * n_words)) / 8.0 + 0.5);
  rxbuf = malloc(n_bytes);

  SPI_read(self->spidev_fd[cs], rxbuf, n_words);

  data = PyList_New(0);
  for (i=0; i<n_words; i++) {
    switch(self->bytes_per_word) {
    case 1:
      word = ((uint8_t*)rxbuf)[i];
      break;
    case 2:
      word = ((uint16_t*)rxbuf)[i];
      break;
    case 4:
      word = ((uint32_t*)rxbuf)[i];
      break;
    default:
      word = 0;
      break;
    }
    word_obj = PyInt_FromLong(word);
    PyList_Append(data, word_obj);
    Py_DECREF(word_obj);
  }
  free(rxbuf);
  return data;
}

PyDoc_STRVAR(SPIDev_write__doc__,
  "SPIDev.write(cs, [words]) -> int\n\n"
  "Writes the given list of words to the SPI interface.\n"
  "Uses the given chip select.\n"
  "Will only write up to a maximum of 4096 byts.\n"
  "Returns the number of words written.\n");
static PyObject *SPIDev_write(SPIDev *self, PyObject *args, PyObject *kwds) {
  uint8_t cs;
  uint32_t n_bytes, n_words, i, word;
  PyObject *data, *word_obj;
  void *txbuf;

  if(!PyArg_ParseTuple(args, "bO!", &cs, &PyList_Type, &data)) {
    return NULL;
  }
  
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  n_words = PyList_Size(data);
  n_bytes = (uint32_t) (((float) (self->bits_per_word * n_words)) / 8.0 + 0.5);
  txbuf = malloc(n_bytes);

  for (i=0; i<n_words; i++) {
    word_obj = PyList_GetItem(data, i);
    if (!PyInt_Check(word_obj)) {
      PyErr_SetString(PyExc_ValueError, 
        "data list to transmit can only contain integers");
      free(txbuf);
      return NULL;
    }
    word = PyInt_AsLong(word_obj);
    if (word < 0) {
      if (PyErr_Occurred() != NULL) return NULL;
      word = 0;
    }
    switch(self->bytes_per_word) {
    case 1:
      ((uint8_t*)txbuf)[i] = (uint8_t) word;
      break;
    case 2:
      ((uint16_t*)txbuf)[i] = (uint16_t) word;
      break;
    case 4:
      ((uint32_t*)txbuf)[i] = (uint32_t) word;
      break;
    default:
      break;
    }
  }
  n_words = SPI_write(self->spidev_fd[cs], txbuf, n_words);
  free(txbuf);
  return Py_BuildValue("i", n_words);
}

PyDoc_STRVAR(SPIDev_transfer__doc__,
  "SPIDev.transfer(cs, [words]) -> list\n\n"
  "Writes the given list of words to the SPI interface while simultaneously\n"
  "reading bytes.\n"
  "Uses the given chip select.\n"
  "Will only write/read up to a maximum of 4096 byts.\n"
  "Returns the number of words written.\n");
static PyObject *SPIDev_transfer(SPIDev *self, PyObject *args, PyObject *kwds) {
  uint8_t cs;
  uint32_t n_bytes, n_words, i, word;
  PyObject *txdata, *rxdata, *word_obj;
  void *txbuf, *rxbuf;

  if (self->mode_3wire) {
    PyErr_SetString(PyExc_IOError, 
      "SPIDev.transfer not supported in 3 wire mode");
    return NULL;
  }
  cs = 0;
  if(!PyArg_ParseTuple(args, "bO!", &cs, &PyList_Type, &txdata)) {
    return NULL;
  }
  
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  n_words = PyList_Size(txdata);
  n_bytes = (uint32_t) (((float) (self->bits_per_word * n_words)) / 8.0 + 0.5);
  txbuf = malloc(n_bytes);
  rxbuf = malloc(n_bytes);

  for (i=0; i<n_words; i++) {
    word_obj = PyList_GetItem(txdata, i);
    if (!PyInt_Check(word_obj)) {
      PyErr_SetString(PyExc_ValueError, 
        "data list to transmit can only contain integers");
      free(txbuf);
      return NULL;
    }
    word = PyInt_AsLong(word_obj);
    if (word < 0) {
      if (PyErr_Occurred() != NULL) return NULL;
      word = 0;
    }
    switch(self->bytes_per_word) {
    case 1:
      ((uint8_t*)txbuf)[i] = (uint8_t) word;
      break;
    case 2:
      ((uint16_t*)txbuf)[i] = (uint16_t) word;
      break;
    case 4:
      ((uint32_t*)txbuf)[i] = (uint32_t) word;
      break;
    default:
      break;
    }
  }
  n_words = SPI_transfer(self->spidev_fd[cs], txbuf, rxbuf, n_words);
  rxdata = PyList_New(0);
  for (i=0; i<n_words; i++) {
    switch(self->bytes_per_word) {
    case 1:
      word = ((uint8_t*)rxbuf)[i];
      break;
    case 2:
      word = ((uint16_t*)rxbuf)[i];
      break;
    case 4:
      word = ((uint32_t*)rxbuf)[i];
      break;
    default:
      word = 0;
      break;
    }
    PyList_Append(rxdata, PyInt_FromLong(word));
  }
  free(txbuf);
  free(rxbuf);
  return rxdata;
}

PyDoc_STRVAR(SPIDev_setMSBFirst__doc__,
  "SPIDev.setMSBFirst(cs) -> None\n\n"
  "Sets the SPI bit order for the given chip select to be most significant\n"
  "bit first.\n"
  "Raises an exception if unable to set the bit order.\n");
static PyObject *SPIDev_setMSBFirst(SPIDev *self, PyObject *args, 
                                    PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_setBitOrder(self->spidev_fd[cs], SPI_MSBFIRST) < 0) {
    PyErr_SetString(PyExc_IOError, "could not set SPI bit order");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_setLSBFirst__doc__,
  "SPIDev.setLSBFirst(cs) -> None\n\n"
  "Sets the SPI bit order for the given chip select to be least significant\n"
  "bit first.\n"
  "Raises an exception if unable to set the bit order.\n");
static PyObject *SPIDev_setLSBFirst(SPIDev *self, PyObject *args, 
                                    PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_setBitOrder(self->spidev_fd[cs], SPI_LSBFIRST) < 0) {
    PyErr_SetString(PyExc_IOError, "could not set SPI bit order");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_setBitsPerWord__doc__,
  "SPIDev.setBitsPerWord(cs, bits_per_word) -> None\n\n"
  "Sets the SPI bits per word for the given chip select to the given value.\n"
  " (0<bits_per_word<256).\n"
  "Raises an exception if unable to set the bit order.\n");
static PyObject *SPIDev_setBitsPerWord(SPIDev *self, PyObject *args, 
                                       PyObject *kwds) {
  uint8_t bpw, cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "bb", &cs, &bpw)) {
    return NULL;
  }
  if (bpw > 32) {
    PyErr_SetString(PyExc_IOError, "bits per word must be <= 32");
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;
  
  if (SPI_setBitsPerWord(self->spidev_fd[cs], bpw) < 0) {
    PyErr_SetString(PyExc_ValueError, "could not set SPI bits per word");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_setMaxFrequency__doc__,
  "SPIDev.setMaxFrequency(cs, frequency) -> None\n\n"
  "Sets the maximum SPI clock frequency for the given chip select to the\n"
  "given value.\n"
  "Raises an exception if unable to set the frequency.\n");
static PyObject *SPIDev_setMaxFrequency(SPIDev *self, PyObject *args, 
                                        PyObject *kwds) {
  uint8_t cs;
  uint32_t frequency;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "bi", &cs, &frequency)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_setMaxFrequency(self->spidev_fd[cs], frequency) < 0) {
    PyErr_SetString(PyExc_IOError, "could not set SPI frequency");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_enableLoopback__doc__,
  "SPIDev.enableLoopback(cs) -> None\n\n"
  "Sets the SPI interface to loopback mode for the given chip sleect.\n"
  "Raises an exception if unable to enable loopback mode.\n");
static PyObject *SPIDev_enableLoopback(SPIDev *self, PyObject *args, 
                                        PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_enableLoopback(self->spidev_fd[cs]) < 0) {
    PyErr_SetString(PyExc_IOError, "could not enable SPI loopback");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_disableLoopback__doc__,
  "SPIDev.disableLoopback(cs) -> None\n\n"
  "Disables loopback mode for the given chip select of the SPI interface.\n"
  "Raises an exception if unable to disable loopback mode.\n");
static PyObject *SPIDev_disableLoopback(SPIDev *self, PyObject *args, 
                                        PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_disableLoopback(self->spidev_fd[cs]) < 0) {
    PyErr_SetString(PyExc_IOError, "could not disable SPI loopback");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_setClockMode__doc__,
  "SPIDev.setClockMode(cs, clock_mode) -> None\n\n"
  "Sets the clock mode for the given chip select of the SPI interface.\n"
  "See http://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus#Mode_numbers\n"
  "Raises an exception if unable to set the clock mode.\n");
static PyObject *SPIDev_setClockMode(SPIDev *self, PyObject *args, 
                                     PyObject *kwds) {
  uint8_t mode, cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "bb", &cs, &mode)) {
    return NULL;
  }
  if (mode > 3) {
    PyErr_SetString(PyExc_IOError, "SPI clock mode must be in range 0-3");
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_setClockMode(self->spidev_fd[cs], mode) < 0) {
    PyErr_SetString(PyExc_IOError, "could not set SPI clock mode");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_setCSActiveLow__doc__,
  "SPIDev.setCSActiveLow(cs) -> None\n\n"
  "Sets the SPI interface to use a low level when activating the given chip\n"
  "select (default).\n"
  "Raises an exception if unable to set the CS mode.\n");
static PyObject *SPIDev_setCSActiveLow(SPIDev *self, PyObject *args, 
                                       PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_setCSActiveLow(self->spidev_fd[cs]) < 0) {
    PyErr_SetString(PyExc_IOError, "could not set SPI CS to active low");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_setCSActiveHigh__doc__,
  "SPIDev.setCSActiveHigh(cs) -> None\n\n"
  "Sets the SPI interface to use a high level when activating the given chip\n"
  "select (inverted).\n"
  "Raises an exception if unable to set the CS mode.\n");
static PyObject *SPIDev_setCSActiveHigh(SPIDev *self, PyObject *args, 
                                        PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_setCSActiveHigh(self->spidev_fd[cs]) < 0) {
    PyErr_SetString(PyExc_IOError, "could not set SPI CS to active high");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_disableCS__doc__,
  "SPIDev.disableCS(cs) -> None\n\n"
  "Disables the given chip select for the SPI interface.\n"
  "Raises an exception if unable to set disable CS.\n");
static PyObject *SPIDev_disableCS(SPIDev *self, PyObject *args, 
                                  PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_disableCS(self->spidev_fd[cs]) < 0) {
    PyErr_SetString(PyExc_IOError, "could not disable SPI CS");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

PyDoc_STRVAR(SPIDev_enableCS__doc__,
  "SPIDev.enableCS(cs) -> None\n\n"
  "Enables the given chip select for the SPI interface (default state).\n"
  "Raises an exception if unable to set disable CS.\n");
static PyObject *SPIDev_enableCS(SPIDev *self, PyObject *args, 
                                  PyObject *kwds) {
  uint8_t cs;
  if (self->spidev_fd[0] < 0) {
    PyErr_SetString(PyExc_IOError, 
      "must call SPIDev.open() first to initialize the SPI interface");
    return NULL;
  }
  if(!PyArg_ParseTuple(args, "b", &cs)) {
    return NULL;
  }
  if (SPIDev_activateCS(self, cs) < 0) return NULL;

  if (SPI_enableCS(self->spidev_fd[0]) < 0) {
    PyErr_SetString(PyExc_IOError, "could not enable SPI CS");
    return NULL;
  }
  Py_INCREF(Py_None);
  return Py_None;
}

static PyObject *SPIDev_getBus(SPIDev *self, void *closure) {
  return Py_BuildValue("i", self->bus);
}

static int SPIDev_setBus(SPIDev *self, PyObject *value, void *closure) {
  long int bus;
  if (value == NULL) {
    PyErr_SetString(PyExc_TypeError, "Cannot delete bus attribute");
    return -1;
  }
  if (!PyInt_Check(value)) {
    PyErr_SetString(PyExc_TypeError, "bus attribute must be integer");
    return -1;
  }

  bus = PyInt_AsLong(value);
  if (bus < 0 || bus > 255) {
    PyErr_SetString(PyExc_TypeError, "bus number must be in range [0,255]");
    return -1;
  }

  self->bus = (uint8_t) bus;
  return 0;
}

static PyObject *SPIDev_getSpidev(SPIDev *self, void *closure) {
  int i;
  PyObject *spidev_fd;
  spidev_fd = PyList_New(SPIDev_MAX_CS_PER_BUS);
  for (i=0; i<SPIDev_MAX_CS_PER_BUS; i++) {
    PyList_SetItem(spidev_fd, i, Py_BuildValue("i", self->spidev_fd[i]));
  }
  return spidev_fd;
}

static int SPIDev_setSpidev(SPIDev *self, PyObject *value, void *closure) {
  return 0;
}


static PyGetSetDef SPIDev_getseters[] = {
  {"bus", (getter)SPIDev_getBus, (setter)SPIDev_setBus, 
   "SPI bus number", NULL},
  {"spidev_fd", (getter)SPIDev_getSpidev, (setter)SPIDev_setSpidev, 
   "spidev file descriptor", NULL},
  {NULL}
};

static PyMethodDef SPIDev_methods[] = {
  {"open", (PyCFunction)SPIDev_open, METH_NOARGS,
    SPIDev_open__doc__},
  {"close", (PyCFunction)SPIDev_close, METH_NOARGS,
    SPIDev_close__doc__},

  {"read", (PyCFunction)SPIDev_read, METH_VARARGS,
    SPIDev_read__doc__},
  {"write", (PyCFunction)SPIDev_write, METH_VARARGS,
    SPIDev_write__doc__},
  {"transfer", (PyCFunction)SPIDev_transfer, METH_VARARGS,
    SPIDev_transfer__doc__},

  {"setMSBFirst", (PyCFunction)SPIDev_setMSBFirst, METH_VARARGS,
    SPIDev_setMSBFirst__doc__},
  {"setLSBFirst", (PyCFunction)SPIDev_setLSBFirst, METH_VARARGS,
    SPIDev_setLSBFirst__doc__},

  {"setBitsPerWord", (PyCFunction)SPIDev_setBitsPerWord, METH_VARARGS,
    SPIDev_setBitsPerWord__doc__},

  {"setMaxFrequency", (PyCFunction)SPIDev_setMaxFrequency, METH_VARARGS,
    SPIDev_setMaxFrequency__doc__},

  {"enableLoopback", (PyCFunction)SPIDev_enableLoopback, METH_VARARGS,
    SPIDev_enableLoopback__doc__},
  {"disableLoopback", (PyCFunction)SPIDev_disableLoopback, METH_VARARGS,
    SPIDev_disableLoopback__doc__},

  {"setClockMode", (PyCFunction)SPIDev_setClockMode, METH_VARARGS,

    SPIDev_setClockMode__doc__},
  {"setCSActiveLow", (PyCFunction)SPIDev_setCSActiveLow, METH_VARARGS,
    SPIDev_setCSActiveLow__doc__},
  {"setCSActiveHigh", (PyCFunction)SPIDev_setCSActiveHigh, METH_VARARGS,
    SPIDev_setCSActiveHigh__doc__},

  {"disableCS", (PyCFunction)SPIDev_disableCS, METH_VARARGS,
    SPIDev_disableCS__doc__},
  {"enableCS", (PyCFunction)SPIDev_enableCS, METH_VARARGS,
    SPIDev_enableCS__doc__},

  {NULL},
};

static PyTypeObject SPIDev_type = {
  PyObject_HEAD_INIT(NULL)
  0,                                        /*ob_size*/
  "spidev.SPIDev",                          /*tp_name*/
  sizeof(SPIDev),                           /*tp_basicsize*/
  0,                                        /*tp_itemsize*/
  (destructor)SPIDev_dealloc,               /*tp_dealloc*/
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
  "SPIDev object",                          /* tp_doc */
  0,                                        /* tp_traverse */
  0,                                        /* tp_clear */
  0,                                        /* tp_richcompare */
  0,                                        /* tp_weaklistoffset */
  0,                                        /* tp_iter */
  0,                                        /* tp_iternext */
  SPIDev_methods,                           /* tp_methods */
  0,                                        /* tp_members */
  SPIDev_getseters,                         /* tp_getset */
  0,                                        /* tp_base */
  0,                                        /* tp_dict */
  0,                                        /* tp_descr_get */
  0,                                        /* tp_descr_set */
  0,                                        /* tp_dictoffset */
  (initproc)SPIDev_init,                    /* tp_init */
  0,                                        /* tp_alloc */
  SPIDev_new,                               /* tp_new */
};


#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC initspidev(void) {
  PyObject* m;

  SPIDev_type.tp_new = PyType_GenericNew;
  if (PyType_Ready(&SPIDev_type) < 0) return;

  m = Py_InitModule3("spidev", SPIDev_methods, SPIDev_module__doc__);
  Py_INCREF(&SPIDev_type);
  PyModule_AddObject(m, "SPIDev", (PyObject *)&SPIDev_type);
}
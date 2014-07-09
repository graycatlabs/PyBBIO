/* bone_mmap.c
 * Part of PyBBIO
 * MIT License
 * 
 * A Python C extension to help speed up IO on the Beaglebone.
 */


#include <Python.h>
#include "bone_mmap.h"
#include <mmap_util.h>
#include <stdio.h>


static PyObject *cleanup(PyObject *self, PyObject *args) {
  mmapClose();
  return Py_BuildValue("");
}

static PyObject *getReg(PyObject *self, PyObject *args) {
  memaddr address;
  if (!PyArg_ParseTuple(args,"K", &address)) {
    return NULL;
  }
  return Py_BuildValue("I", _getReg(address, LITTLEENDIAN, 4));
}

static PyObject *getReg16(PyObject *self, PyObject *args) {
  memaddr address;
  if (!PyArg_ParseTuple(args,"K", &address)) {
    return NULL;
  }
  return Py_BuildValue("I", _getReg(address, LITTLEENDIAN, 2));
}

static PyObject *setReg(PyObject *self, PyObject *args) {
  memaddr address;
  uint value;
  if (!PyArg_ParseTuple(args,"KI", &address, &value)) {
    return NULL;
  }
  _setReg(address, value, LITTLEENDIAN, 4);
  return Py_BuildValue("");
}

static PyObject *setReg16(PyObject *self, PyObject *args) {
  memaddr address;
  uint value;
  if (!PyArg_ParseTuple(args,"KI", &address, &value)) {
    return NULL;
  }
  _setReg(address, value, LITTLEENDIAN, 2);
  return Py_BuildValue("");
}


static PyMethodDef functions[] = {
  {"cleanup", cleanup, METH_VARARGS, 
	 "Driver cleanup routine; must be called once before program exit."},
  
  {"getReg", getReg, METH_VARARGS, "Returns 32 bit value at given register."},
  {"getReg16", getReg16, METH_VARARGS, "Returns 16 bit value at given register."},
  
  {"setReg", setReg, METH_VARARGS, "Sets 32 bit register to given value."},
  {"setReg16", setReg16, METH_VARARGS, "Sets 16 bit register to given value."},
  
  { NULL }
};

void initbone_mmap(void) {
  mmapInit(MMAP_FILE, MMAP_OFFSET, MMAP_SIZE);
  Py_InitModule3("bone_mmap", functions, "BeagleBone mmap driver");
}


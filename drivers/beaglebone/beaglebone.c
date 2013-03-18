/*
 * Requirements for building:
 *  gcc
 *  python-dev
 */


#include <Python.h>
#include "beaglebone.h"
#include <mmap_util.h>
#include <pinmux_util.h>
#include <stdio.h>

int counter;

static PyObject *test_it(PyObject *self, PyObject *args) {
  return Py_BuildValue("i", counter++);
}


static PyObject *cleanup(PyObject *self, PyObject *args) {
  mmapClose();
	return Py_BuildValue("");
}

static PyObject *digitalRead(PyObject *self, PyObject *args) {
	ulong reg;
	uint mask, state;
	if (!PyArg_ParseTuple(args, "kI:beaglebone.digitalRead", &reg, &mask)) {
		return NULL;
	}
  state = !!(getReg(reg, LITTLEENDIAN) & mask);
	return Py_BuildValue("i", state);
}



static PyMethodDef functions[] = {
  {"test_it", test_it, METH_VARARGS, "testing c extensions"},
  {"cleanup", cleanup, METH_VARARGS, 
	 "Driver cleanup routine; must be called once before program exit."},
	{"digitalRead", digitalRead, METH_VARARGS,
	 "Returns input pin state of given pin."},
  { NULL }
};

void initdriver(void) {
  counter = 0;
  mmapInit(MMAP_FILE, MMAP_OFFSET, MMAP_SIZE);
  Py_InitModule3("driver", functions, "Test module");
}


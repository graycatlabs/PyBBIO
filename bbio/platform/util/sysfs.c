/* sysfs.c
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
#include "sysfs.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <glob.h>
#include <errno.h>

 PyDoc_STRVAR(sysfs_module__doc__,
  "This module provides the kernelFileIO routine for reading and writing\n"
  "special kernel files.");

char *getFirstGlobMatch(char *path) {
  char *expanded_path;
  size_t length;
  glob_t glob_results;
  glob(path, GLOB_NOSORT, 0, &glob_results);
  if (glob_results.gl_pathc == 0) {
    // No matching paths, generate empty string:
    expanded_path = (char *) calloc(1, sizeof(char));
  }
  else {
    // Found at least one match, grab first:
    length = strlen(glob_results.gl_pathv[0]);
    expanded_path = (char *) calloc(length+1, sizeof(char));
    memcpy(expanded_path, glob_results.gl_pathv[0], length);
  }
  globfree(&glob_results);
  return expanded_path;
}

int kernelFileWrite(char *path, char *value) {
  FILE* fd;
  char *expanded_path;
  expanded_path = getFirstGlobMatch(path);
  if (strlen(expanded_path) == 0) {
    // Empty string returned, no results found
    free(expanded_path);
    return ENOENT; // "No such file or directory" error code
  }
  fd = fopen(expanded_path, "r+");
  if(!fd) {
    // Could not open file
    free(expanded_path);
    return errno; // fopen() updates errno when it failes
  }
  fprintf(fd, "%s", value);
  fclose(fd);
  free(expanded_path);
  return 0;
}

int kernelFileRead(char *path, char *result, int result_len) {
  FILE* fd;
  char *expanded_path;
  expanded_path = getFirstGlobMatch(path);
  if (strlen(expanded_path) == 0) {  
    // Empty string returned, no results found
    free(expanded_path);
    return ENOENT; // "No such file or directory" error code
  }
  fd = fopen(expanded_path, "r");
  if(!fd) {
    // Could not open file
    free(expanded_path);
    return errno;
  }
  fgets(result, result_len, fd);
  fclose(fd);
  free(expanded_path);
  return 0;
}

static PyObject* kernelFileIO(PyObject *self, PyObject *args) {
  char read_value[READ_BUFFER_LENGTH];
  char *value = NULL;
  char *path;
  int rc;

  // Parse path and optional value:
  if(!(PyArg_ParseTuple(args, "s|s", &path, &value))) {
    PyErr_SetString(PyExc_TypeError, 
      "sysfs.kernelFileIO can only take string values");
    return NULL;
  }
  if (value) {
    // value is not a NULL pointer, meaning a value was passed in
    rc = kernelFileWrite(path, value);
    if (rc) return Py_BuildValue("i", rc); // Got error code, return it
    return Py_BuildValue("s", value);
  }
  rc = kernelFileRead(path, read_value, READ_BUFFER_LENGTH);
  if (rc) return Py_BuildValue("i", rc);
  return Py_BuildValue("s", read_value);
}

static PyMethodDef sysfsMethods[]=
{
	{ "kernelFileIO", kernelFileIO, METH_VARARGS, 
"takes a file path (wildcards allowed) and an optional value string. If only a \
path is given, the contents of the file will be returned. If given a value as \
well, the value will be written to the file and the value will be returned. If \
unsuccsefull an integer error code will be returned (as defined in errno.h)." 
  },
	{ NULL, NULL },
};

#ifndef PyMODINIT_FUNC  /* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif
PyMODINIT_FUNC initsysfs(void)
{
	Py_InitModule3( "sysfs", sysfsMethods, sysfs_module__doc__);
}


/* sysfs.h
 *
 * Provides C and Python functions to read and write kernel driver sysfs 
 * interface files. 
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

#ifndef _SYSFS_H_
#define _SYSFS_H_
  
#include "Python.h"

// Maximum number of bytes to read from file in kernelFileIO():
#define READ_BUFFER_LENGTH 128

// Returns first real path found given path with '*' wildcards, or empty string 
// if no path found. The path string is created with calloc(), and therefore 
// the returned char* must be passed to free() eventually.
char *getFirstGlobMatch(char *path);

// Writes the given value to the file at the given path. The path may contain
// '*' wildcards. Returns 0 if successful, errno error code otherwise. 
int kernelFileWrite(char *filename, char *value);

// Copies up to result_len-1 of the the contents of the file at the given path 
// followed by a null-character to the given result buffer. The path may
// contain '*' wildcards. Returns 0 if successful, errno error code otherwise.
int kernelFileRead(char *filename, char *result, int result_len);

#endif
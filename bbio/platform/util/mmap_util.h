/* mmap_uitl.h
 * Part of PyBBIO
 * MIT License
 * 
 * A C utility for memory access through mmap.
 */

#ifndef _MMAP_UTIL_H
#define _MMAP_UTIL_H

#define LITTLEENDIAN 0
#define BIGENDIAN    1

typedef unsigned long memaddr;
typedef unsigned int uint;

int mmapInit(char *fn, memaddr offset, memaddr size);
/* Attempts to initialize mmap with given parameters. Returns 1 if 
 * successful, 0 otherwise.
 */

void mmapClose(void);
/* Closes mmap. Should be called before program exit.
 */

uint _getReg(memaddr address, int order, int bytes);
/* Returns given number of bytes starting at given address with given 
 * endianness.
 */

void _setReg(memaddr address, uint value, int order, int bytes);
/* Sets memory from address to address+bytes to the given value using
 * the given byte ordering.
 */


#endif

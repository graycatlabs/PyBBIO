/* mmap_uitl.h
 * Part of PyBBIO
 * Apache 2.0 License
 * 
 * A utility for memory access through mmap.
 */

#ifndef _MMAP_UTIL_H
#define _MMAP_UTIL_H

#define LITTLEENDIAN 0
#define BIGENDIAN    1

typedef unsigned long memaddr;
typedef unsigned int uint;

int mmapInit(char *fn, memaddr offset, memaddr size);
/* Attempts to initialize local mmap. Returns 1 if successful, 
 * 0 otherwise.
 */

void mmapClose(void);
/* Closes mmap. Should be called before program exit.
 */

uint getReg(memaddr address, int order);
/* Returns 32-bit value starting at given address with given endianness.
 */

uint getReg16(memaddr address, int order);
/* Returns 16-bit value starting at given address with given endianness.
 */


#endif

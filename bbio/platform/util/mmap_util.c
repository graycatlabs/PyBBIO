/* mmap_uitl.c
 * Part of PyBBIO
 * MIT License
 * 
 * A C utility for memory access through mmap.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include "mmap_util.h"

struct memory {
	int fd;
  int size;
  uint8_t *map;
};

static int mmap_exists = 0;
static struct memory *_mmap;

int mmapInit(char *fn, memaddr offset, memaddr size) {
  int fd;
  uint8_t *map;
  if (mmap_exists) return 0;
  fd = open(fn, O_RDWR);
  if (fd < 0) return 0;
  map = mmap(0, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, offset);
  if (map == MAP_FAILED) return 0;
  _mmap = malloc(sizeof(struct memory*));
  _mmap->fd = fd;
  _mmap->map = map;
  mmap_exists = 1;
  return 1;
}

void mmapClose(void) {
  // Todo: handle and report unmapping/freeing errors
  if (mmap_exists) {
    munmap(_mmap->map, _mmap->size);
    close(_mmap->fd);
    free(_mmap);
    mmap_exists = 0;
  }
}

uint _getReg(memaddr address, int order, int bytes) {
  int i, bits;
  uint value;
  if(!mmap_exists) return 0;
  bits = bytes*8;
  value = 0;
  for (i=0; i<bytes; i++) {
    if (order == BIGENDIAN) {
      value |= (uint) (_mmap->map[address+i] << (bits-(i<<3)));
   	}
    else value |= (uint) (_mmap->map[address+i] << (i<<3));
  }
  return value;
}

void _setReg(memaddr address, uint value, int order, int bytes) {
  int i, bits;
  if(!mmap_exists) return;
  bits = bytes*8;
  for (i=0; i<bytes; i++) {
    if (order == BIGENDIAN) {
      _mmap->map[address+i] = (uint8_t) ((value >> (bits-(i<<3))) & 0xff);
    }
    else _mmap->map[address+i] = ((uint8_t) (value >> (i<<3)) & 0xff);
  }
}


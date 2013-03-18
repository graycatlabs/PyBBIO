/* mmap_uitl.c
 * Part of PyBBIO
 * Apache 2.0 License
 * 
 * A utility for memory access through mmap.
 */


#include "mmap_util.h"
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/mman.h>



struct memory {
	int fd;
  int size;
  int *map;
};

static int mmap_exists = 0;
static struct memory *_mmap;

int mmapInit(char *fn, memaddr offset, memaddr size) {
	int fd, *map;
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

uint getReg(memaddr address, int order) {
  int i;
  uint value;
	if(!mmap_exists) return 0;
  value = 0;
  for (i=0; i<4; i++) {
    if (order == BIGENDIAN) value |= _mmap->map[address+i] << (32-(i<<3));
		else value |= _mmap->map[address+i] << (i<<3);
	}
  return value;
}

uint getReg16(memaddr address, int order) {
  int i;
  uint value;
	if(!mmap_exists) return 0;
  value = 0;
  for (i=0; i<2; i++) {
    if (order == BIGENDIAN) value |= _mmap->map[address+i] << (32-(i<<3));
		else value |= _mmap->map[address+i] << (i<<3);
	}	
	return value;
}

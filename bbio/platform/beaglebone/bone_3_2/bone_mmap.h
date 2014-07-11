/* bone_mmap.h
 * Part of PyBBIO
 * MIT License
 * 
 * PyBBIO configuration for Beaglebone driver.
 */

#ifndef _BEAGLEBONE_CONFIG_H
#define _BEAGLEBONE_CONFIG_H

#define MMAP_FILE   "/dev/mem"
#define MMAP_OFFSET 0x44c00000 
#define MMAP_SIZE   (0x48ffffff-MMAP_OFFSET)


#endif

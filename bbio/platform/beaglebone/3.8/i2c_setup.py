import  cape_manager, bbio, glob, os
from config import I2C

def i2cInit(bus):
	'''
	Initializes reqd I2C bus
	i2c0 (/dev/i2c-0) and i2c2 (/dev/i2c-1) are already initialized
	overlay to be applied for i2c1 (/dev/i2c-2)
	'''
	dev_file, overlay = I2C[bus]
	if os.path.exists(dev_file): 
		return True
	cape_manager.load(overlay, auto_unload=False)
	
	if os.path.exists(dev_file): 
		return True

	for i in range(5):
		bbio.delay(5)
		if os.path.exists(dev_file): 
			return True

	return False


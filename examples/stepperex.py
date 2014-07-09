#t import PyBBIO: 
from bbio import *
# Then we can import Stepper:
from Stepper import *

import time
start_time = time.time() 

stepper = Stepper(GPIO1_17,GPIO3_21,GPIO3_19,GPIO3_15)
def setup():
	stepper.setSpeed(30);

def loop():
	
	
	stepper.stepMotor(1)
	stepper.stepMotor(2)
	stepper.stepMotor(3)
	stepper.stepMotor(4)

	
run(setup, loop)

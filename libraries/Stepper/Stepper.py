"""
 Stepper - v0.1
 Copyright 2014 Alaa Agwa

 Library for controlling stepper motors.

 The sequence of control signals for 4 control wires is as follows:

  Step C0 C1 C2 C3
     1  1  0  1  0
     2  0  1  1  0
     3  0  1  0  1
     4  1  0  0  1

  The sequence of controls signals for 2 control wires is as follows
  (columns C1 and C2 from above):

  Step C0 C1
     1  0  1
     2  1  1
     3  1  0
     4  0  0
"""
from bbio import *


class Stepper(object):
	def __init__(self,pin_1, pin_2, pin_3=None, pin_4=None, steps=100):
		self.step_number = 0	# which step the motor is on
		self.speed = 0			# the motor speed, in revolutions per minute
		self.direction = 0		# motor direction
		self.last_step_time = 0 # time stamp in ms of the last step taken
		self.number_of_steps = steps # total number of steps for this motor

		# Pins for the motor control connection
		self.motor_pin1 = pin_1
		self.motor_pin2 = pin_2
		self.motor_pin3 = pin_3
		self.motor_pin4 = pin_4

		#setup the pins
		pinMode(self.motor_pin1,OUTPUT)
		pinMode(self.motor_pin2,OUTPUT)
		pinMode(self.motor_pin3,OUTPUT)
		pinMode(self.motor_pin4,OUTPUT)

		#pins count the stepMotor() method
		if(self.motor_pin3 == None and self.motor_pin4 == None):
			self.motor_pins = 2
		elif(self.motor_pin3 != None and self.motor_pin4 != None):
			self.motor_pins = 4
		


	#Sets the speed in revs per minute
	def setSpeed(self , whatSpeed):
		self.step_delay = 60L * 1000L / self.number_of_steps / whatSpeed
		


	"""
	Moves the motor steps_to_move steps.  If the number is negative, 
    the motor moves in the reverse direction.
	"""
	def step(self,steps_to_move,start_time):
		steps_left = abs(steps_to_move) #how many steps to take

		#determine direction based on whether steps_to_mode is + or -

		if(steps_to_move>0):
			self.direction = 1
		elif(steps_to_move<0):
			self.direction=0

		#decrement the number of steps, moving one step each time
		while(steps_left >0):
			#move only if the appropriate delay has passed
			if(((start_time*1000) - self.last_step_time) >= self.step_delay):
				self.last_step_time = start_time*1000
				
				#increment or decrement the step number, depending on direction
				if(self.direction == 1):
					self.step_number +=1
					if(self.step_number == self.number_of_steps):
						self.step_number = 0
				else:
					if(self.step_number == 0):
						self.step_number = self.number_of_steps

					self.step_number -=1
			#decrement the steps left
			steps_left -=1
			#step the motor to step number 0, 1, 2, or 3
			stepMotor(self.step_number %4)

	"""

	Moves the motor forward or backwards.

	"""
	def stepMotor(self,thisStep):
		if(self.motor_pins == 2):
			if(thisStep == 0): # 01
				digitalWrite(self.motor_pin1,LOW)
				digitalWrite(self.motor_pin2,HIGH)
			elif(thisStep == 1): # 11 
				digitalWrite(self.motor_pin1,HIGH)
				digitalWrite(self.motor_pin2,HIGH)
			elif(thisStep == 2): # 10
				digitalWrite(self.motor_pin1,HIGH)
				digitalWrite(self.motor_pin2,LOW)
			elif(thisStep == 3): # 00 
				digitalWrite(self.motor_pin1,LOW)
				digitalWrite(self.motor_pin2,LOW)

		elif(self.motor_pins == 4):
			if(thisStep == 0): # 1010
				digitalWrite(self.motor_pin1,HIGH)
				digitalWrite(self.motor_pin2,LOW)
				digitalWrite(self.motor_pin3,HIGH)
				digitalWrite(self.motor_pin4,LOW)
			elif(thisStep == 1): #  0110
				digitalWrite(self.motor_pin1,LOW)
				digitalWrite(self.motor_pin2,HIGH)
				digitalWrite(self.motor_pin3,HIGH)
				digitalWrite(self.motor_pin4,LOW)
			elif(thisStep == 2): # 0101
				digitalWrite(self.motor_pin1,LOW)
				digitalWrite(self.motor_pin2,HIGH)
				digitalWrite(self.motor_pin3,LOW)
				digitalWrite(self.motor_pin4,HIGH)
			elif(thisStep == 3): # 1001
				digitalWrite(self.motor_pin1,HIGH)
				digitalWrite(self.motor_pin2,LOW)
				digitalWrite(self.motor_pin3,LOW)
				digitalWrite(self.motor_pin4,HIGH)

		




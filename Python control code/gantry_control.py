import numpy as np
import math
import serial
import time 

import main_vision



class t_instructions():

	"""
	Creates instructions for gantry arduino to translate from any point to any point
	
	Updates the robot control position

	Takes: 
		- current robot position as array [X1,Y1,Z1]
		- desired end position as array [X2,Y2,Z2]
		- steps per mm for whole gantry [174,174,321]
		- gantry serial port
		- robot control module 
	
	After the message is sent, this will wait untill the arduino sends feedback that the action is complete irl before moving on 

	"""

	def __init__(self, start, end, stepsmm, g_ser, robot_control):

		self.start = start # initial end effector position, given in tuple (x,y,z)
		self.end = end 	# position to move to, given in tuple (x,y,z)
		self.steps_mm = stepsmm
		self.g_ser = g_ser
		self.rc = robot_control # robot control object passed in

		self.message = ["N","N","N",0,0,0,"r","f","u",1000,1000,500]
		self.message_string = "<N,N,N,0,0,0,n,n,n,0,0,0>"
		self.activate_motor_vars=["X","Y","Z"]
		self.neg_dir_vars = ["l","b","d"] # change direction vars to this if going towards datumn, initially set away	
		
		self.fb = 0

		# flush feedback
		g_ser.flush()

		# calculate instructions

		# if datuming 
		if self.end[0]+self.end[1]+self.end[2] == 0:
			
			# use preset X,Y,Z datum instructions & send it 
			self.zero_xyz()

			# get feedback from gantry
			self.get_g_fb()

			# update robot position to datum
			self.rc.update_robot_position(x=0,y=0,z=0)


		else: 
			
			# loop through each axis and set instructions
			for c in range(0,3): #0=x, 1=y, 2=z

				# if coords aren't the same - i.e. that motor must move
				if self.start[c] != self.end[c]:

					# activte the motor in the instructions
					self.activate_motor(c)

					# set direction instruction to negative (l, b, d) if needed - baseline (r, f, u)
					if self.end[c]<self.start[c]:				
						motor_indx = c
						message_indx = c + 6 # 0=x, 1=y, 2=z
						# set message position 6/7/8 to neg dir var 0/1/2
						self.message[message_indx]=self.neg_dir_vars[motor_indx]

					# set the steps to move 
					self.set_steps_for_motor(c, self.start[c], self.end[c])
				
			#send message
			self.create_string()
			self.send_string() # these are seperate as sending the datum instructions just uses send string, as string to be sent is hard coded
			
			# get feedback from gantry when the action is complete 
			self.get_g_fb()

			# update the robots position 
			self.update_rc_position()

	def update_rc_position(self):
		
		# mm moved in x/y/z
		mx= self.message[3]/self.steps_mm[0]
		my= self.message[4]/self.steps_mm[1]
		mz= self.message[5]/self.steps_mm[2]

		mm = [mx,my,mz] # mm moved 

		np = []

		for c in range(0,3): #0=x, 1=y, 2=z
			if self.end[c]<self.start[c]:
				# lowered position
				n = self.start[c] - mm[c]
				np.append(n)
			else: 
				# position inscreased
				n = self.start[c] + mm[c]
				np.append(n)

		self.rc.update_robot_position(x=np[0],y=np[1],z=np[2])
		print("updated robot position to: ", np)
		print()		


	def get_g_fb(self):
		
		fb = self.g_ser.readline() 
		
		print("Gantry action feedback: ", fb)
		print()
		
		self.fb = fb

	def zero_xyz(self):
		
		# message to send to zero all axis 
		self.message_string = "<zero,zero,zero,900000,900000,900000,l,b,d,100,100,700>" 
		
		self.send_string()

	def neg_motor_direction(self, motor):
		
		motor_indx = motor
		message_indx = motor + 6 # 0=x, 1=y, 2=z
		
		# set message position 6/7/8 to neg dir var 0/1/2
		self.message[message_indx]=self.neg_dir_vars[motor_indx]

	def activate_motor(self,motor):
		
		message_indx=motor # 0=x, 1=y, 2=z
		
		# set message position 0/1/2 to activate motor vars at 0/1/2
		self.message[message_indx]=self.activate_motor_vars[message_indx]

	def set_steps_for_motor(self, motor, start, end):
		
		message_indx = motor + 3
		motor_indx = motor

		# if its going to datum - set as 900000
		if end == 0:
			self.message[message_indx] = 900000
		
		else:
			# calc distance between * steps/mm conversion
			steps = int(math.ceil(abs(end-start)*self.steps_mm[motor_indx])) # rounding up as steps likely to be skipped
			
			# add this to instructions message
			self.message[message_indx] = steps 

	def create_string(self):

		#join message in string
		joined_string = ""		#",".join(str(self.message))

		for element in self.message:
			#make sure all thigs are strings
			string=str(element)
			# add the element as a string
			joined_string += string 
			# add the comma
			joined_string += ","

		#remove last comma
		joined_string = joined_string[:-1]
		#add start and end chars
		self.message_string="<"+joined_string+">"

	def send_string(self):
		
		#convert string value to bytes
		encoded_string = self.message_string.encode('ASCII')
		
		#send values over serial
		time.sleep(1)
		self.g_ser.write(encoded_string)
		time.sleep(1)
		
		print("Encoded message sent to arduino to translate: ",encoded_string)
		print()

		#update instruction sent status
		self.sent=1

def start_sequence_for_vsa(stepsmm, g_ser, robot_control):
	""" initiate start sequence & get screw coords from vision system

		1- moves EE to datum
		2- moved BP to picture height
		3- takes picture - the vision system identifies screw coordinates
		4- moves the BP lower for the EE to pass over


		#### REMOVED ####
		5- pics the first screw coordinate and moves the end effector over it
		####         ####

		returns the reorderd vision system coordinates with Z=110

	"""

	adjustment_array = np.array([40.1,186.7,0])

	rc = robot_control  # robot control object

	# array of positions to move through
	pos = np.array([
		[3,6,0],   # 0, unknown / random start potion
		[0,0,0],   # 1, datum
		[0,0,160], # 2, picture height
		[0,0,110], # 3, height for end effector to move over
		])

	# (1) go to datum
	print()
	print("----------------------------------------------------------")
	print("(1) datum action")
	print("----------------------------------------------------------")
	datum_action = t_instructions(pos[0], pos[1], stepsmm, g_ser, robot_control)


	# (2) then want to move to picture z height (move z up)
	print()
	print("----------------------------------------------------------")
	print("(2) move BP up t picture height (160 mm)")
	print("----------------------------------------------------------")
	pic_height_action = t_instructions(rc.robot_position, pos[2], stepsmm, g_ser, robot_control)


	# (3) take a pic
	print()
	print("----------------------------------------------------------")
	print("(3) take picture")
	print("----------------------------------------------------------")
	rs = main_vision.main_vision()
	

	# (4) move z lower so that the ee can pass over
	print()
	print("----------------------------------------------------------")
	print("(4) move z lower for end effector to pass over & moving end effector to VS datum")
	print("----------------------------------------------------------")
	ee_height_action = t_instructions(rc.robot_position, pos[3], stepsmm, g_ser, robot_control)

	
	#move to VS datum exactly
	g_ser.write(b'<X,Y,N,6130,32048,0,r,f,n,1000,1000,0>')
	# wait for feedback that its there before doing anthing else 
	fb = g_ser.readline() 

	print("Vision datum action feedback: ", fb)

	time.sleep(30)

	#update robot position
	rc.update_robot_position(x=0, y=0)

	#time.sleep(500)

	vsl = [] #vision system screw list

	#combine z and screw coords and append to list

	for i in rs:
		j = np.append(i, 120)
		vsl.append(j)

	# convert screw list to array
	vsa= np.array(vsl)

	print("vs screw coordinates: ", vsa)
	np.savetxt('vs_coords.cvs', vsa, fmt="%d", delimiter=",")
	print()

	# return whole array of screws
	return vsa

def engage(start_z, stepsmm, g_ser, robot_control):

	max_dis = 40 # maximum dispalcement the BP can move up (mm)
	max_pos = start_z+ max_dis  # the max position the BP should end up at (150 mm)

	#flush input buffer
	g_ser.flush()

	# confirm theres nothing in serial port already
	inc_data = g_ser.read(g_ser.inWaiting())
	print("there should be nothing here. Incoming data = ", inc_data)
	print()

	# trigger engagement
	engage = e_instructions(start_z, max_pos, stepsmm, g_ser)	

	# parse feedback from arduino 
	fb = g_ser.readline()		# total recieved feedback:  b'12848\r\n'
	#print("total recieved feedback: ", fb)
	#print()

	# to go from b'12848\r\n' to character as a string
	string_fb = str(fb, 'utf-8')
	#print("string feedback: ", string_fb)		# string feedback:  12848
	#print()
		
	# change from string to int
	steps_moved = int(string_fb)
	print("steps moved: ", steps_moved)
	print()

	# calculate new Z bp position from start Z position, steps moved & steps per mm
	new_bp_pos = start_z + steps_moved/stepsmm[2]
	#print("new bp position: ", new_bp_pos)
	#print()

	# update bp position in the robot controller 
	robot_control.update_robot_position(z=new_bp_pos)


class e_instructions():
	"""
	Creates instructions for gantry arduino to engage end effector with phone/screw
	Takes: 
		- current robot Z position 
		- maximum Z height the baseplate can move to 
		- steps per mm for whole gantry [174,174,321]
		- gantry serial port 
	When this is called, the script will move on to the next line after the instructions have been sent

	"""

	def __init__(self, start_z, max_end_z, stepsmm, g_ser):
		#self.ser = serial.Serial('COM11',9800)

		self.g_ser = g_ser
		self.message = ["N","N","E",0,0,0,"n","n","u",0,0,1000]	
		self.steps_mm = stepsmm 
		self.start = start_z # initial end effector position, given in tuple (x,y,z)
		self.end = max_end_z # maximum end position 

		# calculate instructions and send to arduino
		print("start z height: ", self.start)
		print("max final z height: ", self.end)

		# set the steps to move for the z motor
		self.set_steps_for_motor(2, self.start, self.end)
			
		#send message
		self.create_string()
		self.send_string() 


	def set_steps_for_motor(self, motor, start, end):
		motor_indx = 2 # Z motor is at array position 2 
		message_indx = motor_indx + 3 # index for Z motor steps in message to be sent
		
		# calc (distance between start & end points) * steps/mm 
		steps = int(math.ceil(abs(end-start)*self.steps_mm[2])) # rounding up as steps likely to be skipped
		
		# add this to instructions message
		self.message[message_indx] = steps 

	def create_string(self):
		
		#join message in string
		joined_string = ""

		for element in self.message:
			# change message element to string
			string=str(element)
			# add the element to combined string
			joined_string += string 
			# add the comma between each elements
			joined_string += ","

		#remove last comma
		joined_string = joined_string[:-1]
		#add start and end chars
		self.message_string="<"+joined_string+">"

	def send_string(self):

		#convert string value to bytes
		encoded_string = self.message_string.encode('ASCII')
		#send values over serial
		time.sleep(1)
		self.g_ser.write(encoded_string)
		time.sleep(1)

		print("Encoded message sent to arduino to engage: ", encoded_string)
		print()



if __name__ == "__main__":

	g_ser = serial.Serial('COM11',9600)
	if not g_ser.isOpen():
		g_ser.open()
	print('gantry COM11 is open', g_ser.isOpen())
	print()
	time.sleep(1)

	engage_test(110, [0,0,321.199], g_ser)
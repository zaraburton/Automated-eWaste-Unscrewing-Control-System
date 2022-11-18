import numpy as np
import math
import serial
import time 
import keyboard
import sys

#import main_vision


# variables 
stepsmm = 174.66
#current_position = np.empty([3,1])
datum = np.array([0,0,100])


# number of mm to move in the test
mm_to_move = 58.46


class translate():
	"""translation action, initiated by brain, creates and sends arduino instructions and reads and intreprets serial feedback"""
	def __init__(self, start, end, stepsmm):
		
		self.start = start #start position of end effector
		self.end = end # desired position of end effector (either datum or screw)
		self.stepsmm = stepsmm
		self.state = 0 #0 = to do, 1 = instructions sent & waiting for fb, 2 = didnt go as planned :/ 3 = all good, action succesful 

		self.ard_in = arduino_intructions(self.start, self.end, self.stepsmm)# initiates arduino instructions & sends automatically
		self.message = self.ard_in.message # list of instructions sent

		#self.port = serial.Serial('COM11')

		self.fb_result = self.compare_fb(self.expected_fb(),self.get_stepper_fb())

		if self.fb_result == 1: # 1 = good, expected fb and recieved fb matched
			self.state = 3 # feedback all groovy
			
		if self.fb_result == 0: # 0 = bad, expected fb and recieved fb didnt match
			self.state = 2 # feedback mismatch
	

	## Current calculating expected feedback before message is sent, so doesn't calc it from the final arduino message, it does it from the initial nul one 	
	def expected_fb(self): #serial feedback
		"""calculate expected feedback from arduino, givent he instructions sent"""
		message = self.message  # list of what was sent
		exp_fb = [0,0,0] # list of expected feedback

		#for each motor
		for i in range(0,3):
			# if it wasnt told to move 
			if message[i] == "N":
				exp_fb[i] = 0 # should get back 0 for unmoved
			# or if it was told to go to the datumn
			elif message[i] == "zero":
				exp_fb[i] = 2 # should get back 2 for datumn limit switch hit
			else:
				# should have completed all steps
				exp_fb[i] = 1 # 1 for all steps completed
		#print("expected fb: ", exp_fb)
		return exp_fb

	def get_stepper_fb(self):
		"""parses serial feedback"""
		fb = [] # list of feeback for eaxy stepper [x,y,z]
		# read serial port messages untill got feedback on all positions
		while len(fb)<3: # if havent got feed back on all 3 motors
			ch = ser.read() # characters read on serial
			#print("ch = ser.read(): ", ch)

			# to go from b'character' to character as a string
			string = str(ch, 'utf-8')
			#change from string to int
			number = int(string)
			#letter = int(float(ch)) #.decode('ASCII') # 
			
			fb.append(number)
			#print("arduino returned:", number)
		#print("recieved feedback: ", fb)
		return fb 

	def compare_fb(self, expected, recieved):
		exp = expected
		rec = recieved
		bad = 0
		good = 1
		# compare each character in the string 
		for x, y in zip(exp, rec):
			if x != y:
				#print("fb doesnt match - result =0")
				return bad
		#print("fb matches - good! - result =1")
		return good

class arduino_intructions():
	"""object for the arduino instructions that are made from a start and end point"""

	def __init__(self, start, end, stepsmm):
		#self.ser = serial.Serial('COM11',9800)

		self.sent = 0  #status of message, where 0 = not sent & 1 = sent
		self.message = ["N","N","N",0,0,0,"r","f","u",1000,1000,100]
		self.null_message = ["N","N","N",0,0,0,"n","n","n",0,0,0]
		self.message_string = "<N,N,N,0,0,0,n,n,n,0,0,0>"
		self.steps_mm = stepsmm # passed down from translate class
		self.activate_motor_vars=["X","Y","Z"]
		self.neg_dir_vars = ["l","b","u"] # change direction vars to this if going towards datumn, initially set away	

		self.start = start # initial end effector position, given in tuple (x,y,z)
		self.end = end 	# position to move to, given in tuple (x,y,z)

		# calculate instructions and send to arduino
		if self.sent == 0:
			# if returning to XYZ datum
			if self.end[0]+self.end[1]+self.end[2] == 0:
				# use preset X,Y,Z datum instructions & send it 
				self.zero_xyz()
				self.sent = 1
			# if returning to just XY datum
			elif self.end[0]+self.end[1] == 0:
				# use preset X & Y datum instructions & send it 
				self.zero_xy()
				self.sent = 1

			else: 
				# loop through each axis and set instructions
				for c in range(0,3): #0=x, 1=y, 2=z
					# if no movement required, and coords are the same, the initial null instructions are sent
					# if coords aren't the same
					if self.start[c] != self.end[c]:
						# activte the motor in the instructions
						self.activate_motor(c)
						#if its moving towards the datum
						if self.end[c]<self.start[c]:
							#set the directions to negative
							self.neg_motor_direction(c)
						# set the steps to move 
						self.set_steps_for_motor(c, self.start[c], self.end[c])
						### add in bit for setting speed [] - currently all set to 400ms pd
					
				#send message
				self.create_string()
				self.send_string() # these are seperate as sending the datum unstructions just uses send string, not create
				self.sent = 1

	def zero_xy(self):
		# message to send to zero all axis 
		self.message_string = "<zero,zero,N,900000,900000,900000,l,b,d,100,100,400>" 
		self.send_string()

	def zero_xyz(self):
		# message to send to zero all axis 
		self.message_string = "<zero,zero,zero,900000,900000,900000,l,b,d,100,100,100>" 
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
		ee = start
		scrw = end 
		# if its going to datum - set as 900000
		if end == 0:
			self.message[message_indx] = 900000
		else:
			# calc distance between * steps/mm conversion
			steps = int(math.ceil(abs(scrw-ee)*self.steps_mm)) # rounding up as steps likely to be skipped
			# add this to instructions message
			self.message[message_indx] = steps 

	def calc_steps_all(self,screw_coords, ee_coords):
		screw=screw_coords
		ee=ee_coords
		x_dist= abs(screw[0]-ee[0])*self.steps_mm
		y_dist= abs(screw[1]-ee[1])*self.steps_mm
		#set z distance as just moving down a bit idk ?? zero for now?
		z_dist=0
		return [x_dist,y_dist,z_dist]

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
		ser.write(encoded_string)
		time.sleep(1)
		

		#print(encoded_string)


		#update instruction sent status
		self.sent=1


def kb(current_position): #keyboard press
	
	current_position = current_position

	while True:
		# move backwards the mms to move when b is pressed
		if keyboard.is_pressed("b"):
			print("moving back")
			new_pos = current_position - np.array([0, mm_to_move, 0])
			move_back = translate(current_position, new_pos, stepsmm)
			current_position = move_back.end
		
		# move forwards the mm to move when f is pressed
		if keyboard.is_pressed("f"):
			print("moving forwards")
			new_pos = current_position + np.array([0, mm_to_move, 0])
			move_forwards = translate(current_position, new_pos, stepsmm)
			current_position = move_forwards.end

		# left
		if keyboard.is_pressed("l"):
			print("moving left")
			new_pos = current_position - np.array([mm_to_move, 0, 0])
			move_left = translate(current_position, new_pos, stepsmm)
			current_position = move_left.end

		# right
		if keyboard.is_pressed("r"):
			print("moving right")
			new_pos = current_position + np.array([mm_to_move, 0, 0])
			move_right = translate(current_position, new_pos, stepsmm)
			current_position = move_right.end

		# up
		if keyboard.is_pressed("u"):
			print("moving up")
			new_pos = current_position - np.array([0, 0, mm_to_move])
			move_up = translate(current_position, new_pos, stepsmm)
			current_position = move_up.end

		# down
		if keyboard.is_pressed("d"):
			print("moving down")
			new_pos = current_position + np.array([0, 0, mm_to_move])
			move_down = translate(current_position, new_pos, stepsmm)
			current_position = move_down.end

		# print current position & EXIT
		if keyboard.is_pressed("p"):
			print(current_position)
			sys.exit(0) 



if __name__ == "__main__":

	# establish serial port connection to arduino
	ser = serial.Serial('COM16',9600)
	if not ser.isOpen():
		ser.open()
	print('com16 is open', ser.isOpen())
	time.sleep(1)


	##############################
	#	Comment this in / out as needed		# 
	##############################

	# zero the gantry
	#datum_action = translate(current_position, datum, stepsmm)
	# update current position
	#current_position = datum_action.end

	#move to testing position
	#test_pos = np.array([90,150,0])
	#centering_action = translate(current_position, test_pos, stepsmm)
	# update current positon
	#current_position = centering_action.end

	current_position = np.array([90,114,60])
	# move based on different keyboard presses 
	kb(current_position)







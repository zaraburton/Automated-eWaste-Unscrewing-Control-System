import numpy as np
import math
import serial
import time 
import argparse
import keyboard
import sys


import gantry_control as gc 
import main_vision as vision
import unscrew as usc #unscrew control


def main_test1():

	# set lists as fake serial ports to append messages to 

	# open gantry serial port 
	g_ser = serial.Serial('COM16',9600)
	if not g_ser.isOpen():
		g_ser.open()
	print('gantry COM16 is open', g_ser.isOpen())
	time.sleep(1)



	# open DC motor arduino serial port
	dc_ser = 0

	# open multimeter serial port
	mm_ser = 0

	stepsmm = [174.7789337, 173.1400966, 321.199]

	# initiate robot control class 
	rc = robot_controller(g_ser, dc_ser, stepsmm)


def main():

	# open gantry serial port 
	g_ser = serial.Serial('COM16',9600)
	if not g_ser.isOpen():
		g_ser.open()
	print('gantry COM16 is open', g_ser.isOpen())
	time.sleep(1)

	# open DC motor arduino serial port
	dc_ser = serial.Serial("COM13", 9600)
	if not dc_ser.isOpen():
		dc_ser.open()
	print('dc motor COM13 is open', dc_ser.isOpen())
	time.sleep(1)

	# open multimeter serial port
	#mm_ser = serial.Serial("COM??", 9600)
	#if not mm_ser.isOpen():
		#mm_ser.open()
	#print('multimeter COM?? is open', mm_ser.isOpen())
	#time.sleep(1)

	stepsmm = [174.7789337, 173.1400966, 321.199] # used for testing 

	# initiate robot control class 
	rc = robot_controller(g_ser, dc_ser, stepsmm)


class robot_controller():
	"""
	BTW - throughout this, states follow the same key:
		0 = unvisited / not doing anything about this yet
		1 = attempting point got from vision system
		2 = attempting point generated from spiral 
		3 = FAIL
		4 = SUCESS
		5 = abandoned by user
	unscrewing results key:
		1 = failed to engage
		2 = failed to unscrew 
		3 = unscrewed sucessfully
		4 = point abandoned (when instructed by user)
	"""
	def __init__(self, g_ser, dc_ser, stepsmm):

		self.g_ser = g_ser # gantry serial port
		self.dc_ser = dc_ser # dc motor serial port
		
		self.stepsmm = stepsmm # steps per mm for [X,Y,Z] axis

		self.vision_system_screws = []
		self.robot_position = np.empty((3))

		self.total_screws = 0 #
		self.current_attempt = 0 # tracking the number of times a particular screw has been tried
		self.screw_counter = 0  # tracking which screw the robot is trying to find (initially screw 0, )
		self.spiral_points = [] # arrray of new spiral points to try 
		self.screw_attempts = 0 # counter to track which spiral points being tried now
		self.max_spiral_points = 40 # maximum number of points to try for each screw 
		self.above_screw_pos = 0 # X,Y,Z position at Z=110 above the current point 
	


		# on startup - excecute start sequence to get screw coordinates from the vision system 
		# start sequence = moves to first screw and returns all vision system screw coords at 110 BP height
		print("Commencing start up sequence")
		vsa = gc.start_sequence_for_vsa(self.stepsmm, self.g_ser, self) #vision system array

		print("vs screw coordinates: ", vsa)
		#np.savetxt('vs_coords.cvs', vsa, fmt="%d", delimiter=",")
		print()
		
		self.total_screws = vsa.shape[0]  # number of screws found by vision system
		self.spiral_points = 40 # number of points to try for spiralling

		# create array of all possible possitions to try for all screws
		s = (self.spiral_points, self.total_screws, 3) # shape of array
		ap = np.ones(shape=(s), dtype=np.longfloat) # empty array

		for i in range(0, self.total_screws):
			
			# calculate the spiral coords for each screw point
			spiral = self.calc_spiral_set(vsa[i], self.spiral_points)  
			
			for j in range(0, self.spiral_points):
				# add each spiral point to array of all points
				ap[j][i] = spiral[j]

		self.all_points = ap
		print("All points which may be attempted: ", self.all_points)
		print()

		self.results_tracker = np.zeros((self.spiral_points, self.total_screws)) # array to track result of each position 
		print("Initial resuts tracker:", self.results_tracker)

		# for each screw found by the vision system - try and engage & unscrew it 
		while self.screw_counter < self.total_screws:

			if self.screw_counter > self.total_screws:
				# break out of loop when done with all screws
				break

			# from above phone, go over to next point
			print()
			print("----------------------------------------------------------")
			print("(5) moving to screw number:", self.screw_counter, "  attempt number: ", self.screw_attempts)
			print("----------------------------------------------------------")
			gc.t_instructions(self.robot_position, self.all_points[self.screw_attempts][self.screw_counter], self.stepsmm, self.g_ser, self)
		
			# engage with screw (this updates bp position)
			print()
			print("----------------------------------------------------------")
			print("(6) engaging with phone")
			print("----------------------------------------------------------")
			gc.engage(self.robot_position[2], self.stepsmm, self.g_ser, self)   # def engage(start_z, stepsmm, g_ser, robot_control):

			# call effector script 
			print()
			print("----------------------------------------------------------")
			print("(7) calling end-effector script")
			print("----------------------------------------------------------")
			end_eff_results = usc.get_end_effector_results(self.dc_ser, self) # 3 = fail, 4 = success # set screw one result to this 



			if end_eff_results == 1: # if engagement FAILED the first time -- spiral


				# disengage - move bp to 110  // translate(current pos, next pos, stepsm, g_ser)
				print()
				print("----------------------------------------------------------")
				print(" Engagement failed ==> Moving to next spiral search point")
				print(" (8) disengaging with screw")
				print("----------------------------------------------------------")
				
				gc.t_instructions(self.robot_position, self.all_points[self.screw_attempts][self.screw_counter], self.stepsmm, self.g_ser, self)

				# set results of current screw to failed
				self.results_tracker[self.screw_attempts][self.screw_counter] = 3 

				# track number of engagement attempts for current screw
				self.screw_attempts += 1

				# set state of screw search to spiralling for the next screw
				self.results_tracker[self.screw_attempts][self.screw_counter] = 2 

				print("Results tracker: ", self.results_tracker)
				print()

				# will now go back to (5) for the same screw but a different point
				


			if end_eff_results == 2: # if unscrewing failed but engaged sucessfylly / abandoning screw
				
				# record screw failure
				self.results_tracker[self.screw_attempts][self.screw_counter] = 3

				# disengage & change bp position
				print()
				print("----------------------------------------------------------")
				print(" Unscrewing failed ==> Moving to next screw")
				print(" (8) disengaging with screw")
				print("----------------------------------------------------------")
				
				gc.t_instructions(self.robot_position, self.all_points[self.screw_attempts][self.screw_counter], self.stepsmm, self.g_ser, self)

				# move to next screw
				self.screw_counter += 1

				# reset screw attempts for next screw
				self.screw_attempts = 0

				# set results for next screw to 1 = attempting point from vision system
				self.results_tracker[self.screw_attempts][self.screw_counter] = 1

				print(" Results tracker: ", self.results_tracker)
				print()

				# will now go back to (5) for a new screw at the vision system point


			if end_eff_results == 4: #  user input to abandon screw / vs false positive
				
				# record abandoning screw
				self.results_tracker[self.screw_attempts][self.screw_counter] = 5

				# disengage & change bp position
				print()
				print("----------------------------------------------------------")
				print(" Abandoning this point ==> Moving to next screw")
				print(" (8) disengaging with screw")
				print("----------------------------------------------------------")
				
				gc.t_instructions(self.robot_position, self.all_points[self.screw_attempts][self.screw_counter], self.stepsmm, self.g_ser, self)

				# move to next screw
				self.screw_counter += 1

				# reset screw attempts for next screw
				self.screw_attempts = 0

				# set results for next screw to 1 = attempting point from vision system
				self.results_tracker[self.screw_attempts][self.screw_counter] = 1

				print("Results tracker: ", self.results_tracker)
				print()

				# will now go back to (5) for a new screw at the vision system point

			if end_eff_results == 3: # SUCESSFUL screw removal 

				# record success
				self.results_tracker[self.screw_attempts][self.screw_counter] = 4

				# track number of engagement attempts for current screw
				self.screw_attempts += 1

				# disengage - move BP down to Z=110 
				print()
				print("----------------------------------------------------------")
				print(" Screw successfulling removed ==> Moving to next screw")
				print(" (8) disengaging with screw")
				print("----------------------------------------------------------")
				
				gc.t_instructions(self.robot_position, self.all_points[self.screw_attempts][self.screw_counter], self.stepsmm, self.g_ser, self)

				# ask for the screw to be removed from the end effector 
				remove_screw()

				# add 1 to screw counter to select next screw in loop 
				self.screw_counter += 1

				# reset screw attempts for the next screw to start at 0
				self.screw_attempts = 0

				# set results for next screw to 1 = attempting point from vision system
				self.results_tracker[self.screw_attempts][self.screw_counter] = 1

				print("Results tracker: ", self.results_tracker)
				print()

				# will now go back to (5) for a new screw at the vision system point

		# print results 
		self.print_results()
		print("fin.")

	def print_results(self):

		print("Final results: ", self.results_tracker)
		r = self.results_tracker.reshape((self.all_points*3, self.total_screws))
		np.savetxt('point_results.cvs', r, fmt="%d", delimiter=",")
		np.savetxt('all_points.cvs', self.all_points, fmt="%d", delimiter=",")
		print("Saved results to CVS")
		print("fin.")		

	def update_robot_position(self, **kwargs):

		# get updated values of x,y,z
		x = kwargs.get('x', None)
		y = kwargs.get('y', None)
		z = kwargs.get('z', None)

		new_pos = [x,y,z]

		# append any changed values to robot position
		for i in range(0,3):
			if new_pos[i] != None:
				self.robot_position[i] = new_pos[i]

		print("updated robot position: ", self.robot_position)
		print()

	def calc_spiral_set(self, current_position, spiral_points):

		# lists to store x and y axis points 
		xdata, ydata = [], [] 

		# get data points 
		for i in range(0,spiral_points): 

			#ARCHIMEDES SPIRAL
			r = 0.6+0.075*i


			# x, y values to be plotted 
			x = r*np.sin(r/0.1) 
			y = r*np.cos(r/0.1) 

			# appending new points to x, y axes points list 
			xdata.append(x) 
			ydata.append(y) 

		# combining into one array of all spiral points
		sp1 = np.vstack((xdata, ydata)).T

		# adding 0 on for z positon
		sp2 = []
		for i in sp1:
			j = np.append(i, 0)
			sp2.append(j)
		#convert list to array
		sp3 = np.array(sp2)
		#print(sp3)

		# array of 19 same positions to add to spiral coords
		cp = np.tile(current_position, (20,1))

		spiral_set = cp + sp3 

		return spiral_set



		
if __name__ == "__main__":

    main()


















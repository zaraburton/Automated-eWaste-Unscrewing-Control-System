import serial
import time
import keyboard
import sys
import numpy as np

def get_end_effector_results(dc_ser, results_tracker):
	"""
	initiated when end effector pressed into screw/phone
		- unscrews slowly
		- checks for engagement
		- if failed 
			- pauses unscrewing
			- returns (1) engagement failed
		- if sucessfull
			- unscrews fast
			- checks for screw removal
			- if removal sucessful:
				- pauses unscrewing
				- returns (3) for removal sucessful
			- if removal fails:
				- pauses unscrewing
				- returns (2) for removal fails

	"""

	# unscrew slowly
	unscrew("S", dc_ser)

	result = 0 # result variable returned to the main controller

	#check engagement
	print("Has end-effector engaged Y/N? Press X to abandon this point. Press E to save results and exit.")
	while True:
		if keyboard.is_pressed("Y"):
			break	

		if keyboard.is_pressed("N"):
			unscrew("P", dc_ser)
			result = 1 # engagement fail
			break

		if keyboard.is_pressed("X"):

			unscrew("P", dc_ser)
			result = 4 # abandon point
			break


	# try to remove screw if engaged successfully
	if result == 0:
		unscrew("F", dc_ser)

		#check if screws been removed
		print("Press Y when the screw is removed. Press N if the end effector fails to remove the screw. Press X to abandon this point.")
		while True:
			if keyboard.is_pressed("Y"):
				unscrew("S", dc_ser)
				print("Press P to stop at the right place")
				while True:
					if keyboard.is_pressed("P"):
						unscrew("P", dc_ser)
						result = 3 # removal sucess
						break	
				break

			if keyboard.is_pressed("N"):
				unscrew("S", dc_ser)
				print("Press P to stop at the right place")
				while True:
					if keyboard.is_pressed("P"):
						unscrew("P", dc_ser)
						result = 2 # removal fail
						break
				break	

			if keyboard.is_pressed("X"):
				unscrew("S", dc_ser)
				print("Press P to stop at the right place")
				while True:
					if keyboard.is_pressed("P"):
						unscrew("P", dc_ser)
						result = 4 # abandon point
						break
				break	

	return result


def unscrew(speed, dc_ser):
	""" Sends instructions to dc motor arduino to go slow, fast or pause unscrewing"""


	# messages to send to DC motor arduino
	us_slow = "S"
	us_fast = "F"
	us_pause = "P"


	if speed == us_slow:
		# convert string to bytes
		ms = "<"+us_slow+">"
		encoded_string = ms.encode('ASCII')

		time.sleep(1)

		#send value over serial
		dc_ser.write(encoded_string)
		print(encoded_string)

	if speed == us_fast:
		# convert string to bytes
		ms = "<"+us_fast+">"
		encoded_string = ms.encode('ASCII')

		time.sleep(1)

		#send value over serial
		dc_ser.write(encoded_string)
		print(encoded_string)

	if speed == us_pause:
		# convert string to bytes
		ms = "<"+us_pause+">"
		encoded_string = ms.encode('ASCII')

		time.sleep(1)

		#send value over serial
		dc_ser.write(encoded_string)
		print(encoded_string)



if __name__ == "__main__":

	# open DC motor arduino serial port
	dc_ser = serial.Serial("COM13", 9600)
	if not dc_ser.isOpen():
		dc_ser.open()
	print('dc motor COM13 is open', dc_ser.isOpen())
	time.sleep(1)

	get_end_effector_results(dc_ser)

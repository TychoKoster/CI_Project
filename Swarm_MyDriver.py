from pytocl.driver import Driver
from pytocl.car import State, Command
from pykeyboard import PyKeyboard

import pickle
import math
import numpy as np
import pyautogui

class MyDriverMLP(Driver):
	def __init__(self):
		fi = open("currentmodel.p",  "rb")
		self.alt_model = pickle.load(fi)
		fi.close()		

	# Override the `drive` method to create your own driver
	def drive(self, carstate: State) -> Command:
		command = Command()
		
		speed_x = carstate.speed_x
		speed_y = carstate.speed_y
		speed_z = carstate.speed_z
		speed = math.sqrt(speed_x**2 + speed_y**2 + speed_z**2)
		distance = carstate.distance_from_start
		distance_raced = carstate.distance_raced
		curlaptime = carstate.current_lap_time
		lastlaptime = carstate.last_lap_time
		time =  curlaptime
		track_position = carstate.distance_from_center
		
		angle = carstate.angle
		
		track_edges = carstate.distances_from_edge

		input_data = [speed, track_position, angle]
		for edge in track_edges:
			input_data.append(edge)

		opponents = carstate.opponents
		for i in range(9, len(opponents), 9):
			input_data.append(opponents[i])

		input_data = np.reshape(input_data, (1,len(input_data)))

		output = self.alt_model.predict(input_data)

		acceleration = output[0][0]
		brake = output[0][1]
		steering = output[0][2]
		



		if acceleration > 0:
			if carstate.rpm > 8000:
				command.gear = carstate.gear + 1

		if carstate.rpm < 2500:
			command.gear = carstate.gear - 1

		if not command.gear:
			command.gear = carstate.gear or 1

		if track_edges[9] < 130.0 and track_edges[9] > 80.0:
			if speed > 40:
				acceleration = 0
				brake = 0.05
		elif track_edges[9] < 80 and track_edges[9] > 40:
			if speed > 25:
				acceleration = 0
				brake = 0.05
		elif track_edges[9] < 40:
			if speed > 15:
				acceleration = 0
				brake = 0.05
		if speed > 30:
			acceleration = 0
			brake = 0.05

		command.accelerator = acceleration
		command.brake = brake 
		command.steering = steering

		# To train:
		#if time > 6 and distance_raced > 80 and distance > 20:
		#	if lastlaptime < 2:
		#		fitness = (distance*distance)/(time*1000.)
		#	else:
		#		fitness = 200
		#		print("Stop") 
		#		print(fitness)
		#		fi = open("fitness.p","wb")
		#		pickle.dump(fitness, fi)
		#		fi.close()				
		#		pyautogui.press("esc")
		#		pyautogui.press("down")
		#		pyautogui.press("enter")
		#		pyautogui.press("down")
		#		pyautogui.press("enter")
		#		pyautogui.press("right")
		#		pyautogui.press("enter")
		#		pyautogui.press("enter")
		#		pyautogui.press("enter")
		#		pyautogui.press("up")
		#		pyautogui.press("enter")
		#		exit(0)
		#else:
		#	fitness = 0
		#print(distance)
		#print(fitness)

		#if abs(angle) >= 80:
		#	print("Stop") 
		#	print(fitness)
		#	fi = open("fitness.p","wb")
		#	pickle.dump(fitness, fi)
		#	fi.close()
		#	pyautogui.press("esc")
		#	pyautogui.press("enter")
		#	exit(0)
		#elif time > 5 and speed < 2:
		#	print("Stop") 
		#	print(fitness)
		#	fi = open("fitness.p","wb")
		#	pickle.dump(fitness, fi)
		#	fi.close()				
		#	pyautogui.press("esc")
		#	pyautogui.press("enter")
		#	exit(0)
		#elif time > 400:
		#	print("Stop2")
		#	print(fitness)
		#	fitness = 250
		#	fi = open("fitness.p","wb")
		#	pickle.dump(fitness, fi)
		#	fi.close()
		#	pyautogui.press("esc")
		#	pyautogui.press("enter")
		#	exit(0)

		#print(track_edges[9])
		#print(command)

		return command

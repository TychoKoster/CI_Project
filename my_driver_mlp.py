from pytocl.driver import Driver
from pytocl.car import State, Command

import threading
import pickle
import math
import numpy as np
import communication as c

class MyDriverMLP(Driver):
	def __init__(self):
		self.model = pickle.load(open("MLPR.p", "rb"))
		self.alt_model = pickle.load(open("MLPR_alt.p", "rb"))
		self.opponents_model = pickle.load(open("MLPR_no_opponents.p", "rb"))

	# Override the `drive` method to create your own driver
	def drive(self, carstate: State) -> Command:
		# threading.Thread(target=c.communicate, args=(carstate, "communication.csv")).start()
		command = Command()
		
		speed_x = carstate.speed_x
		speed_y = carstate.speed_y
		speed_z = carstate.speed_z
		speed = math.sqrt(speed_x**2 + speed_y**2 + speed_z**2)

		track_position = carstate.distance_from_center
		
		angle = carstate.angle
		
		track_edges = carstate.distances_from_edge

		input_data = [speed, track_position, angle]
		for edge in track_edges:
			input_data.append(edge)

		opponents = carstate.opponents
		for i in range(0, len(opponents), 4):
			input_data.append(opponents[i])

		input_data = np.reshape(input_data, (1,len(input_data)))

		# output = self.model.predict(input_data)
		# output = self.alt_model.predict(input_data)
		output = self.opponents_model.predict(input_data)

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
		elif track_edges[9] < 60 and track_edges[9] > 40:
			if speed > 25:
				acceleration = 0
				brake = 0.05
		elif track_edges[9] < 40:
			if speed > 15:
				acceleration = 0
				brake = 0.05

		command.accelerator = acceleration
		command.brake = brake 
		command.steering = steering
		
		return command

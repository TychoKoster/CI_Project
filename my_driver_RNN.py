from pytocl.driver import Driver
from pytocl.car import State, Command
from keras.models import load_model
from sklearn.externals import joblib

import math
import numpy as np

class MyDriver(Driver):
	def __init__(self):
		self.model = load_model('lstm.h5')
		self.lstm_model = load_model('lstm_50_epochs.h5')
		self.dense_model = load_model('dense.h5')
		self.data_logger = None

	# Override the `drive` method to create your own driver
	def drive(self, carstate: State) -> Command:
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

		input_data = np.reshape(input_data, (1, 22, 1))

		# output = self.model.predict(input_data)
		# output = self.dense_model.predict(input_data)
		# output = self.lstm_model.predict(input_data)

		acceleration = output[0][0]
		brake = output[0][1]
		steering = output[0][2]
		
		if acceleration > 0.5:
			brake = 0
		else:
			acceleration = 0
		
		if acceleration > 0:
			if carstate.rpm > 8000:
				command.gear = carstate.gear + 1

		if carstate.rpm < 2500:
			command.gear = carstate.gear - 1

		if not command.gear:
			command.gear = carstate.gear or 1

		command.accelerator = acceleration
		command.brake = brake 
		command.steering = steering

		return command

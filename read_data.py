from collections import defaultdict
import numpy as np
import pandas
import os


def read_data(path):
	input_data = np.array([])
	output_data = np.array([])
	category_index_input = dict()
	category_index_output = dict()
	for file in os.listdir(path):
		if file.endswith('.csv'):
			file_path = path + file
			dataframe = pandas.read_csv(file_path)
			dataset = dataframe.values
			if not output_data.any():
				output_data = dataset[:,0:3]
				input_data = dataset[:,3:]
			else:
				output_data = np.append(output_data, dataset[:,0:3], axis=0)
				input_data = np.append(input_data, dataset[:,3:], axis=0)
	no_opponents = np.array([200.0] * 3)
	input_data_opponents = []
	for i in range(len(input_data)):
		input_data_opponents.append(np.concatenate((input_data[i], no_opponents)))
	# Set category indices

	return input_data, output_data, np.array(input_data_opponents)
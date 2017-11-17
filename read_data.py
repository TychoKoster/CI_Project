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
	# Set category indices
	data_types = dataframe.columns
	input_categories = data_types[3:]
	output_categories = data_types[0:3]
	for i, category in enumerate(input_categories):
		category_index_input[category] = i
	for i,category in enumerate(output_categories):
		category_index_output[category] = i
	return category_index_input, category_index_output, input_data, output_data
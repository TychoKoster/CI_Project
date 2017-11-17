from collections import defaultdict
import csv
import os


def read_data(path):
	input_data = []
	output_data = []
	category_index_input = defaultdict(str)
	category_index_output = defaultdict(str)
	for file in os.listdir(path):
		if file.endswith('.csv'):
			file_path = path + file
			with open(file_path, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				# Skip category names
				row1 = next(reader)
				for row in reader:
					output_data.append(row[0:3])
					input_data.append(row[3:])
	# Set category indices
	input_categories = row1[0:3]
	output_categories = row1[3:]
	for i, category in enumerate(input_categories):
		category_index_input[category] = i
	for i,category in enumerate(output_categories):
		category_index_output[category] = i
	return category_index_input, category_index_output, input_data, output_data
from collections import defaultdict
import csv
import os


def read_data(path):
	data = []
	category_index = defaultdict(str)
	for file in os.listdir(path):
		if file.endswith('.csv'):
			file_path = path + file
			with open(file_path, 'r') as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				# Skip category names
				row1 = next(reader)
				for row in reader:
					data.append(row)
	# Set category indices
	for i, category in enumerate(row1):
		category_index[category] = i
	return category_index, data
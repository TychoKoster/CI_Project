import read_data as rd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.utils import shuffle
import numpy as np


def main():
	# Uncomment for data With added opponent data
	_, output_data, input_data = rd.read_data("train_data/")

	# Uncomment for data without added opponent data
	# input_data, output_data, _ = rd.read_data("train_data/")
	
	# input_data, output_data = shuffle(input_data, output_data)
	X_train, X_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.2)
	
	

	models = []
	for i in range(1):
		# Best architecture for no opponent data
		# MLPR = MLPRegressor(hidden_layer_sizes=(100, 20), activation='tanh', solver='lbfgs', alpha=0.0005, max_iter=2000, random_state=42)
		
		# Best architecture for 9 opponent data
		MLPR = MLPRegressor(hidden_layer_sizes=(250, 70), activation='tanh', solver='lbfgs', alpha=0.0005, max_iter=3000, random_state=42)

		MLPR.fit(X_train, y_train)
		print(MLPR.score(X_train, y_train))
		print(MLPR.score(X_test, y_test))
		models.append((MLPR, MLPR.score(X_train, y_train) + MLPR.score(X_test, y_test)))
	models.sort(key=lambda x:x[1], reverse=True)

	pickle.dump(models[0][0], open('torcs-server/torcs-client/MLPR_no_opponents.p', 'wb+'))

if __name__ == '__main__':
	main()
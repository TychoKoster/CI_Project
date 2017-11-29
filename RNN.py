import read_data as rd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
	
from keras.models import Model, Sequential, load_model
from keras.layers import Input, SimpleRNN, Embedding, LSTM, Dense, concatenate, Activation, Flatten
from keras.optimizers import TFOptimizer
from sklearn.preprocessing import scale, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib


def LSTM_network(path, x, y):
	x = np.reshape(x, (x.shape[0], 22, 1))
	X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
	
	input_layer = Input(shape=(22,1))

	hidden = LSTM(22, input_shape=(22,1))(input_layer)

	hidden = Dense(90, activation='relu')(hidden)
	
	# Output layers
	acceleration = Dense(1, activation='sigmoid')(hidden)
	brake = Dense(1, activation='sigmoid')(hidden)
	steering = Dense(1, activation='tanh')(hidden)

	output_layer = concatenate([acceleration, brake, steering])

	# Compile model
	model = Model(inputs=input_layer, outputs=output_layer)

	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(x, y, epochs=100, batch_size=32, verbose=1)

	print(model.evaluate(X_train, y_train))
	print(model.evaluate(X_test, y_test))

	model.save(path)	
	
	return model

def Dense_network(path, x, y):
	x = np.reshape(x, (x.shape[0], 22, 1))
	X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

	model = Sequential()
	model.add(Dense(22, input_shape=(22,1)))
	model.add(Activation('relu'))
	model.add(Dense(100))
	model.add(Activation('relu'))
	model.add(Dense(50))
	model.add(Activation('relu'))
	model.add(Flatten())
	model.add(Dense(3, activation='sigmoid'))

	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(X_train, y_train, epochs=100, batch_size=32, verbose=0)

	print(model.evaluate(X_train, y_train))
	print(model.evaluate(X_test, y_test))

	model.save(path)	

def main():
	path = os.getcwd()
	data_path = os.path.join(path, 'train_data/')
	lstm_path = os.path.join(path, 'torcs-server/torcs-client/lstm.h5')
	dense_path = os.path.join(path, 'torcs-server/torcs-client/dense.h5')

	category_index_input, category_index_output, input_data, output_data = rd.read_data(data_path)

	# LSTM_network(lstm_path, input_data, output_data)
	Dense_network(dense_path, input_data, output_data)

if __name__ == '__main__':
	main()
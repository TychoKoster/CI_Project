import read_data as rd
import numpy as np
import matplotlib.pyplot as plt
import timeit
import math
	
from keras.models import Model, Sequential, load_model
from keras.layers import Input, Embedding, LSTM, Dense, concatenate
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize

def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped


def LSTM_network(x, y, x_test, y_test):
	input_layer = Input(shape=(22,))
	embedded_layer = Embedding(22, 3)(input_layer)

	lstm_layer = LSTM(3)(embedded_layer)
	
	# Output layers
	acceleration = Dense(1, activation='sigmoid')(lstm_layer)
	brake = Dense(1, activation='sigmoid')(lstm_layer)
	steering = Dense(1, activation='tanh')(lstm_layer)

	output_layer = concatenate([acceleration, brake, steering])

	# Compile model
	model = Model(inputs=input_layer, outputs=output_layer)

	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(x, y, epochs=1, batch_size=1, verbose=1, validation_data=(x_test, y_test))
	model.save('lstm.h5')	
	
	return model


def main():
	path = '/home/jterstall/Documents/CI/CI_Project/train_data/'
	category_index_input, category_index_output, input_data, output_data = rd.read_data(path)
	x, x_test, y, y_test = train_test_split(input_data, output_data, test_size=0.2)
	x = normalize(x)
	y = normalize(y)
	# model = LSTM_network(x, y, x_test, y_test)
	model = load_model('lstm.h5')

if __name__ == '__main__':
	main()
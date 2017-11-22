import read_data as rd
import numpy as np
import matplotlib.pyplot as plt
import math
	
from keras.models import Model, Sequential, load_model
from keras.layers import Input, Embedding, LSTM, Dense, concatenate
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize, scale, MinMaxScaler


def LSTM_network(x, y, x_test, y_test):
	x = np.reshape(x, (x.shape[0], 22, 1))
	input_layer = Input(shape=(22,1))

	hidden = Dense(15, input_shape=(22,1), activation='relu')(input_layer)
	hidden = LSTM(15, return_sequences=True)(hidden)

	lstm_layer = LSTM(3)(hidden)
	
	# Output layers
	acceleration = Dense(1, activation='sigmoid')(lstm_layer)
	brake = Dense(1, activation='sigmoid')(lstm_layer)
	steering = Dense(1, activation='tanh')(lstm_layer)

	output_layer = concatenate([acceleration, brake, steering])

	# Compile model
	model = Model(inputs=input_layer, outputs=output_layer)

	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(x, y, epochs=10, batch_size=32, verbose=1)
	model.fit(x, y, epochs=10, batch_size=32, verbose=1, validation=(x_test, y_test))
	model.save('/home/jterstall/Documents/CI/CI_Project/torcs-server/torcs-client/lstm.h5')	
	
	return model

def LSTM_network2(x, y, x_test, y_test):
	x = np.reshape(x, (x.shape[0], 22, 1))
	model = Sequential()
	model.add(LSTM(22, input_shape=(22,1)))
	model.add(Dense(15, activation='relu'))
	model.add(Dense(3))
	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(x, y, epochs=5, batch_size=32, verbose=1)
	# model.fit(x, y, epochs=5, batch_size=32, verbose=1, validation=(x_test,y_test))
	model.save('/home/jterstall/Documents/CI/CI_Project/torcs-server/torcs-client/lstm.h5')	
	return model

def main():
	path = '/home/jterstall/Documents/CI/CI_Project/train_data/'
	category_index_input, category_index_output, input_data, output_data = rd.read_data(path)
	input_data, test_input, output_data, test_output = train_test_split(input_data, output_data, test_size=0.1)
	input_data = scale(input_data)
	output_data = scale(output_data)
	model = LSTM_network(input_data, output_data, test_input, test_output)
	# model = LSTM_network2(input_data, output_data, test_input, test_output)

if __name__ == '__main__':
	main()
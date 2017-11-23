import read_data as rd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
	
from keras.models import Model, Sequential, load_model
from keras.layers import Input, Embedding, LSTM, Dense, concatenate
from sklearn.preprocessing import scale, StandardScaler
from sklearn.externals import joblib


def LSTM_network(path, x, y):
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
	model.fit(x, y, epochs=1, batch_size=32, verbose=1, validation_split=0.1)

	model.save(path)	
	
	return model

def LSTM_network2(path, x, y):
	x = np.reshape(x, (x.shape[0], 22, 1))
	model = Sequential()
	model.add(LSTM(22, input_shape=(22,1)))
	model.add(Dense(15, activation='relu'))
	model.add(Dense(3))
	model.compile(loss='mean_squared_error', optimizer='adam')
	model.fit(x, y, epochs=5, batch_size=32, verbose=1, validation_split=0.1)
	model.save(path)	
	return model

def main():
	path = os.getcwd()
	data_path = os.path.join(path, 'train_data/')
	model_path = os.path.join(path, 'torcs-server/torcs-client/lstm.h5')
	scaler_path = os.path.join(path, 'torcs-server/torcs-client/scaler.pkl')
	category_index_input, category_index_output, input_data, output_data = rd.read_data(data_path)
	scaler = StandardScaler()
	scaler.fit(input_data)
	input_data = scaler.transform(input_data)
	joblib.dump(scaler, scaler_path)

	model = LSTM_network(model_path, input_data, output_data)
	# model = LSTM_network2(model_path, input_data, output_data)

if __name__ == '__main__':
	main()
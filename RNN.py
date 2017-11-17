import read_data as rd
import numpy as np
import timeit

from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def wrapper(func, *args, **kwargs):
	def wrapped():
		return func(*args, **kwargs)
	return wrapped


def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(22, input_dim=22, kernel_initializer='normal', activation='relu'))
	model.add(Dense(3, kernel_initializer='normal'))
	# Compile model
	model.compile(loss='mean_squared_error', optimizer='adam')
	return model


def test_keras(input_data, output_data):
	# evaluate model with standardized dataset
	# fix random seed for reproducibility
	seed = 7
	np.random.seed(seed)
	# evaluate model with standardized dataset
	estimator = KerasRegressor(build_fn=baseline_model, nb_epoch=100, batch_size=5, verbose=0)
	kfold = KFold(n_splits=10, random_state=seed)
	results = cross_val_score(estimator, input_data, output_data, cv=kfold)
	
	print("Results: %.2f (%.2f) MSE" % (results.mean(), results.std()))


def main():
	path = '/home/jterstall/Documents/CI/CI_Project/train_data/'
	category_index_input, category_index_output, input_data, output_data = rd.read_data(path)
	wrapped = wrapper(test_keras, input_data, output_data)
	print(timeit.timeit(wrapped, number=1))

if __name__ == '__main__':
	main()
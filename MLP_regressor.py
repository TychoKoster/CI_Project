import read_data as rd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor


def main():
	category_index_input, category_index_output, input_data, output_data = rd.read_data("train_data/")
	X_train, X_test, y_train, y_test = train_test_split(input_data, output_data, test_size=0.2)
	
	MLPR = MLPRegressor(hidden_layer_sizes=(100, 20), activation='tanh', solver='lbfgs', alpha=0.0005, max_iter=2000, random_state=42)
	MLPR.fit(X_train, y_train)
	
	print(MLPR.score(X_train, y_train))
	print(MLPR.score(X_test, y_test))

	pickle.dump(MLPR, open('torcs-server/torcs-client/MLPR_alt.p', 'wb+'))

if __name__ == '__main__':
	main()
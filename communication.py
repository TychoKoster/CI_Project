import csv
import numpy as np
import timeit

def communicate(carstate, path):
	state = list(carstate.opponents)
	state.extend([carstate.distance_from_center])
	state.extend([carstate.distance_from_start])
	state.extend(carstate.distances_from_edge)

	# np.save("communication.npy", np.array(state))
	with open(path, 'w') as f:
		carstate_writer = csv.writer(f, delimiter=',')
		carstate_writer.writerow(state)
			
	
def listen(path):
	with open(path, 'r+') as f:
		print(type(f.read()))
	print("hello ? thanks")
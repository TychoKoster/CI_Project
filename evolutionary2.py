#! /usr/bin/env python3

import numpy as np
import pickle
import random
import os

MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.6
POPULATION_SIZE = 10

def main():
	model = pickle.load(open("MLPR_alt.p", "rb"))

	population = [model, model, model, model, model, model, model, model, model, model]
	population[1:10] = diversity(population)
	population[0] = model
	population, fitness = test(population)
	new_population = selection(population,fitness)
	population = crossover(new_population)	
	population = mutate(population)
	pickle.dump(population, open("population.p","wb"))	
	

	# # Input
	# print(len(weights[0]))

	# # Input -> 1st hidden
	# print(len(weights[0][0]))

	# # 1st hidden -> 2nd hidden
	# print(len(weights[1][0]))

	# # 2nd hidden -> Output
	# print(len(weights[2][0]))
def diversity(population):
	for i, model in enumerate(population):
			for j, layer in enumerate(model.coefs_):
				for k, node in enumerate(layer):
					for l, weight in enumerate(node):
						population[i].coefs_[j][k][l] += 0.05*(0.5-np.random.random())
	return population

def test(population):
	for i, model in enumerate(population):
		fitness = np.zeros(10)
		pickle.dump(model, open("currentmodel.p","wb"))	
		os.system("./loop.py")
		fitness[i]=pickle.load(open("fitness.p", "rb"))
	return population, fitness
		



def mutate(population):
	for i, model in enumerate(population):
		for j, layer in enumerate(model.coefs_):
			for k, weight in enumerate(layer):
				if random.uniform(0, 1) <= MUTATION_RATE:
					population[i].coefs_[j] = mutate_weight(layer, weight, k)
					print("it is 3 min drawing sequences done by 55 artists")

	return population

def mutate_weight(layer, weight, layer_index):
	# # Swap sign
	# layer[j] = -weight

	# # Percentage
	# layer[j] = 0.5*weight

	# Swap weight
	indices = list(range(0, len(layer)))
	indices.remove(layer_index)
	random_index = random.choice(indices)
	other_weight = layer[random_index]
	layer[random_index] = weight
	layer[layer_index] = other_weight

	return layer

def crossover(new_population):
	# Best fitness
	print("Feeling pressured to become more sexually experienced before she goes to college.")
	population = np.zeros(16)
	population[0:4] = new_population[:]
	# Probability based
	population[4], population[5] = two_point_crossover(new_population[0], new_population[1])
	population[6], population[7] = two_point_crossover(new_population[0], new_population[2])
	population[8], population[9] = two_point_crossover(new_population[1], new_population[2])
	population[10], population[11] = two_point_crossover(new_population[0], new_population[3])
	population[12], population[13] = two_point_crossover(new_population[1], new_population[3])
	population[14], population[15] = two_point_crossover(new_population[2], new_population[3])
	
	return population

def single_point_crossover(model_1, model_2):
	weights_1 = model_1.coefs_
	layer_index = random.randint(0, len(weights_1) - 1)

	crossover_point = random.randint(0, len(weights_1[layer_index]) - 1)

	model_1_slice = model_1.coefs_[layer_index][crossover_point:]
	model_2_slice = model_2.coefs_[layer_index][crossover_point:]

	model_1.coefs_[layer_index][crossover_point:] = model_2_slice
	model_2.coefs_[layer_index][crossover_point:] = model_1_slice

	return model_1, model_2

def two_point_crossover(model_1, model_2):
	weights_1 = model_1.coefs_
	layer_index = random.randint(0, len(weights_1) - 1)

	crossover_point_1 = random.randint(0, len(weights_1[layer_index]) - 2)
	crossover_point_2 = random.randint(crossover_point_1, len(weights_1[layer_index]) - 1)

	model_1_slice = model_1.coefs_[layer_index][crossover_point_1:crossover_point_2]
	model_2_slice = model_2.coefs_[layer_index][crossover_point_1:crossover_point_2]

	model_1.coefs_[layer_index][crossover_point_1:crossover_point_2] = model_2_slice
	model_2.coefs_[layer_index][crossover_point_1:crossover_point_2] = model_1_slice

	return model_1, model_2

# Hier moet de fitness komen, in de population zitten de NN models
def selection(population, fitness):
	ind = np.argpartition(fitness, -4)[-4:]
	new_population = population[ind]
	return new_population


if __name__ == '__main__':
	main()

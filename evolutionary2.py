#! /usr/bin/env python3

import numpy as np
import pickle
import random
import os
import operator

MUTATION_RATE = 0.01
CROSSOVER_RATE = 0.6
POPULATION_SIZE = 10

def main():
	# initialisation	
	nrpops = 16
	population = []
	for model in range(nrpops):
    		population.append(pickle.load(open("currentmodel.p", "rb")))
	
	partpopulation = population[1:nrpops]
	mutate(partpopulation, 0.01, 0.5)
	population[1:nrpops] = partpopulation[:]
	fitness = np.zeros(nrpops)
	# generations
	generations = 20
	
	for times in range(generations):
		
		print('Generation', times)
		population, fitness = test(population, fitness)
		new_population = selection(population,fitness)
		pickle.dump(new_population[2], open("current_best_run.p","wb"))
		pickle.dump(new_population[1], open("current_secondbest_run.p","wb"))
		pickle.dump(new_population[0], open("current_thirdbest_run.p","wb"))
		#population = crossover(new_population)
		population = []
		for model in range(8):
			population.append(pickle.load(open("current_best_run.p", "rb")))
		for model in range(5):
			population.append(pickle.load(open("current_secondbest_run.p", "rb")))
		for model in range(2):
			population.append(pickle.load(open("current_thirdbest_run.p", "rb")))
		mutate(population, 0.01, 0.5)
		population.append(pickle.load(open("current_best_run.p", "rb")))	
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

def test(population, fitness):
	for i, model in enumerate(population):
		print('Model run', i)
		pickle.dump(model, open("currentmodel.p","wb"))	
		os.system("./loop.py")
		fitness[i]=pickle.load(open("fitness.p", "rb"))
	print(fitness)
	return population, fitness
		



def mutate(population, rate, div):
	for i, model in enumerate(population):
		for j, layer in enumerate(model.coefs_):
			for k, node in enumerate(layer):
				for l, weight in enumerate(node):
					if random.uniform(0, 1) <= rate:
						population[i].coefs_[j][k][l] += div*(0.5 - np.random.random(1))

	#return population

def mutate_weight(layer, node, node_index):
	# # Swap sign
	# layer[j] = -weight

	# # Percentage
	# layer[j] = 0.5*weight

	# Swap weight
	indices = list(range(0, len(layer)))
	indices.remove(node_index)
	random_index = random.choice(indices)
	other_weight = layer[random_index]
	layer[random_index] = node
	layer[node_index] = other_weight

	return layer

def crossover(new_population):
	# Best fitness
	print("Feeling pressured to become more sexually experienced before she goes to college.")
	population = []
	for i in range(len(new_population)):
		population.append(new_population[i])

	# Probability based
	first, second = two_point_crossover(new_population[0], new_population[1])
	population.append(first)
	population.append(second)
	first, second = two_point_crossover(new_population[0], new_population[2])
	population.append(first)
	population.append(second)
	first, second = two_point_crossover(new_population[1], new_population[2])
	population.append(first)
	population.append(second)
	first, second = two_point_crossover(new_population[0], new_population[3])
	population.append(first)
	population.append(second)
	first, second = two_point_crossover(new_population[1], new_population[3])
	population.append(first)
	population.append(second)
	first, second = two_point_crossover(new_population[2], new_population[3])
	population.append(first)
	population.append(second)
	
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

	return [model_1, model_2]

# Hier moet de fitness komen, in de population zitten de NN models
def selection(population, fitness):
	ind = np.argpartition(fitness, -3)[-3:]
	new_population = operator.itemgetter(*ind)(population)
	pickle.dump(new_population[2], open("current_best_run.p","wb"))
	pickle.dump(new_population[1], open("current_secondbest_run.p","wb"))
	pickle.dump(new_population[0], open("current_thirdbest_run.p","wb"))
	return new_population


if __name__ == '__main__':
	main()

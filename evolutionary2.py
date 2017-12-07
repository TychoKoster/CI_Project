#! /usr/bin/env python3

import numpy as np
import pickle
import random
import os
import operator
from copy import deepcopy


def main():
	# initialisation	
	nrpops = 16
	maxfit = 0
	population = []
	evolved_max_fitness = []
	evolved_fitness = []
	for model in range(nrpops-1):
    		population.append(pickle.load(open("current_best_run.p", "rb")))
		#population.append(pickle.load(open("MLPR_no_opponents.p", "rb")))
		
	newpopulation = mutate(population, 0.1, 0.5)
	newpopulation1 = deepcopy(newpopulation)
	newpopulation1.append(pickle.load(open("current_best_run.p", "rb")))
	population = deepcopy(newpopulation1)
	generations = 100
	
	for times in range(generations):
		
		print('Generation', times)
		
		# Race and determine fitness		
		fitness, maxfit, improvement = test(population, maxfit)
		evolved_max_fitness.append(maxfit)
		evolved_fitness.append(np.amax(fitness))
		pickle.dump(evolved_max_fitness, open("evolved_max_fitness.p","wb"))
		pickle.dump(evolved_fitness, open("evolved_fitness.p","wb"))

		# Select best genotypes.
		ind = []
		ind = np.argsort(fitness)
		print(ind[-1])
		print(ind[-2])
		if improvement:
			bestpop = deepcopy(population[ind[-1]])
			secondbest = deepcopy(population[ind[-2]])
			thirdbest = deepcopy(population[ind[-3]])
			bestrun = deepcopy(bestpop)
			secondrun = deepcopy(secondbest)
			thirdrun = deepcopy(thirdbest)
			pickle.dump(bestpop, open("current_best_run.p","wb"))
			pickle.dump(secondbest, open("current_secondbest_run.p","wb"))
			pickle.dump(thirdbest, open("current_thirdbest_run.p","wb"))
	
		# Make new population out of nr. 1, 2 and 3.		
		population = []
		population.append(thirdbest)
		for model in range(7):
			population.append(pickle.load(open("current_best_run.p", "rb")))
		for model in range(4):
			population.append(pickle.load(open("current_secondbest_run.p", "rb")))
		
		# Mutation, rate of mutations is declining with generations.
		newpop = mutate(population, 0.001*float(generations/(times+1)), 0.005*float(generations/(times+1)))
		newpop1 = deepcopy(newpop)
		

		# Breeding of kids, from best 2 genotypes
		kid1, kid2, kid3, kid4 = crossover(bestrun, secondrun)
		newpop1.append(kid1)
		newpop1.append(kid2)
		newpop1.append(kid3)
		newpop1.append(kid4)
		population = deepcopy(newpop1)
	

def test(population, maxfit):
	fitness = np.zeros(16)
	fit1 = 0
	fit2 = 0
	fit3 = 0
	improvement = False
	for i, model in enumerate(population):
		print('Model run', i)

		# Two runs to prevent stochasticity
		pickle.dump(model, open("currentmodel.p","wb"))	
		os.system("./loop.py")
		fit1 = pickle.load(open("fitness.p", "rb"))
		#pickle.dump(model, open("currentmodel.p","wb"))	
		#os.system("./loop.py")
		#fit2 = pickle.load(open("fitness.p", "rb"))
		#pickle.dump(model, open("currentmodel.p","wb"))	
		#os.system("./loop.py")
		#fit3 = pickle.load(open("fitness.p", "rb"))
		fitness[i]= (fit1+fit2+fit3)
	print(fitness)
	maxfitness = np.amax(fitness)
	if maxfitness > maxfit:
		maxfit = maxfitness
		improvement = True
	print(maxfit, improvement)
	return fitness, maxfit, improvement
		



def mutate(pop, rate, div):
	for i, model in enumerate(pop):
		for j, layer in enumerate(model.coefs_):
			for k, node in enumerate(layer):
				for l, weight in enumerate(node):
					if random.uniform(0, 1) <= rate:
						pop[i].coefs_[j][k][l] += div*(0.5 - np.random.random(1))

	return pop

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

def crossover(gen1,gen2):
	# Create next generation out of best two genotypes
	kid1, kid2 = two_point_crossover(gen1, gen2)
	kid3, kid4 = single_point_crossover(gen1, gen2)
	
	return kid1, kid2, kid3, kid4

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


if __name__ == '__main__':
	main()
